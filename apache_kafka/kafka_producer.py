import configparser

import kafka
from kafka.errors import KafkaError

# Kafka Config file
# This config is for Kafka brokers configured with SCRAM credentials
config = configparser.ConfigParser()
config.read('kafka_config.ini')

section = config['producer']


def init_kafka_producer():
    return kafka.KafkaProducer(bootstrap_servers=[section['broker_url']],
                               sasl_mechanism=section['sasl_mechanism'],
                               security_protocol=section['security_protocol'],
                               sasl_plain_username=section['sasl_plain_username'],
                               sasl_plain_password=section['sasl_plain_password'],
                               value_serializer=str.encode)


def post_message(message):
    future = producer.send(topic=section['topic'], value=message)
    try:
        record_metadata = future.get(timeout=10)
        print(f"Successfully posted message to Kafka with partition {record_metadata.partition}"
              f" and offset {record_metadata.offset}")
    except KafkaError:
        print(f"Failed to post to Kafka")


producer = init_kafka_producer()
post_message("Hello Kafka")