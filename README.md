# dbt Autodoc

A simple OpenAI-based CLI tool to dynamically create model documentation for a given model. 

The general idea is that this tool can help you document your project one model at the time. Once you document your sources and write your first model, this tool will be able to suggest a `yml` file for your first model based on the source(s) and the code. Once that documentation is in place, you can build your next model based on your previous one, and the previously generated documentation together with the new code will be used to generate the documentation for your new model. Using this approach you can follow the DAG of your dbt project and suggest documentation for all models, from left to right. Good documentation begets good documentation.

## How it works

For a given model, the dbt-autodoc parses the dbt manifest, finds the code for the model as well as the documentation of the upstream dependencies. It then sends this information to OpenAI's GPT-4 model, which suggests a `yml` file for the model. The suggested `yml` file is then printed to the console, and optionally written to a file.

The input is always the model code and the documentation for the immediate upstream dependencies. Well-documented upstream models are essential for good results.

You might want to note that the tool does not include macros in the input to the GPT-4 model. That would vastly increase the amount of code passed to the model, and would be unlikely to improve the quality of the suggestions as the output would likely be very code-centric.

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

## Example

An example of a yaml file suggested by the tool: https://github.com/radbrt/dbt_er/blob/master/models/job_ads/l2/l2_job_ads.yml

This suggestion was based on the upstream dependency (source): https://github.com/radbrt/dbt_er/blob/master/models/job_ads/job_ads_sources.yml, and the model code: https://github.com/radbrt/dbt_er/blob/master/models/job_ads/l2/l2_job_ads.sql

## Roadmap

This is intended to be a simple tool without a lot of bells and whistles. But a few things come to mind:

- More tests. Because tests are good.
- Pluggable LLM backend. Because not everyone can use plain OpenAI.