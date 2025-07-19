# GitHub Actions Workflows

This directory contains the continuous integration and deployment workflows for the divine-thegraph-token-api project.

## Workflows

### ci.yml - Continuous Integration
- **Triggers**: On every push to main/develop branches and all pull requests
- **Jobs**:
  - **test**: Runs pytest with coverage on multiple OS (Ubuntu, Windows, macOS) with Python 3.13
  - **lint**: Runs ruff linter and formatter, plus mypy type checking
  - **security**: Runs Trivy vulnerability scanner
  - **build**: Builds the Python package after tests pass
- **Features**:
  - Caches pip dependencies for faster runs
  - Uploads coverage reports to Codecov
  - Enforces 90% minimum coverage threshold
  - Tests on multiple operating systems

### pypi-publish.yml - Package Publishing
- **Triggers**: On version tags (v*, v*.*.*)
- **Jobs**:
  - **test**: Runs full CI test suite (calls ci.yml)
  - **build**: Builds distribution packages (only if tests pass)
  - **publish-to-pypi**: Publishes to PyPI using trusted publishing
  - **github-release**: Creates GitHub release with signed artifacts
- **Features**:
  - Only publishes after all tests pass
  - Uses PyPI trusted publishing (no API tokens needed)
  - Signs artifacts with Sigstore
  - Creates GitHub releases automatically

### dependency-review.yml - Dependency Security Review
- **Triggers**: On pull requests that modify dependencies
- **Features**:
  - Reviews dependency changes for security vulnerabilities
  - Fails on high severity issues
  - Only allows approved licenses
  - Comments summary in PR

### badges.yml - Badge Generation
- **Triggers**: After CI workflow completes or on push to main
- **Features**:
  - Creates badge JSON files for README
  - Updates coverage, test status, and Python version badges

## Setup Requirements

1. **PyPI Publishing**:
   - Configure PyPI trusted publishing in your PyPI project settings
   - Add the `pypi` environment in GitHub repository settings

2. **Codecov** (optional):
   - Add `CODECOV_TOKEN` to repository secrets for coverage reporting

3. **Branch Protection**:
   - Enable branch protection on `main` branch
   - Require CI status checks to pass before merging

## Local Testing

To run the same tests locally:
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests with coverage
pytest -v --cov=thegraph_thegraph_token_api --cov-report=term-missing

# Run linting
pip install ruff mypy
ruff check .
ruff format --check .
mypy src/thegraph_thegraph_token_api --ignore-missing-imports
```
