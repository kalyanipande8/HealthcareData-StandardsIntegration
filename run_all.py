"""End-to-end: simulate source records, map to ICD-10/CPT standards,
build FHIR resources, and verify data-lineage completeness."""
import json
import os

from src.simulate_source_data import simulate
from src.standards_mapping import map_standards, to_fhir_resources, mapping_completeness
from src.data_lineage import get_lineage_table, verify_lineage_completeness

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Simulating 500 raw patient encounters ===")
source = simulate()
source.to_csv("data/source_raw.csv", index=False)
print(source.shape)

print("\n=== Mapping to ICD-10-CM / CPT standards ===")
mapped = map_standards(source)
mapped.to_csv("data/mapped_standards.csv", index=False)
completeness = mapping_completeness(mapped)
print(completeness)

print("\n=== Building FHIR R4 resources ===")
resources = to_fhir_resources(mapped)
print(f"{len(resources)} FHIR resources built")
print(resources[0])

print("\n=== Data lineage documentation + verification ===")
lineage_table = get_lineage_table()
lineage_table.to_csv("results/source_to_target_mapping.csv", index=False)
lineage_verification = verify_lineage_completeness(mapped)
print(lineage_verification)

summary = {
    "n_encounters": completeness["n_encounters"],
    "icd10_mapping_rate_pct": completeness["icd10_mapping_rate_pct"],
    "cpt_mapping_rate_pct": completeness["cpt_mapping_rate_pct"],
    "n_fhir_resources": len(resources),
    "pct_lineage_verified": lineage_verification["pct_lineage_verified"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
