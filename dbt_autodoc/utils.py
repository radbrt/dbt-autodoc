"""Some utility functions."""
from openai import OpenAI
import json
import os

def parse_manifest(file_path):
    """Parse the manifest file and return the parsed content."""

    if not os.path.exists('dbt_project.yml'):
        raise FileNotFoundError(f"dbt_project.yml not found. Are you in the dbt directory?")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"dbt manifest not found. Have you run a dbt command such as `dbt run` or `dbt compile`?")
    
    with open(file_path, 'r') as file:
        return json.load(file)

def get_nodes_and_sources(manifest):
    """Get the nodes and sources from the manifest."""
    return {**manifest['nodes'], **manifest['sources']}

def get_model_from_name(model_name, manifest):
    """Get the model from the manifest."""
    nodes_and_sources = get_nodes_and_sources(manifest)
    for id, model in nodes_and_sources.items():
        if model['name'] == model_name:
            return model
    raise ValueError(f"Model {model_name} not found in the manifest")

def get_upstream_models(model_name, manifest):
    """Get the upstream models of a model."""
    model = get_model_from_name(model_name, manifest)
    nodes_and_sources = get_nodes_and_sources(manifest)

    if model:
        upstrea_models = [nodes_and_sources[model_id] for model_id in model['depends_on']['nodes']]
        return upstrea_models
    return []

def compile_upstream_description_markdown(model_name, manifest):
    """Compile the upstream models into a markdown string."""
    upstream_models = get_upstream_models(model_name, manifest)

    all_models = []
    if upstream_models:
        for model in upstream_models:
            top_level_description = f'{model["name"]}: {model.get("description") or "(no description)"}'
            column_descriptions = '\n'.join(
                [f'* {column}: {content.get("description") or "(no description)"}' 
                for column, content in model['columns'].items()]
                ) or '(no columns defined)'
            all_models.append(f'{top_level_description}\nColumns:\n{column_descriptions}')
    return '\n\n'.join(all_models)

def create_instructions(model_name, manifest):
    """Create a markdown string with instructions for the model."""
    model_description = compile_upstream_description_markdown(model_name, manifest)

    raw_code = get_model_from_name(model_name, manifest)['raw_code']

    REQUEST = f"""
Create a table description for the dbt model `{model_name}`, given the following:

The code for the model:
```
{raw_code}
```

Description of the upstream models:
{model_description}

The output should be a JSON with the following structure:
{{
    "name": "{model_name}",
    "description": "The description of the model"
    "columns": [
      {{"name": "column1", "description": "The description of the column"}},
      {{"name": "column2", "description": "The description of the column"}},
      ...
      ]
}}
"""

    return REQUEST

def generate_docs(model_name, manifest):
    """Generate documentation for the model."""
    updoc = create_instructions(model_name, manifest)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
      model="gpt-4-turbo-preview", 
      messages=[
        {"role": "system", 
        "content": "You are a data analyst, and read Business documentation as well as SQL to create documentation for new dbt models"},
        {"role": "user", "content": updoc}
      ],
      response_format={"type": "json_object"}
    )

    j = json.loads(response.choices[0].message.model_dump_json())
    jc = json.loads(j['content'])
    return jc
