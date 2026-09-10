# Wishlist

A small Secret Santa assignment generator. It loads people and policy YAML,
creates assignments, and writes a Mermaid Markdown diagram for each run.

## Setup

Install the project and development tools:

```bash
uv sync
```

Optional local path overrides belong in `.env`. Start from the example:

```bash
cp .env.example .env
```

## Configure a draw

- Edit people and relationships in `config/secret_santa.yaml`.
- Edit draw rules in `config/policies/exclude_spouse.yaml`.
- Set `CONFIG_PATH` and `POLICY_CONFIG_PATH` in `.env` only when using
  different files.

## Run

From the repository root:

```bash
uv run main.py
```

The generated Mermaid Markdown run is written under `runs/auto/`.

## Development

```bash
uv run pytest
uv run ruff check .
```

## Layout

- `wishlist/`: application source code.
- `config/`: editable Secret Santa data and policies.
- `runs/`: generated and manually saved run documents.

Future Docker files belong at the repository root beside `pyproject.toml`.
