import click
from dbt_autodoc.utils import (
  parse_manifest,
  generate_docs
)
import os
from openai import OpenAI
import io
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

@click.command()
@click.argument('model', required=True)
def autodoc(model):
    """Main dbt-autodoc command entrypoint"""
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError('OPENAI_API_KEY environment variable not set')
    manifest_path = 'target/manifest.json'
    manifest = parse_manifest(manifest_path)
    docs = generate_docs(model, manifest)

    ordered_data = CommentedMap()
    ordered_data['name'] = docs['name']
    ordered_data['description'] = docs['description']
    ordered_data['columns'] = docs['columns']

    full_data = CommentedMap()
    full_data['version'] = 2
    full_data['models'] = [ordered_data]

    yaml = YAML()
    yaml.indent(sequence=4, offset=2)
    yaml.preserve_quotes = True
    output_stream = io.StringIO()
    yaml.dump(full_data, output_stream)
    yaml_string = output_stream.getvalue()
    output_stream.close()
    print(yaml_string)