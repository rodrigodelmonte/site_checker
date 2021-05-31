from setuptools import find_packages, setup

setup(
    name="site_checker",
    version="0.1",
    description="monitors website availability over the network, produces metrics about this and passes these events through an Aiven Kafka instance into an Aiven PostgreSQL database.",  # noqa: E501
    packages=find_packages(where="site_checker"),
    package_dir={"": "site_checker"},
    install_requires=[
        "requests==2.25.1",
    ],
    python_requires="==3.7.9",
)
