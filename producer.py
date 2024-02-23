from kafka import KafkaProducer
from db_setup import make_inventory_if_not_exists,inventory_replenishment
from sqlite3 import Cursor
import random
import json
import datetime
import time
from constants import MU,SIGMA, MIN_STOCK_LEVEL
# from add_to_price import reset_products_list


inventory_runs_out = False
CUSTOMER_ID = [id for id in range(10000,13000)]

def random_products(
        nr_of_prod_to_random:int, 
        nr_of_prod_in_db:int, 
        cursor:Cursor
        ) -> list[dict]:
    
    list_of_random_products = []
    global inventory_runs_out

    for _ in range(nr_of_prod_to_random):
        rand_prod_id = random.randint(1,nr_of_prod_in_db)
        prod = cursor.execute(f"SELECT * FROM products WHERE productid={rand_prod_id}").fetchone()

        quantity = random.randint(1,10)

        # Change here if you need to control if the inventory runs out
        if prod[5] == MIN_STOCK_LEVEL:
            #will update the whole inventory
            inventory_runs_out = True





        if quantity > prod[5]: quantity = 0

        random_product = {"product_id": prod[0],
                          "product_name": prod[1],
                          "product_type": prod[2],
                          "price_type": prod[3],
                          "price":prod[4],
                          "quantity":quantity}
        
        list_of_random_products.append(random_product)

    return list_of_random_products

def random_order(order_id:int, num_of_prod:int, cursor:Cursor) -> dict:
    customer_id = random.choice(CUSTOMER_ID)
    products = random_products(random.randint(1,5), num_of_prod, cursor)
    order_time = datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")

    new_order = dict(order_id=order_id,
                     customer_id=customer_id,
                     order_details=products,
                     order_time=order_time) 
    return new_order


if __name__ == "__main__":
    

    order_id = 100000

    # cursor = producer_db_setup()
    cursor, db = make_inventory_if_not_exists()

    products = cursor.execute("SELECT * FROM products").fetchall()
    number_of_products_in_database = len(products)

    producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode(encoding='utf-8')
    )
    try:
        while True:
            time.sleep(1)
            random_whole_numb_gaussian = int(random.gauss(mu=MU, sigma=SIGMA))
            for _ in range(random_whole_numb_gaussian):
                order_id += 1
                new_order = random_order(order_id, number_of_products_in_database, cursor)
                producer.send("Orders", new_order)  
                print(new_order)
                if inventory_runs_out:
                    cursor.close()
                    db.close()
                    cursor, db = inventory_replenishment()
                    # cursor.close()
                    inventory_runs_out = False
            producer.flush()

    except KeyboardInterrupt:
        print('Shutting down!')
    
    finally:
        producer.flush()
        producer.close()
        cursor.close()

            


    





