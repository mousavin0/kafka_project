# Kafka fake order producer

Small program that produces fakeorders to a kafka topic "Orders". The topic must be created manualy.

### To run
To run you need to 
1. Spin up a kafka container by running 'docker-compose up'
2. Create the topic "Orders" on your kafka-cluster
3. Create an virtual environment (recommended)
4. Install the requirements:
```bash
pip install -r requirements.txt
```
4. Run consumer_update_inventory.py and producer.py to simulate orders and update the inventory database.

5. Run consumer_number_of_orders.py, consumer_total_sales.py and cosumer_reports.py to get daily and hourly order summary and reports.