from datetime import datetime
import random
 
#year = random.randint(1950, 2000)
#month = random.randint(1, 12)
year = 2017
month = 12
day = random.randint(1, 28)
random_timestamps = datetime(year, month, day)

print(random_timestamps)
