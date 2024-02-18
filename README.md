# dbt Autodoc

A simple CLI tool to dynamically create model documentation for a given model.

Unsurprisingly, the tool uses OpenAI to suggest a `yml` file for a given model. It parses the dbt manifest in order to assemble the code for the model as well as the description of the immediate upstream models.

## Installation

This tool can be installed with `pip`:

```bash
pip install git+https://github.com/radbrt/dbt-autodoc.git
```

The tool assumes you have your own OpenAI API key in an environment variable named `OPENAI_API_KEY`.

## Usage

When you are in your dbt project, get a suggestion for a model documentation by running `dbt-autodoc <your-model-name>`.

## Roadmap

This is intended to be a simple too without a lot of bells and whistles. But a few things come to mind:

- More tests. Because tests are good.
- Pluggable LLM backend. Because not everyone can use plain OpenAI.
- Option to write model documentation to file. Possibly a really bad idea, but what do I know?