All code in this repo is released under the MIT License. This means that you are free to fork the repository and modify it to answer whatever questions you have. 

## Installation
I used `uv` to manage my virtual environment while developing this project. To recreate my environment:
1. Clone this repository.
2. Install uv ([link](https://docs.astral.sh/uv/#installation)).
3. In the project directory type `uv sync`. This will create a virtual environment with the project's dependencies in `.venv`. 
4. Type `source .venv/bin/activate` to activate the virtual environment.
5. Type `streamlit run streamlit_app.py` to run the app locally.

## Modifying the App

The front end code is in `streamlit_app.py`.

The data which powers the app is in `data/county_data.csv`.

To modify the data which the app uses, see `data/gen_county_data.py`.

## Linting

This repo has a workflow enabled that runs `black`, `flake8` and `ruff` on each PR. If you are making a PR to this repo, please run the following commands prior to making a PR:

```
uv run black .
uv run flake8 ./*.py
uv run ruff check .
```
