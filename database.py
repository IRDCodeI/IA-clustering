from dotenv import load_dotenv
import MySQLdb
import os
load_dotenv()

connection = MySQLdb.connect(
  host= "aws.connect.psdb.cloud",
  user="",
  passwd= "",
  db= "rdcode",
  autocommit = True,  
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  }
)