<div align="center">
    <h1>Modbot</h1>
    <h2>a simple discord bot I wrote</h2>
</div>

## Hacking

All our deps are managed through [`uv`](https://docs.astral.sh/uv/). There is a nix flak provided for convice

To start with run

```bash
uv sync
```
this will install all of the deps required by us. After this you should active the venv(.venv) and run `python modbot` to run modbot. In prodoction you should run `python -O modbot`to run in production mode to speed things up

### Committing

Before committing ensure per-commit is installed.
```
pre-commit install
```
pre-commit install will install the hook adnd when you commit using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)