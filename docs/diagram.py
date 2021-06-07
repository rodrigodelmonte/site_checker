from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Postgresql
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python

with Diagram(filename="docs/site_checker_architecture"):

    kafka = Kafka()
    postgres = Postgresql()
    producer = Python("producer")
    consumer = Python("consumer")
    website = Server("www.website.com")

    website << producer
    producer >> kafka >> consumer >> postgres
