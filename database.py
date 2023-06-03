from dotenv import load_dotenv
import MySQLdb
import os
load_dotenv()

connection = MySQLdb.connect(
  host= "aws.connect.psdb.cloud",
  user="u0nw9hd9elv9i3csjc7m",
  passwd= "pscale_pw_PkAe48lOi72rK3OSjki5uQEdlmIYVKO6H4ygekOmG5P",
  db= "rdcode",
  autocommit = True,  
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    "ca": "/etc/ssl/certs/ca-certificates.crt"
  }
)