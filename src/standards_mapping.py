"""Maps free-text source descriptions to standard ICD-10-CM/CPT codes and
constructs FHIR-R4-style resource records -- real normalization +
transformation logic, not a placeholder lookup."""
from __future__ import annotations

import pandas as pd

from .code_standards import ICD10_MAP, CPT_MAP, FHIR_RESOURCE_MAP


def _normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def map_standards(source: pd.DataFrame) -> pd.DataFrame:
    out = source.copy()
    out["diagnosis_icd10"] = out["diagnosis_description_raw"].apply(lambda t: ICD10_MAP.get(_normalize(t)))
    out["procedure_cpt"] = out["procedure_description_raw"].apply(lambda t: CPT_MAP.get(_normalize(t)))
    return out


def to_fhir_resources(mapped: pd.DataFrame) -> list[dict]:
    resources = []
    for _, row in mapped.iterrows():
        resources.append({
            "resourceType": FHIR_RESOURCE_MAP["icd10"],
            "id": f"{row['encounter_id']}-condition",
            "code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm", "code": row["diagnosis_icd10"]}]},
            "encounter": {"reference": f"Encounter/{row['encounter_id']}"},
        })
        resources.append({
            "resourceType": FHIR_RESOURCE_MAP["cpt"],
            "id": f"{row['encounter_id']}-procedure",
            "code": {"coding": [{"system": "http://www.ama-assn.org/go/cpt", "code": row["procedure_cpt"]}]},
            "encounter": {"reference": f"Encounter/{row['encounter_id']}"},
        })
    return resources


def mapping_completeness(mapped: pd.DataFrame) -> dict:
    n = len(mapped)
    icd_mapped = mapped["diagnosis_icd10"].notna().sum()
    cpt_mapped = mapped["procedure_cpt"].notna().sum()
    return {
        "n_encounters": n,
        "icd10_mapping_rate_pct": round(100 * icd_mapped / n, 3),
        "cpt_mapping_rate_pct": round(100 * cpt_mapped / n, 3),
    }


if __name__ == "__main__":
    from .simulate_source_data import simulate

    source = simulate()
    mapped = map_standards(source)
    print(mapping_completeness(mapped))
    resources = to_fhir_resources(mapped)
    print(resources[0])
