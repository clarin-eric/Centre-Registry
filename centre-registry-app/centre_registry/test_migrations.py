#!/usr/bin/env python

from django import setup
from django.test import TransactionTestCase
from django_test_migrations.migrator import Migrator
import glob


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
        migrator = Migrator(database='default')

        # roll back to init state
        init_state = migrator.before(migrate_from=("centre_registry", "0001_initial"))

        migrations = glob.glob('./migrations').remove('__init__.py')

        # roll forward to final state
        final_state = migrator.after(migrate_to=("centre_registry", migrations[-1]))

        migrator.reset()