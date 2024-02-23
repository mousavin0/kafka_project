from kafka import KafkaConsumer
import json
from datetime import datetime


consumer = KafkaConsumer(
    'Orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_commit_interval_ms=3000
)
total_orders_count = 0


now_datetime = datetime.now()
try:
    for message in consumer:
        #print(message)
        # print(json.dumps(message.value, indent=4))
        end_time = datetime.now()


        if end_time.day != now_datetime.day:
            now_datetime = datetime.now()
            total_orders_count = 0
            print('starting to count todays sales from zero')


        end_time = datetime.now()
        start_time_today = datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0)
        # end_time - timedelta(hours=1)
        order_time = datetime.strptime(message.value['order_time'], '%m/%d/%Y-%H:%M:%S')
        if start_time_today <= order_time <= end_time:
            total_orders_count += 1



        print(f"Total Orders Today (from {start_time_today} to {end_time}): {total_orders_count}")
        # print(f"end_time: {end_time}")
        # print(f"start_time_today: {start_time_today}")
        # print(f"start_time_last_hour: {start_time_last_hour}")
        # print(f"order_time: {order_time}")
        print('*********')
except KeyboardInterrupt:
    print('Closing')
finally:
    consumer.close()

