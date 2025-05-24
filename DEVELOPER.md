All code in this repo is released under the MIT License. This means that you are free to fork the repository and modify it to answer whatever questions you have. 

## Installation
I used `uv` to manage my virtual environment while developing this project. To recreate my environment:
1. Clone this repository.
2. Install uv ([link](https://docs.astral.sh/uv/#installation){:target="_blank"}).
3. In the project directory type `uv sync`. This will create a virtual environment with the project's dependencies in `.venv`. 
4. Type `source .venv/bin/activate` to activate the virtual environment.

To run the app locally, type `streamlit run streamlit_app.py`.

To modify the data which the app uses, see `data/gen_county_data.py`.

## Linting

Continuous Integration (CI) for this repo runs `black`, `flake8` and `ruff` on each PR. Please run the following commands, and fix any errors they report, before making a PR:

```
uv run black .
uv run flake8 ./*.py
uv run ruff check .
```
