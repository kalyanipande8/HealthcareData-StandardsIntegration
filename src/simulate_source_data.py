"""Simulate raw source system records (free-text diagnosis/procedure
descriptions, inconsistent casing/spacing) for 500 patient encounters --
the real starting point a standards-mapping pipeline has to normalize."""
from __future__ import annotations

import random

import pandas as pd

from .code_standards import ICD10_MAP, CPT_MAP

N_ENCOUNTERS = 500
SEED = 139


def simulate(n: int = N_ENCOUNTERS, seed: int = SEED) -> pd.DataFrame:
    rng = random.Random(seed)
    diagnoses = list(ICD10_MAP.keys())
    procedures = list(CPT_MAP.keys())

    rows = []
    for i in range(n):
        dx = rng.choice(diagnoses)
        proc = rng.choice(procedures)
        # realistic inconsistent casing/whitespace from free-text entry
        dx_raw = dx.upper() if rng.random() < 0.3 else dx
        dx_raw = f"  {dx_raw} " if rng.random() < 0.2 else dx_raw
        proc_raw = proc.title() if rng.random() < 0.3 else proc

        rows.append({
            "encounter_id": f"ENC-{i:05d}",
            "diagnosis_description_raw": dx_raw,
            "procedure_description_raw": proc_raw,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
    print(df.head())
