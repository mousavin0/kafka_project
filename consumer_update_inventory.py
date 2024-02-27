from kafka import KafkaConsumer
import json
from constants import  MIN_STOCK_LEVEL,AUTO_COMMIT_OFFSET_MS,KAFKA_BOOTSTRAP_SERVERS
from db_setup import make_inventory_if_not_exists

import time



def update_product_balance(productid,quantity,cursor,db):
    
    
    sql_query = "SELECT saldo FROM products WHERE productid = ?"
    values = (productid, )
    quantity_old = cursor.execute(sql_query,values).fetchone()[0]
    print(f'Quantity for product {productid} before the order : {quantity_old}')

    if quantity_old - quantity < 0:
        print("Something went wrong! HANDLE CUNCURRENT ORDERS!")

    else:
        sql_query = "UPDATE products SET saldo = ? WHERE productid = ?"
        values = (quantity_old - quantity , productid)
        cursor.execute(sql_query,values)
        
        #remove this
        sql_query = "SELECT saldo FROM products WHERE productid = ?"
        values = (productid, )
        quantity_new = cursor.execute(sql_query,values).fetchone()[0]
        print(f'Quantity for product {productid} after the order : {quantity_new}')

        db.commit()
    

if __name__ == "__main__":
    # print(update_product_balance(1,1))
    cursor,db = make_inventory_if_not_exists()
    consumer = KafkaConsumer(
        'Orders',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest', 
        group_id= 'inventory_update', #if groupid is none, offset will not get updated. meaning we go through same orders again for a second run of the code
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_commit_interval_ms = AUTO_COMMIT_OFFSET_MS
    )
    try:
        for message in consumer:
            # print(message)
            # print(json.dumps(message.value, indent=4))


            for order in message.value['order_details']:
                product_id = order['product_id']
                quantity = order['quantity']
                update_product_balance(product_id,quantity,cursor,db)
    except KeyboardInterrupt:
        print('Closing')
        time.sleep(AUTO_COMMIT_OFFSET_MS/1000 + 0.5) # to make sure offset is commited and we will not handle an order for the second time in the next run
    finally:
        consumer.close()
        cursor.close()



