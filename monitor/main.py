# This Python file uses the following encoding: utf-8
import pika
import sys
import os
import json
from db_connector import DB_Controller
import db_models as DB_Models
class Monitor:
    def __init__(self):
        self.db_connector = DB_Controller(DB_Models.engine)

    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        json_data = json.loads(body.decode("utf-8"))
        log = DB_Models.Log(
            hostname=json_data['hostname'],
            alert_type=json_data['alert-type'],
            average_percent=json_data['average-percent'],
            current_percent=json_data['current-percent'],
            high_use_time=json_data['high-use-time'],
            interval=json_data['interval']
        )
        self.db_connector.addLogRecord(log)

    def connect(self):
        credentials = pika.PlainCredentials(username='guest', password='guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq',port=5672,credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue='alert')
        channel.basic_consume(queue='alert', on_message_callback=self.callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

def main():
    monitor = Monitor()
    monitor.connect()
    """

    """

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
