from configs import kafka_config, postgres_config, websites_configs


def test_kafka_config(config_path):

    config = kafka_config(config_path)
    assert config.bootstrap_servers == "<CHANGEME>"
    assert config.security_protocol == "SSL"


def test_website_configs(config_path):

    websites = websites_configs(config_path)
    website_names = [website.name for website in websites]

    assert type(websites) == list
    assert len(websites) == 3
    assert website_names == ["python", "cncf", "apache"]
    assert websites[0].url == "http://python.org/"


def test_postgres_config(config_path):

    config = postgres_config(config_path)

    assert config.user == "<CHANGEME>"
    assert config.password == "<CHANGEME>"
