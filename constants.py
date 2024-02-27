# Change here for correct path if you need
PRODUCTS_DB_PATH = "products.db"
# PRODUCTS_FILE = "products.txt"
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

"""If one would want to change the initial condition of the transformation from produkter.txt to products.txt"""
SLEEP_TIME_BEFORE_SIMULATING_NEW_ORDERS = 1

MIN_NUM_OF_PRODUCTS_IN_EACH_ORDER = 1
MAX_NUM_OF_PRODUCTS_IN_EACH_ORDER = 5

MIN_QUANTITY_OF_PRODUCTS_IN_EACH_ORDER = 1
MAX_QUANTITY_OF_PRODUCTS_IN_EACH_ORDER = 10

PRICE_LOWER_LIMIT = 20
PRICE_UPPER_LIMIT = 2000
IN_STOCK_LOWER_LIMIT = 100
IN_STOCK_UPPER_LIMIT = 110
FILE_NAME = "produkter.txt"



# Parameters for a normal distribution
MU = 10 # dictates the avrage amount of orders sent for each second
SIGMA = 1 # dictates the variaton around MU, small number implies more likely MU orders, bigger number the oposit



MIN_STOCK_LEVEL = 20


AUTO_COMMIT_OFFSET_MS = 3000

REPORT_FILES_CREATIMG_TIME = '00:00'
REPORT_FILES_TIME_CHECKING_INTERVAL_SECONDS = 60
REPORT_FILES_WAIT_TIME_BEFORE_RESETTING_COUNTERS_SECONDS = 20