I just added a linting CI workflow. To run the tests locally type:

```
uv run black
uv run flake8 ./*.py # It runs in .venv, etc. otherwise
uv run ruff check .
```
