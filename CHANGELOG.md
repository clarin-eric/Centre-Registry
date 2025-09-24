# Changelog

## [3.0.2] - TBD

### New features
- venv bundling Python inside app container
- management command for updating certification status based on AssessmentDate
- email notification to maintainers about centre's certification expiring
- well controlled vocabulary for Centre's Type Status
- reordering admin fields according to maintainer request
- historical models
- country field changed from CharField to django_countries.CountryField
- pruning redundant (artifacts) address fields between Centre and Consortium
- init OpenAPI documentation of endpoints (only Centre .json endpoint so far, no trivial .xsd to OpenAPI for xml endpoints)
- dependency bump
- centre.type_certification_status_fk M2M bundling assessment date and certification status that were previously unrelated on the data model level
- country in XML API source changed from consortium to centre
- adjusted XML API template to centre.type_certification_status_fk

### New dependencies
- django-countries 7.6.1
- django-simple-history 3.7.0
- tzdata 2025.1
- xmlschema 3.4.4

### Dependency bumps
- Django 4.2.11 -> 4.2.24
- django-debug-toolbar 4.3.0 -> 5.2.0
- django-test-migrations 1.3.0 -> 1.4.0
- djangorestframework 3.15.1 -> 3.15.2
- drf-spectacular 0.27.0 -> 0.28.0
- jsonschema 4.21.1 -> 4.23.0
- lxml 5.2.1 -> 5.3.1
- selenium 4.19.0 -> 4.29.0

## [3.0.1] - 25.04.2024

### New features
- `api/all_centres_full` endpoint for CLARIN website
- project root `.pytoml` building Centre Registry packages (`centre-registry-app`; `Centre-Registry-config`) into a single package
- `.whl` build and distribution via release

### Changed features
- Fixed validation of geographical coordinates on administration interface. #79
- Updated dependencies:
  - Django 4.1.11 to Django 4.2.11
  - django-debug-toolbar 4.2.0 to 4.3.0
  - Jsonschema 4.19.1 to 4.21.1
  - lxml 4.9.3 to 5.2.1
  - Selenium 4.13.0 to 4.19.0
- Added dependency on djangorestframework 3.15.1

## [3.0.0] - 03.10.2023

### Changed features
- Django 2.2.25 to 4.1.11
- Other updated dependencies:
  - Selenium to 4.13.0
  - Jsonschema to 4.19.1
  - django-test-migrations to 1.3.0
  - django-debug-toolbar 4.2.0
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
