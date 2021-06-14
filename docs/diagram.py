from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram(filename="docs/site_checker_architecture"):

    kafka = Kafka("Kafka")
    postgres = Postgresql("PostgreSQL")
    producer = Python("site_checker\nproducer")
    consumer = Python("site_checker\nconsumer")
    website = Server("www.website.com")

    website << producer
    producer >> kafka >> consumer >> postgres

with Diagram(filename="docs/site_checker_config_ini"):

    kafka = Kafka("Kafka")
    postgres = Postgresql("PostgreSQL")
    producer = Python("site_checker\nproducer")
    consumer = Python("site_checker\nconsumer")
    websites = [Server(f"www.website_{n}.com\nTherad-{n}") for n in range(3)]

    websites << producer
    producer >> kafka >> consumer >> postgres


with Diagram(filename="docs/site_checker_cli_parameters"):

    kafka = Kafka("Kafka")
    postgres = Postgresql("PostgreSQL")
    consumer = Python("site_checker\nconsumer")

    producer1 = Docker("site_checker\nproducer_1")
    producer2 = Docker("site_checker\nproducer_2")
    producer3 = Docker("site_checker\nproducer_3")

    website1 = Server("www.website_1.com")
    website2 = Server("www.website_2.com")
    website3 = Server("www.website_3.com")

    website1 << producer1 >> kafka
    website2 << producer2 >> kafka
    website3 << producer3 >> kafka

    kafka >> consumer >> postgres
