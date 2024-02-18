"""Misc tests"""

from dbt_autodoc.utils import (
  get_upstream_models, 
  parse_manifest, 
  get_upstream_models,
  compile_upstream_description_markdown
)

def test_upstream_models():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('customers', manifest)
  assert len(upstream_models) == 1

def test_compile_upstream_description_markdown():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('customers', manifest)
  assert len(upstream_models) == 1
  upstream_description = compile_upstream_description_markdown('customers', manifest)
  assert "The name of the customer" in upstream_description 