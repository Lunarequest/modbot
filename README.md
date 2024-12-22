<div align="center">
    <h1>Modbot</h1>
    <h2>a simple discord bot to handle modoeration in The shoe</h2>
</div>

## Hacking

All our deps are managed through `poetry`(currently our nix flakes do not work). In the furture we may switch to flakes.

To start with run

```bash
poetry install
```
this will install all of the deps required by poetry. After this you should use `poetry shell` to run modbot.

### Committing

Before committing ensure per-commit is installed(simply being in a `poetry shell` should be enough). please resolve all of the issues raised by the `pre-commit` hooks. most of the time this involves running `black` on the code base