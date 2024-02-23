from kafka import KafkaConsumer
import json
from datetime import datetime, timedelta
import schedule
import time
from threading import Thread

total_orders_count = 0
total_sales_amount = 0
product_sales = {}

today = datetime.now()



def report_consumer():
    consumer = KafkaConsumer(
        'Orders',
        bootstrap_servers='localhost:9092',  # Update with your Kafka bootstrap server address
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_commit_interval_ms=3000
    )
    try:
        for message in consumer:
            global total_orders_count
            global total_sales_amount
            global product_sales

            global today

            end_time = datetime.now()

            if end_time.day != today.day:
                #wait to make sure the correct count is not lost before written in the report
                time.sleep(20)

                today = datetime.now()
                total_orders_count = 0
                total_sales_amount = 0
                product_sales = {}
                print('starting to count todays sales from zero')

            #what are we counting? then-now
            start_time_today = datetime(end_time.year, end_time.month, end_time.day, 0, 0, 0)
            order_time = datetime.strptime(message.value['order_time'], '%m/%d/%Y-%H:%M:%S')


            if start_time_today <= order_time <= end_time:
                total_orders_count += 1
                for order in message.value['order_details']:
                    total_sales_amount += order['price']*order['quantity']
                    product_id = order['product_id']
                    product_sales[product_id] = product_sales.get(product_id, 0) + 1



        
    except KeyboardInterrupt:
        print('Closing')
    finally:
        consumer.close()

def create_report():
    schedule.every().day.at("17:37").do(generate_daily_report)
    # schedule.every(1).minutes.do(generate_daily_report)
    while True:
        schedule.run_pending()
        time.sleep(10)  # Sleep for 60 seconds between checks

def generate_daily_report():
    global total_orders_count
    global total_sales_amount
    global product_sales

    global today


    today = datetime.now()
    yesterday = today - timedelta(days=1)
    # Write the daily report to a file
    report_filename = f'daily_report_{yesterday.year}-{yesterday.month}-{yesterday.day}.txt'
    with open(report_filename, 'w') as file:
        file.write(f'Daily Report - {yesterday.year}-{yesterday.month}-{yesterday.day}\n')
        file.write(f'Total Orders: {total_orders_count}\n')
        file.write(f'Total Sales Amount: {total_sales_amount}\n')
        file.write('Product Sales:\n')
        for product_id, quantity_sold in product_sales.items():
            file.write(f'Product ID: {product_id}, Quantity Sold: {quantity_sold}\n')
    print(f'Daily report generated: {report_filename}')
    total_orders_count = 0
    total_sales_amount = 0 
    product_sales = {}

if __name__ == '__main__':
    Thread(target = report_consumer).start()
    Thread(target = create_report).start() 