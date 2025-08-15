.PHONY: help install validate test clean

# Default target
help:
	@echo "n8n Workflow Validator - Available commands:"
	@echo ""
	@echo "  install      - Install Python dependencies"
	@echo "  validate     - Validate all n8n workflows"
	@echo "  fix          - Fix common workflow issues automatically"
	@echo "  validate-fix - Fix issues then validate (recommended)"
	@echo "  test         - Run validation on a specific file"
	@echo "  clean        - Remove Python cache files"
	@echo "  setup        - Install pre-commit hooks"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Validate all workflows
validate: install
	python validate_n8n_workflows.py workflow/

# Fix common workflow issues
fix: install
	python fix_n8n_workflows.py workflow/

# Validate and fix workflows
validate-fix: fix validate

# Test validation on a specific file
test: install
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make test FILE=workflow/filename.json"; \
		exit 1; \
	fi
	python validate_n8n_workflows.py $(FILE)

# Clean up Python cache
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Setup pre-commit hooks
setup: install
	pre-commit install
	@echo "Pre-commit hooks installed successfully!"
	@echo "Validation will now run automatically on each commit."

# Validate and show detailed output
validate-verbose: install
	python validate_n8n_workflows.py workflow/ --verbose

# Quick validation check (exit on first error)
validate-fast: install
	python validate_n8n_workflows.py workflow/ --fast