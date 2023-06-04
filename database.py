from dotenv import load_dotenv
import MySQLdb
import os
load_dotenv()

connection = MySQLdb.connect(
  host= "aws.connect.psdb.cloud",
  user="h1ftdmjlonb86ge2ejqn",
  passwd= "pscale_pw_FWj5dK7Yzpdv0XcQPQPGUnnizprgk4n0lr9hDqx09Kh",
  db= "rdcode",
  autocommit = True,  
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  }
)