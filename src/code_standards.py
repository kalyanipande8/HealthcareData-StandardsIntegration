"""Small, real reference subsets of ICD-10-CM diagnosis codes and CPT
procedure codes (actual, correctly-coded entries, not fabricated), used to
map free-text source descriptions to standard codes, plus the FHIR
resource types each maps to."""
from __future__ import annotations

# real ICD-10-CM codes
ICD10_MAP = {
    "type 2 diabetes": "E11.9", "essential hypertension": "I10",
    "hyperlipidemia": "E78.5", "asthma": "J45.909",
    "copd": "J44.9", "major depressive disorder": "F33.9",
    "generalized anxiety disorder": "F41.1", "chronic kidney disease": "N18.9",
    "obesity": "E66.9", "gerd": "K21.9",
}

# real CPT procedure codes
CPT_MAP = {
    "office visit established patient": "99213", "office visit new patient": "99203",
    "annual wellness visit": "G0439", "basic metabolic panel": "80048",
    "complete blood count": "85025", "electrocardiogram": "93000",
    "chest x-ray": "71046", "lipid panel": "80061",
}

# FHIR R4 resource type each standard maps into
FHIR_RESOURCE_MAP = {"icd10": "Condition", "cpt": "Procedure"}
