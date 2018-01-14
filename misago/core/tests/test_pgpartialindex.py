from django.db import connection
from django.test import TestCase

from misago.threads.models import Thread

from misago.core.pgutils import PgPartialIndex


class PgPartialIndexTests(TestCase):
    def setUp(self):
        self.skipTest('Fix search')  # TODO

    def test_multiple_fields(self):
        """multiple fields are supported"""
        with connection.schema_editor() as editor:
            sql = PgPartialIndex(
                fields=['has_events', 'is_hidden'],
                name='test_partial',
                where={'has_events': True},
            ).create_sql(Thread, editor)

            self.assertIn('CREATE INDEX "test_partial" ON "misago_threads_thread"', sql)
            self.assertIn('ON "misago_threads_thread" ("has_events", "is_hidden")', sql)

    def test_where_clauses(self):
        """where clauses generate correctly"""
        with connection.schema_editor() as editor:
            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events': True},
            ).create_sql(Thread, editor)

            self.assertTrue(sql.endswith('WHERE "has_events" = true'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events': False},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" = false'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events': 42},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" = 42'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events__lt': 42},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" < 42'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events__gt': 42},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" > 42'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events__lte': 42},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" <= 42'))

            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={'has_events__gte': 42},
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" >= 42'))

    def test_multiple_where_clauses(self):
        """where clause with multiple conditions generates correctly"""
        with connection.schema_editor() as editor:
            sql = PgPartialIndex(
                fields=['has_events'],
                name='test_partial',
                where={
                    'has_events__gte': 42,
                    'is_hidden': True,
                },
            ).create_sql(Thread, editor)
            self.assertTrue(sql.endswith('WHERE "has_events" >= 42 AND "is_hidden" = true'))

    def test_set_name_with_model(self):
        """valid index name is autogenerated"""
        index = PgPartialIndex(
            fields=['has_events', 'is_hidden'],
            where={'has_events': True},
        )
        index.set_name_with_model(Thread)
        self.assertEqual(index.name, 'misago_thre_has_eve_1b05b8_part')

        index = PgPartialIndex(
            fields=['has_events', 'is_hidden', 'is_closed'],
            where={'has_events': True},
        )
        index.set_name_with_model(Thread)
        self.assertEqual(index.name, 'misago_thre_has_eve_eaab5e_part')

        index = PgPartialIndex(
            fields=['has_events', 'is_hidden', 'is_closed'],
            where={
                'has_events': True,
                'is_closed': False,
            },
        )
        index.set_name_with_model(Thread)
        self.assertEqual(index.name, 'misago_thre_has_eve_e738fe_part')

    def test_index_repr(self):
        """index creates descriptive representation string"""
        index = PgPartialIndex(
            fields=['has_events'],
            where={'has_events': True},
        )
        self.assertEqual(repr(index), "<PgPartialIndex: fields='has_events', where='has_events=True'>")

        index = PgPartialIndex(
            fields=['has_events', 'is_hidden'],
            where={'has_events': True},
        )
        self.assertIn("fields='has_events, is_hidden',", repr(index))
        self.assertIn(", where='has_events=True'", repr(index))

        index = PgPartialIndex(
            fields=['has_events', 'is_hidden', 'is_closed'],
            where={
                'has_events': True,
                'is_closed': False,
                'replies__gte': 5,
            },
        )
        self.assertIn("fields='has_events, is_hidden, is_closed',", repr(index))
        self.assertIn(", where='has_events=True, is_closed=False, replies__gte=5'", repr(index))
