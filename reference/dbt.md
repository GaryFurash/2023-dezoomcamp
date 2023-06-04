# DBT

## Installing in Python VENV

```bash
python -m venv .venv_dbt
source .venv_dbt/bin/activate
pip install --upgrade pip setuptools
pip install --upgrade dbt-core
# add the bigquery adapter
pip install --upgrade dbt-bigquery
```
