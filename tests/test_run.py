from click.testing import CliRunner

from site_checker.run import cli


def test_run_producer_with_config_ini():
    runner = CliRunner()

    args = "producer --config-path example/config.ini --dry-run".split()
    result = runner.invoke(cli, args)

    assert result.exit_code == 0


def test_run_producer_with_arguments():
    runner = CliRunner()

    args = """./site_checker/run.py producer \
        --name test \
        --url http://www.test.org \
        --regex test \
        --kafka-bootstrap-servers 127.0.0.1:28177 \
        --kafka-security-protocol SSL \
        --kafka-ssl-cafile ./config/ca.pem \
        --kafka-ssl-certfile ./config/service.cert \
        --kafka-ssl-keyfile ./config/service.key \
        --pooling-interval 60 \
        --dry-run"""
    result = runner.invoke(cli, args)

    assert result.exit_code == 0
