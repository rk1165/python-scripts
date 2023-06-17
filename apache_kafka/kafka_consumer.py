import configparser

import kafka

# Kafka Config file
# This config is for Kafka brokers configured with SCRAM credentials
config = configparser.ConfigParser()
config.read('kafka_config.ini')

section = config['consumer']
consumer = kafka.KafkaConsumer(section['topic'],
                               group_id=section['group_id'],
                               bootstrap_servers=section['broker_url'],
                               sasl_mechanism=section['sasl_mechanism'],
                               security_protocol=section['security_protocol'],
                               sasl_plain_username=section['sasl_plain_username'],
                               sasl_plain_password=section['sasl_plain_password'])


def test_connection():
    topics = consumer.topics()

    print(topics)

    if not topics:
        raise RuntimeError()


def consume_message():
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))


consume_message()
