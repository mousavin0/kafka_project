# Change here for correct path if you need
PRODUCTS_DB_PATH = "products.db"
# PRODUCTS_FILE = "products.txt"


"""If one would want to change the initial condition of the transformation from produkter.txt to products.txt"""

PRICE_LOWER_LIMIT = 20
PRICE_UPPER_LIMIT = 2000
IN_STOCK_LOWER_LIMIT = 100
IN_STOCK_UPPER_LIMIT = 110
FILE_NAME = "produkter.txt"



# Parameters for a normal distribution
MU = 0.1 # dictates the avrage amount of orders sent for each second
SIGMA = 1 # dictates the variaton around MU, small number implies more likely MU orders, bigger number the oposit



MIN_STOCK_LEVEL = 30


AUTO_COMMIT_OFFSET_MS = 3000