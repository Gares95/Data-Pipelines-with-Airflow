from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 table="",
                 sql = "",
                 functionality="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.functionality = functionality

    def execute(self, context):
        self.log.info('LoadDimensionOperator work in progress')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        if self.functionality == "truncate":
            self.log.info("Clearing data from destination Redshift table")
            redshift.run("DELETE FROM {}".format(self.table))

            self.log.info("Inserting data from staging tables to {} fact table".format(self.table))
            formatted_sql = "INSERT INTO {} {}".format(self.table, self.sql)
        elif self.functionality == "append-only":
            self.log.info("Inserting data from staging tables to {} fact table".format(self.table))
            formatted_sql = "INSERT INTO {} {}".format(self.table, self.sql)
        redshift.run(formatted_sql)