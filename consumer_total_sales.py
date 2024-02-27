from kafka import KafkaConsumer
import json
from datetime import datetime
from constants import KAFKA_BOOTSTRAP_SERVERS


consumer = KafkaConsumer(
    'Orders',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    # enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    # auto_commit_interval_ms=3000
)
total_sales_count = 0
last_hour_sales_count = 0

#for controlling whether we need to reset the counters
today = datetime.now()

try:
    for message in consumer:
        #print(message)
        # print(json.dumps(message.value, indent=4))
        end_time = datetime.now()

        if end_time.hour != today.hour or end_time.day != today.day or end_time.month != today.month or end_time.year != today.year:
            today = datetime.now()
            last_hour_sales_count = 0
            print('starting to count last hour sales from zero')

        if end_time.day != today.day:
            today = datetime.now()
            total_sales_count = 0
            print('starting to count todays sales from zero')


        #what are we counting? then-now
        start_time_today = datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0)
        start_time_last_hour = datetime(end_time.year, end_time.month, end_time.day, end_time.hour, 0, 0)

        
        order_time = datetime.strptime(message.value['order_time'], '%m/%d/%Y-%H:%M:%S')

        if start_time_today <= order_time <= end_time:
            for order in message.value['order_details']:
                total_sales_count += order['price']*order['quantity']

        if start_time_last_hour <= order_time <= end_time:
            for order in message.value['order_details']:
                last_hour_sales_count += order['price']*order['quantity']


        print(f"Total Sales Today (from {start_time_today} to {end_time}): {total_sales_count}")
        print(f"Sales in Last Hour (from {start_time_last_hour} to {end_time}): {last_hour_sales_count}")
        print('*********')
except KeyboardInterrupt:
    print('Closing')
finally:
    consumer.close()

