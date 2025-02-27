import unittest
from . import assertions

from pipelinewise.fastsync.mysql_to_bigquery import tap_type_to_target_type, sync_table, main_impl

PACKAGE_IN_SCOPE = 'pipelinewise.fastsync.mysql_to_bigquery'
TAP = 'FastSyncTapMySql'
TARGET = 'FastSyncTargetBigquery'


# pylint: disable=missing-function-docstring,invalid-name,no-self-use
class MySQLToBigQuery(unittest.TestCase):
    """
    Unit tests for fastsync mysql to bigquery
    """
    def test_tap_type_to_target_type_with_defined_tap_type_returns_equivalent_target_type(self):
        self.assertEqual('STRING', tap_type_to_target_type('binary', None))
        self.assertEqual('STRING', tap_type_to_target_type('geometry', None))
        self.assertEqual('STRING', tap_type_to_target_type('point', None))
        self.assertEqual('STRING', tap_type_to_target_type('linestring', None))
        self.assertEqual('STRING', tap_type_to_target_type('polygon', None))
        self.assertEqual('STRING', tap_type_to_target_type('multipoint', None))
        self.assertEqual('STRING', tap_type_to_target_type('multilinestring', None))
        self.assertEqual('STRING', tap_type_to_target_type('multipolygon', None))
        self.assertEqual('STRING', tap_type_to_target_type('geometrycollection', None))

    def test_tap_type_to_target_type_with_undefined_tap_type_returns_STRING(self):
        self.assertEqual('STRING', tap_type_to_target_type('random-type', 'random-type'))

    @staticmethod
    def test_sync_table_runs_successfully_returns_true():
        assertions.assert_sync_table_returns_true_on_success(sync_table, PACKAGE_IN_SCOPE, TAP, TARGET)

    @staticmethod
    def test_sync_table_exception_on_copy_table_returns_failed_table_name_and_exception():
        assertions.assert_sync_table_exception_on_failed_copy(sync_table, PACKAGE_IN_SCOPE, TAP, TARGET)

    @staticmethod
    def test_main_impl_with_all_tables_synced_successfully_should_exit_normally():
        assertions.assert_main_impl_exit_normally_on_success(main_impl, PACKAGE_IN_SCOPE, TAP, TARGET)

    @staticmethod
    def test_main_impl_with_one_table_fails_to_sync_should_exit_with_error():
        assertions.assert_main_impl_should_exit_with_error_on_failure(main_impl, PACKAGE_IN_SCOPE, TAP, TARGET)


if __name__ == '__main__':
    unittest.main()
