.PHONY: data check help

# Generate all CSVs into the data/ directory
data:
	uv run python -m scripts.gen_data

# Run formatting, linting, type checking, and tests
check:
	uv run ruff format .
	uv run ruff check .

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make data           Generate all CSV files into data/"
	@echo "  make check          Run formatting, linting, and type checks"
