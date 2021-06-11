from click.testing import CliRunner
from pytest import mark

from site_checker.run import cli


@mark.parametrize(
    "args",
    [
        "producer --config-path example/example.config.ini --dry-run",
        """producer \
                --name test \
                --url http://www.test.org \
                --regex test \
                --kafka-bootstrap-servers 127.0.0.1:28177 \
                --kafka-security-protocol SSL \
                --kafka-ssl-cafile ./config/ca.pem \
                --kafka-ssl-certfile ./config/service.cert \
                --kafka-ssl-keyfile ./config/service.key \
                --pooling-interval 60 \
                --dry-run""",
    ],
)
def test_run_producer_with_config_ini_and_arguments(args):
    runner = CliRunner()

    args = args.split()
    result = runner.invoke(cli, args)

    assert result.exit_code == 0


@mark.parametrize(
    "args",
    [
        "consumer --config-path example/example.config.ini --dry-run",
        """consumer \
            --kafka-bootstrap-servers 127.0.0.1:28177 \
            --kafka-security-protocol SSL \
            --kafka-ssl-cafile ./config/ca.pem \
            --kafka-ssl-certfile ./config/service.cert \
            --kafka-ssl-keyfile ./config/service.key \
            --kafka-topic test_topic \
            --postgres-user user_test \
            --postgres-password pass_test \
            --postgres-host host_test \
            --postgres-port port_test \
            --postgres-database database_test \
            --postgres-sslmode verify-ca \
            --postgres-sslrootcert ca.pem \
            --dry-run
        """,
    ],
)
def test_run_consumer_with_config_ini_and_arguments(args):
    runner = CliRunner()

    args = args.split()
    result = runner.invoke(cli, args)

    assert result.exit_code == 0
