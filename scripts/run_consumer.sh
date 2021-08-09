#!/bin/bash
./run.py consumer \
    --kafka-bootstrap-servers ${KAFKA_BOOTSTRAP_SERVERS} \
    --kafka-security-protocol ${KAFKA_SECURITY_PROTOCOL} \
    --kafka-ssl-cafile ${KAFKA_SSL_CAFILE} \
    --kafka-ssl-certfile ${KAFKA_SSL_CERTFILE} \
    --kafka-ssl-keyfile ${KAFKA_SSL_KEYFILE} \
    --kafka-topic ${KAFKA_TOPIC} \
    --postgres-user ${POSTGRES_USER} \
    --postgres-password ${POSTGRES_PASSWORD} \
    --postgres-host ${POSTGRES_HOST} \
    --postgres-port ${POSTGRES_PORT} \
    --postgres-database ${POSTGRES_DATABASE} \
    --postgres-sslmode ${POSTGRES_SSLMODE} \
    --postgres-sslrootcert ${POSTGRES_SSLROOTCERT}
