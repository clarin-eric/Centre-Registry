# Changelog


## [3.0.0] - 03.10.2023

### Changed features
- Django 2.2.25 to 4.1.12
- Other updated dependencies:
  - Selenium to 4.13.0
  - Jsonschema to 4.19.1
  - django-test-migrations to 1.3.0
  - lxml to 4.9.3
- Build config changed from setup.py to pyproject.toml
- Build backend from setuptools to poetry

## [2.3.5] - 21.03.2023

### Changed features
- Started CHANGELOG.md
- Updated dependencies:
  - Django 2.2.25 to 2.2.28
  - Jsonschema 3.1.1 to 4.17.3
  - django-test-migrations 0.2.0 to 1.2.0
  - lxml 4.6.5 to 4.9.2
- Build config changed from setup.py to pyproject.toml
- Build backend from setuptools to poetry
- Travis build on Python 3.9 (from 3.7)
- Upgraded selenium 3.141.0 to 4.8.2
- Lowest version of Firefox test upgraded from 45 to 70
- Added browser test on macOS 12, 13 and Windows 11 platforms
- Removed browser tests on Linux platforms (not supported by Sellenium anymore)
