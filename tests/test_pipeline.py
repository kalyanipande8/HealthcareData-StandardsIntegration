import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_source_data import simulate
from src.standards_mapping import map_standards, to_fhir_resources, mapping_completeness
from src.data_lineage import verify_lineage_completeness
from src.code_standards import ICD10_MAP, CPT_MAP


@pytest.fixture(scope="module")
def mapped():
    source = simulate()
    return map_standards(source)


def test_500_encounters_simulated():
    assert len(simulate()) == 500


def test_icd10_codes_are_real_format(mapped):
    codes = mapped["diagnosis_icd10"].dropna().unique()
    assert set(codes) <= set(ICD10_MAP.values())


def test_cpt_codes_are_real_format(mapped):
    codes = mapped["procedure_cpt"].dropna().unique()
    assert set(codes) <= set(CPT_MAP.values())


def test_mapping_handles_inconsistent_casing(mapped):
    """Confirms normalization actually works despite the injected
    casing/whitespace noise -- not a trivial 0% or 100% by luck."""
    result = mapping_completeness(mapped)
    assert result["icd10_mapping_rate_pct"] == 100.0
    assert result["cpt_mapping_rate_pct"] == 100.0


def test_fhir_resources_built_for_every_encounter(mapped):
    resources = to_fhir_resources(mapped)
    assert len(resources) == 2 * len(mapped)


def test_lineage_is_genuinely_verified(mapped):
    result = verify_lineage_completeness(mapped)
    assert result["pct_lineage_verified"] == 100.0
    assert result["n_verified_present"] == result["n_checkable_targets"]
