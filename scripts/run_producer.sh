#!/bin/bash
./run.py producer \
    --name ${NAME} \
    --url ${URL} \
    --regex ${REGEX} \
    --kafka-bootstrap-servers ${KAFKA_BOOTSTRAP_SERVERS} \
    --kafka-security-protocol ${KAFKA_SECURITY_PROTOCOL} \
    --kafka-ssl-cafile ${KAFKA_SSL_CAFILE} \
    --kafka-ssl-certfile ${KAFKA_SSL_CERTFILE} \
    --kafka-ssl-keyfile ${KAFKA_SSL_KEYFILE} \
    --pooling-interval ${POOLING_INTERVAL}
