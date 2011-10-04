# 
#  __init__.py
#  SEDMachine
#  
#  Created by Alexander Rudy on 2011-10-04.
#  Copyright 2011 Alexander Rudy. All rights reserved.
# 

import logging
import time
import sys

logging.basicConfig(filename="Logs/"+__name__+"-"+time.strftime("%Y-%m-%d")+".log",format="%(asctime)s : %(levelname)-8s : %(name)-20s : %(message)s",datefmt="%Y-%m-%d-%H:%M:%S",level=logging.DEBUG,filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)