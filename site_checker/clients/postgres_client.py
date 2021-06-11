import logging
import sys

from configs import PostgresConfig
from models import WebsiteMetrics
from psycopg2 import DatabaseError
from psycopg2.pool import SimpleConnectionPool


class PostgresClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create_connection_pool(
        self, postgres_config: PostgresConfig
    ) -> SimpleConnectionPool:
        """Create Simple Postgres Connection Pool
        https://pynative.com/psycopg2-python-postgresql-connection-pooling/#h-simpleconnectionpool

        Args:
            postgres_config (PostgresConfig): Postgres configurations

        Returns:
            SimpleConnectionPool: Postgres connection pool
        """

        connection_pool = None
        try:
            connection_pool = SimpleConnectionPool(
                minconn=postgres_config.min_connection,
                maxconn=postgres_config.max_connection,
                user=postgres_config.user,
                password=postgres_config.password,
                host=postgres_config.host,
                port=postgres_config.port,
                database=postgres_config.database,
                sslmode=postgres_config.sslmode,
                sslrootcert=postgres_config.sslrootcert,
            )
            if connection_pool:
                self.logger.info("SQL Database connection pool created successfully")
        except (Exception, DatabaseError) as e:
            self.logger.exception(f"Error while connecting to PostgreSQL\n{e}")
            sys.exit(1)

        return connection_pool

    def _execute_query(self, connection, query) -> None:
        """Execute query provided using the database connection provided"""

        connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            self.logger.debug(f"Query executed: {query}")
        except (Exception, DatabaseError) as e:
            self.logger.exception(f"Error running the query: {query}\n{e}")

    def insert(self, connection, website_metrics: WebsiteMetrics) -> None:
        """Insert template statement for website metrics"""

        insert_statement = f"""
        INSERT INTO
            site_checker.{website_metrics.name}
            (url, regex, has_regex, status_code, response_time, ocurred_at)
        VALUES (
            '{website_metrics.url}',
            '{website_metrics.regex}',
            {website_metrics.has_regex},
            {website_metrics.status_code},
            {website_metrics.response_time},
            '{website_metrics.ocurred_at}'
        )
        """

        self._execute_query(connection, insert_statement)

    def create_table(self, connection, topic_name: str) -> None:
        """Create database table for the topic_name provided"""

        create_schema = f"CREATE SCHEMA IF NOT EXISTS site_checker"
        create_table = f"""
            CREATE TABLE IF NOT EXISTS site_checker.{topic_name} (
                id SERIAL PRIMARY KEY,
                url VARCHAR(1024),
                regex VARCHAR(1024),
                has_regex BOOL,
                status_code SMALLINT,
                response_time INT,
                ocurred_at TIMESTAMP
            );
        """
        self._execute_query(connection, create_schema)
        self._execute_query(connection, create_table)
