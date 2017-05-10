from datetime import timedelta
from time import sleep

from celery.task import task
from celery.utils.log import get_task_logger
import pika
import redis

from .utils import get_random_string


logger = get_task_logger(__name__)


def process_queue(ch, method, properties, body):
    sleep(3)
    message = str(body,'utf-8')
    if message == 'error':
        raise Exception()
    print("process_queue, body = %s" % (message, ))
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
    redis_db.rpush('messages', message)
    return True


@task(name="Process Message From Queue")
def consumer():
    logger.info("Start listening queue 'Messages'")
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='main')
    channel.basic_consume(process_queue,
                          queue='main',
                          no_ack=True)

    channel.start_consuming()
    print("Opa Opa, Random message: %s" % (get_random_string()))
    logger.info("Task finished")

