"""Misc tests"""

from dbt_autodoc.utils import get_column_descriptions, parse_manifest, get_upstream_models

def test_column_descriptions():
  manifest = parse_manifest('tests/data/manifest_1.json')
  col_desc = list(get_column_descriptions('customers', manifest))
  assert len(col_desc) == 2

def test_upstream_models():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('customers', manifest)
  assert len(upstream_models) == 1