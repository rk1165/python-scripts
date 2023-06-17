import boto3

sqs_client = boto3.client('sqs')


def get_message_count(queue):
    """
    Get message count in a queue
    :param queue: name of the queue
    :return: count of messages in the queue
    """
    queue_url = sqs_client.get_queue_url(QueueName=queue).get('QueueUrl')
    queue_attributes = sqs_client.get_queue_attributes(QueueUrl=queue_url,
                                                       AttributeNames=['ApproximateNumberOfMessages'])
    msg_count = int(queue_attributes['Attributes']['ApproximateNumberOfMessages'])
    if msg_count > 0:
        print("{0: <52} : {1: <4}".format(queue, str(msg_count)))
    return msg_count


def get_message(queue):
    """
    Retrieves one message from the queue
    :param queue: name of the queue from which to retrieve message
    :return: a message from the queue
    """
    queue_url = sqs_client.get_queue_url(QueueName=queue).get('QueueUrl')
    response = sqs_client.receive_message(QueueUrl=queue_url, MessageAttributeNames=["All"], VisibilityTimeout=600,
                                          WaitTimeSeconds=1)
    print(response)
    return response
    # sqs_client.change_message_visibility(QueueUrl=queue_url, ReceiptHandle=receipt_handle,
    #                                      VisibilityTimeout=3600)


def send_message(queue, message, attributes):
    """
    Sends a given message to a queue with attributes
    :param queue: name of the queue to which to send message
    :param message: to send
    :param attributes: additional attributes associated with the message
    :return: nothing
    """
    sent = sqs_client.send_message(QueueUrl=queue, MessageBody=message, MessageAttribuets=attributes)
    print(sent['MessageId'])


def delete_message(queue, receipt_handle):
    """
    Deletes a message from a queue
    :param queue: name of the queue from which to delete message
    :param receipt_handle: parameter to identify the message
    :return: nothing
    """
    sqs_client.delete_message(QueueUrl=queue, ReceiptHandle=receipt_handle)
