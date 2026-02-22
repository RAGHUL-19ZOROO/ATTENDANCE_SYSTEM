import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="3FXbxWqYyErQxC6.root",
        password="izl3JviVOUVvTXuB",
        database="attendance",
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )