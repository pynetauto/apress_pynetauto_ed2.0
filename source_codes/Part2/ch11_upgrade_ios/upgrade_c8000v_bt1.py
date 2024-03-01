import socket  # For socket networking
import os  # For Python Server OS
import time  # Python time module
import pandas as pd  # Pandas for reading data into a data frame
import re  # Python regular expression module
from getpass import getpass  # For uid & password collection
import os.path  # For Python Server OS directory
import hashlib  # For MD5 checks
from netmiko import ConnectHandler, SCPConn  # netmiko SSH connection and SCP file transfer
from netmiko import NetMikoTimeoutException  # To catch netmiko timeout exceptions
import difflib  # For analyzing two files and differences

t1 = time.mktime(time.localtime()) # Timer(t1) start to measure script running time

# Add your ten applications here!

tt = time.mktime(time.localtime()) - t1
print("Total wait time : {0} seconds".format(tt)) # Timer finish to show total time (tt)

