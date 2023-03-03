#!/usr/bin/env python

from django import setup
from django.test import TransactionTestCase
from django_test_migrations.migrator import Migrator
import glob
import os
import pathlib


class MigrationChainTest(TransactionTestCase):
    fixtures = ["test_data"]

    @classmethod
    def setUpClass(cls):
        super(MigrationChainTest, cls).setUpClass()
        setup()

    @classmethod
    def tearDownClass(cls):
        super(MigrationChainTest, cls).tearDownClass()

    def test_migration_chain(self):
        app_dir_path = pathlib.Path(__file__).parent
        migrations_dir_path = app_dir_path.joinpath('migrations')
        migrations = sorted(glob.glob(str(migrations_dir_path) + '/[0-9]*'))

        if not migrations:
            self.fail("No migration files have been found in: " + migrations_dir_path)
        migrator = Migrator(database='default')

        # roll back to init state
        init_state = migrator.apply_initial_migration(migrate_from=("centre_registry", os.path.splitext(os.path.basename(migrations[0]))[0]))

        # roll forward to final state
        final_state = migrator.apply_tested_migration(migrate_to=("centre_registry", os.path.splitext(os.path.basename(migrations[-1]))[0]))
        migrator.reset()