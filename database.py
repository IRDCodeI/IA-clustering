from dotenv import load_dotenv
import MySQLdb
import redis
import os
load_dotenv()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

connection = MySQLdb.connect(
  host= "aws.connect.psdb.cloud",
  user="7rbwlsdfsv5brp8cqxhi",
  passwd= "pscale_pw_YwcNqeLw0sd4e7xUhWHILWC0xk6SWIHn0BNr9cEaP0X",
  db= "rdcode",
  autocommit = True,  
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  }
)