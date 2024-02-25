import sqlite3

from constants import PRODUCTS_DB_PATH


import random
from constants import PRICE_LOWER_LIMIT, PRICE_UPPER_LIMIT, IN_STOCK_LOWER_LIMIT, IN_STOCK_UPPER_LIMIT, FILE_NAME

import os

# helper function to be used in the reset_inventory function only
def producer_db_setup() -> sqlite3.Cursor:

    db = sqlite3.connect(PRODUCTS_DB_PATH)

    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS products 
                (productid INTEGER PRIMARY KEY AUTOINCREMENT,
                productname TEXT,
                type TEXT, 
                pricetype TEXT, 
                price INTEGER, 
                saldo INTEGER)""")

    return cursor,db


def make_random_orders():
    num_of_prod = 0
    dict_of_products= {}
    with open(FILE_NAME, "r", encoding='utf-8') as f:
        for prod in f.readlines():
            num_of_prod +=1 
            p = prod.strip().strip("(").strip(")").strip("\n").replace(" ","")
            new_prod = tuple(
                p.split(",") + \
                [str(random.randint(PRICE_LOWER_LIMIT,PRICE_UPPER_LIMIT))] + \
                [str(random.randint(IN_STOCK_LOWER_LIMIT,IN_STOCK_UPPER_LIMIT))])
            dict_of_products[num_of_prod] = new_prod
    return dict_of_products




def make_inventory_if_not_exists():
    # if force_reset:
    #     os.remove(PRODUCTS_DB_PATH)

    cursor, db= producer_db_setup()

    if not cursor.execute("SELECT * FROM products").fetchall():
        #reset the txt file
        dict_of_products= make_random_orders()
        for key,value in dict_of_products.items():
            prod = str(value)
            p = prod.strip().strip("(").strip(")").strip("\n").replace(" ","").split(',')
            cursor.execute(f"INSERT INTO products (productname, type, pricetype, price, saldo) VALUES({p[0]},{p[1]},{p[2]},{p[3]},{p[4]})")
            db.commit()
        print("INVENTORY RESET!")
    
    return cursor, db






def inventory_replenishment():
    db = sqlite3.connect(PRODUCTS_DB_PATH)
    cursor = db.cursor()
    dict_of_products= make_random_orders()
    for key,value in dict_of_products.items():
        prod = str(value)
        p = prod.strip().strip("(").strip(")").strip("\n").replace(" ","").split(',')
        sql_query = f"UPDATE products SET saldo = ? WHERE productname = ?"
        values = (int(p[4].strip('\'')), p[0].strip('\''))
        cursor.execute(sql_query,values)
        db.commit()
    print("INVENTORY UPDATED!")
    
    return cursor, db



# if __name__ == "__main__":
#     add_to_inventory()