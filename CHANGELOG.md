# Changelog


## [3.1.1] - TBD

### Changed features
- Django 4.1.6 to 4.2.4

#### Merge of KCentre database into Centre Registry:
- new table Organisation, centre.organisation_name -> centre.organisation_fk
- new table KCentreServiceType
- new table ResourceFamily
- new table KCentreStatus
- new table KCentreFormQueue
- Centre 1...1 KCentre relation
#### New features:
- KCentre edit form exposed to the user
- KCentre edit manual review mechanism

## [3.1.0] - TBD

This is a migration milestone changing database backend, use this tag for importing data from sqlite backend 
at migration 0032_20200409_1923

### Changed features
- sqlite3 -> postgres db backend migration


## [3.0.0] - TBD

### Changed features
- Started CHANGELOG.md 
- Django 2.2.25 to 4.1.6
- Build config changed from setup.py to pyproject.toml
- Build backend from setuptools to poetry
