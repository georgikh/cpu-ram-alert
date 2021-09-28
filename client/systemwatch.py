from threading import Event
import datetime
import platform
import psutil
import time
import pika
import json

class SystemWatch:
    
    #def check_receive_thread(self):
    #    while(true)
    def __init__(self, interval, cpu_threshold, ram_threshold):
        self.connectToRabbitMQ(host='rabbitmq',port=5672,username='guest',password='guest')
        
        self.stopped = Event()
        
        self.cpu_last_change_time = None
        self.ram_last_change_time = None
        
        self.cpu_last_recorded_percent = None
        self.ram_last_recorded_percent = None
        
        self.cpu_notification_sended_cnt = 0
        self.ram_notification_sended_cnt = 0
        
        self.cpu_threshold_percent = cpu_threshold
        self.ram_threshold_percent = ram_threshold
        self.interval = interval
        self.check_interval = 0.1

        self.ram_last_percents = []
        self.cpu_last_percents = []
        
    def connectToRabbitMQ(self, host,port,username,password):
        print("Connecting to RabbitMQ...")
        credentials = pika.PlainCredentials(username=username, password=password)
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,credentials=credentials))
        except Exception as e:
            print(str(e))
        
        self.channel = self.connection.channel()
        try:
            self.channel.queue_declare(queue='alert')
        except Exception as e:
            print(str(e))
        print("Connected to RabbitMQ")

    def get_cpu_usage(self):
        percentage = psutil.cpu_percent(interval=1)
        return percentage
        
    def get_ram_usage(self):
        return psutil.virtual_memory().percent
        
    def set_interval_secs(self,seconds):
        self.interval = seconds
        
    def set_cpu_threshold(self,cpu_threshold):
        self.cpu_threshold_percent = cpu_threshold
        
    def set_ram_threshold(self,ram_threshold):
        self.ram_threshold_percent = ram_threshold
        
    def check_cpu_usage(self):
        cpu_percent = self.get_cpu_usage()
        if not self.cpu_last_change_time:
            self.cpu_last_change_time = datetime.datetime.now()
        else:
            if cpu_percent >= self.cpu_threshold_percent:
                self.cpu_last_percents.append(cpu_percent)
                diff = (datetime.datetime.now() - self.cpu_last_change_time).total_seconds()
                
                if diff > self.interval and (int(int(diff)/self.interval) > self.cpu_notification_sended_cnt):
                    self.cpu_notification_sended_cnt += 1
                    toSend = f"CPU: percent={cpu_percent},{diff},{self.cpu_notification_sended_cnt}"
                    average_cpu_percent = sum(self.cpu_last_percents)/len(self.cpu_last_percents)
                    toSend = {
                        "alert-type":"cpu",
                        "hostname": platform.node(),
                        "average-percent":average_cpu_percent,
                        "current-percent":cpu_percent,
                        "high-use-time":diff,
                        "interval":self.interval
                    }
                    self.channel.basic_publish(exchange='', routing_key='alert', body=json.dumps(toSend))
                    
            else:
				# Reset CPU monitor timer
                self.cpu_last_change_time = datetime.datetime.now()
                self.cpu_notification_sended_cnt = 0
                self.cpu_last_percents.clear()

                
    def check_ram_usage(self):
        ram_percent = self.get_ram_usage()
        if not self.ram_last_change_time:
            self.ram_last_change_time = datetime.datetime.now()
        else:
            if ram_percent >= self.ram_threshold_percent:
                self.ram_last_percents.append(ram_percent)
                diff = (datetime.datetime.now() - self.ram_last_change_time).total_seconds()
                
                if diff > self.interval and (int(int(diff)/self.interval) > self.ram_notification_sended_cnt):
                    self.ram_notification_sended_cnt += 1
                    #print("RAM: ","percent=",ram_percent,diff,self.ram_notification_sended_cnt)
                    toSend = f"RAM: percent={ram_percent},{diff},{self.ram_notification_sended_cnt}"
                    average_ram_percent = sum(self.ram_last_percents)/len(self.ram_last_percents)
                    toSend = {
                        "alert-type":"ram",
                        "hostname": platform.node(),
                        "average-percent":average_ram_percent,
                        "current-percent":ram_percent,
                        "high-use-time":diff,
                        "interval":self.interval
                    }

                    self.channel.basic_publish(exchange='', routing_key='alert', body=json.dumps(toSend))
            else:
                # Reset RAM monitor timer
                self.ram_last_change_time = datetime.datetime.now()
                self.ram_notification_sended_cnt = 0
                self.ram_last_percents.clear()
   
    def start(self):
        while True:
            time.sleep(self.check_interval)
            self.check_cpu_usage()
            self.check_ram_usage()
