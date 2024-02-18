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

When you are in your dbt project, get a suggestion for a model documentation by running `dbt-autodoc` or the shorthand alias `ddoc`:

```bash
dbt-autodoc <your-model-name>
```

Or equivalently:

```bash
ddoc <your-model-name>
```

This will print the suggested `yml` file to the console. 

If you want to save it to a file directly, you can use the `--write` or `-w` flag. This will write the suggested `yml` file to a `yml` file next to the `sql` file of the model. Make sure to check the file manually though, before committing it to your repository. Not all suggestions make sense, and some modifications are usually in order.

```bash
ddoc <your-model-name> --write
```

## Roadmap

This is intended to be a simple too without a lot of bells and whistles. But a few things come to mind:

- More tests. Because tests are good.
- Pluggable LLM backend. Because not everyone can use plain OpenAI.