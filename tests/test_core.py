"""Misc tests"""
import json
from dbt_autodoc.utils import (
  get_upstream_models, 
  parse_manifest, 
  get_upstream_models,
  compile_upstream_description_markdown,
  create_instructions
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

#country_report
  
def test_upstream_models_country_report():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('country_report', manifest)
  assert len(upstream_models) == 2

def test_compile_upstream_description_markdown_country_report():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('country_report', manifest)
  assert len(upstream_models) == 2
  upstream_description = compile_upstream_description_markdown('customers', manifest)
  assert "Seed data for customers" in upstream_description

def test_create_instructions_country_report():
  manifest = parse_manifest('tests/data/manifest_1.json')
  upstream_models = get_upstream_models('country_report', manifest)
  assert len(upstream_models) == 2
  upstream_description = create_instructions('customers', manifest)
  assert "SELECT ix*2 as ix2, upper(name) AS name FROM" in json.dumps(upstream_description)
