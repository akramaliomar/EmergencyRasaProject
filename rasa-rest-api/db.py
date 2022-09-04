import os
import pymysql
# import pymysql.cursors
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user,
                                   password=db_password,
                                   unix_socket=unix_socket,
                                   db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
    except pymysql.MySQLError as e:
        return e
    return conn


def db_get_vs():
    conn = open_connection()
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute('SELECT * FROM vital_sign_table ORDER BY tb_vital_sign_id DESC LIMIT 1;')
            vital_signs = cursor.fetchall()
            if result > 0:
                get_vital_signs = jsonify(vital_signs)
            else:
                get_vital_signs = "No vital signs in DB"
            return get_vital_signs

def db_aggregated_vs():
    conn = open_connection()
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute("SELECT MAX(hr) as maxhr, MAX(spo2) AS maxspo2,MAX(resp) AS maxresp, MAX(tempr) as maxtempr, MIN(hr) as minhr, MIN(spo2) AS minspo2, MIN(resp) AS minresp, MIN(tempr) as mintempr, CONVERT(AVG(hr),CHAR) as avghr,CONVERT(AVG(spo2),CHAR) AS avgspo2, CONVERT(AVG(resp),CHAR) AS avgresp, CONVERT(AVG(tempr),CHAR) as avgtempr FROM vital_sign_table;")
            vital_signs = cursor.fetchall()
            if result > 0:
                get_vital_signs = jsonify(vital_signs)
            else:
                get_vital_signs = "No vital signs in DB"
            return get_vital_signs
def db_get_rand_vs():
    conn = open_connection()
    with conn:
        with conn.cursor() as cursor:
            result = cursor.execute("SELECT *  FROM vital_sign_table ORDER BY RAND ( ) LIMIT 1  ")
            vital_signs = cursor.fetchall()
            return vital_signs[0]["output"]


def db_add_vs(v_signs):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO vital_sign_table(timestamp, hr, spo2, resp, tempr) VALUES(%s, %s, %s, %s, %s)',
                       (v_signs["timestamp"], v_signs["hr"], v_signs["spo2"], v_signs["resp"], v_signs["tempr"]))
    conn.commit()
    conn.close()
