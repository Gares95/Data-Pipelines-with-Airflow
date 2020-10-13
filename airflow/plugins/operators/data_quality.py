import logging
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 tables=[],
                 checks=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.checks = checks

    def execute(self, context):
        self.log.info('DataQualityOperator work in progress')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        self.log.info('This are my tables {}'.format(self.tables))
        for table in self.tables: 
#             columns = redshift_hook.get_records(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}';")
            columns = redshift_hook.get_records(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' ORDER BY ORDINAL_POSITION;")
            self.log.info('This are my columns {}'.format(columns))
            i = 0
            for check in self.checks:
                if i == 0:
                    sql = check.get('check_sql').format(table)
                else:
                    self.log.info('This is my column: {}'.format(columns[0][0]))
                    sql = check.get('check_sql').format(table,columns[0][0])
                    self.log.info('This is sql: {}'.format(sql))
                exp_result = check.get('expected_result')
                records = redshift_hook.get_records(sql)
                self.log.info('This is the count: {}'.format(records[0][0]))
                if (records[0][0] > 0) != exp_result:
                    raise ValueError(f"Data quality check failed. {table}")
                i += 1
            logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")

            