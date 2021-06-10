#!/bin/bash
./run.py consumer \
    --kafka-bootstrap-servers ${KAFKA_BOOTSTRAP_SERVERS} \
    --kafka-security-protocol ${KAFKA_SECURITY_PROTOCOL} \
    --kafka-ssl-cafile ${KAFKA_SSL_CAFILE} \
    --kafka-ssl-certfile ${KAFKA_SSL_CERTFILE} \
    --kafka-ssl-keyfile ${KAFKA_SSL_KEYFILE} \
    --kafka-topic ${KAFKA_TOPIC} \
    --user ${USER} \
    --password ${PASSWORD} \
    --host ${HOST} \
    --port ${PORT} \
    --database ${DATABASE} \
    --sslmode ${SSLMODE} \
    --sslrootcert ${SSLROOTCERT}
