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
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        self.log.info('DataQualityOperator work in progress')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        self.log.info('This are my tables {}'.format(self.tables))
        for table in self.tables: 
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            self.log.info("This records are of type: {}".format(type(records)))
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"Data quality check failed. {table} returned no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"Data quality check failed. {table} contained 0 rows")
            if any(elem is None for elem in records):
                raise ValueError(f"Data quality check failed. {table} contains None element(s)")
            logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")

            