# Kafka fake order producer

Small program that produces fakeorders to a kafka topic "Orders". The topic must be created manualy.

Typical order looks like:
```json
{
    "order_id": 100112,
    "customer_id": 10079,
    "order_details": [
        {
            "product_id": 24,
            "product_name": "CycloneCykel",
            "product_type": "Sportutrustning",
            "price_type": "Styckpris",
            "price": 719,
            "quantity": 10
        },
        {
            "product_id": 46,
            "product_name": "EcoOilOlivolja",
            "product_type": "Matoljor",
            "price_type": "Literpris",
            "price": 1799,
            "quantity": 9
        },
        {
            "product_id": 1,
            "product_name": "ProBookLaptop",
            "product_type": "Elektronik",
            "price_type": "Styckpris",
            "price": 1131,
            "quantity": 5
        },
        {
            "product_id": 53,
            "product_name": "FreshSqueezeCitronsaft",
            "product_type": "Drycker",
            "price_type": "Literpris",
            "price": 1717,
            "quantity": 8
        }
    ],
    "order_time": "02/13/2024-23:10:44"
}
```
## Configuration
- in add_to_price.py you can change the initial products price and stock-level randomization. You need to run the script to generate a new txt-file
- in producer_db_sertup.py you can specify the path for the sqlite database
- in main.py you can dictate the rate of which orders are produced by change the parameters for the gaussian distribution for which the number of orders each second are randomed

### To run
To run you need to 

1. Create the topic "Orders" on your kafka-cluster
2. Create an virtual environment (recommended)
3. Install the requirements:
```bash
pip install -r requirements.txt
```
4. Run main.py either by vs-code or terminal or what ever you please
```bash
py main.py
```
```bash
python main.py
```

### Test Consumer
För att se om det fungerar kan du köra test_consumer.py vilket bara skriver ut ordrarna som kommer in i terminalen
