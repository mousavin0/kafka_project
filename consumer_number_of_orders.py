from kafka import KafkaConsumer
import json
from datetime import datetime
from constants import KAFKA_BOOTSTRAP_SERVERS

total_orders_count = 0
now_datetime = datetime.now()

consumer = KafkaConsumer(
    'Orders',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest', # read from older times too, not just from now on
    # group_id= 'analytics3', # default is None which means do not commit offset, everytime count from earliest that exists, regardless of previous runs
    # enable_auto_commit=False, #everytime count from earliest that exists, regardless of previous runs, ALTERNATIVELY set group_id equal to None
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    # auto_commit_interval_ms=3000
) 

if __name__ == '__main__':
 
    
    try:
        for message in consumer:
            end_time = datetime.now()


            if end_time.day != now_datetime.day:
                now_datetime = datetime.now()
                total_orders_count = 0
                print('starting to count todays sales from zero')


            end_time = datetime.now()
            start_time_today = datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0)
            order_time = datetime.strptime(message.value['order_time'], '%m/%d/%Y-%H:%M:%S')
            if start_time_today <= order_time <= end_time:
                total_orders_count += 1


            print(f"Total Orders Today (from {start_time_today} to {end_time}): {total_orders_count}")
            print('*********')
    except KeyboardInterrupt:
        print('Closing')
    finally:
        consumer.close()

