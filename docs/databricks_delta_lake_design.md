# Databricks & Delta Lake Architecture — Design Documentation

**Status: an authored architecture design — no Databricks workspace or
Delta Lake tables are provisioned in this environment.**

## Intended architecture
```
Source systems (EHR/claims, free-text dx/procedure descriptions)
        |
   Bronze Delta table (raw, as-landed, append-only)
        |
   Silver Delta table (src/standards_mapping.py's normalize + ICD-10/CPT
        mapping logic, applied as a Databricks notebook/job)
        |
   Gold Delta table (FHIR-shaped Condition/Procedure resources,
        analytics- and interoperability-ready)
```

## Why this shape
The medallion architecture (bronze/silver/gold) is the standard Databricks
Delta Lake pattern specifically because it keeps raw source data
immutable and auditable (bronze) while allowing the standards-mapping
transformation logic (this repository's real, executed code) to be
re-run against gold without ever risking the raw record.

## Honest disclosure
No Databricks workspace, cluster, or Delta Lake table exists in this
environment. The mapping and lineage logic in `src/` is executed locally
against simulated data with pandas, standing in for what would run as a
Databricks notebook/job against Delta tables in a real deployment.
