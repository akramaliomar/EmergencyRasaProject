# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode
#
# def add_user(user_name, user_code):
#
#     try:
#         db = mysql.connector.connect(host='172.18.0.4', user='root', password='alsharif_2022', port=3306,
#                                      database="vital_signs")
#
#
#         # cursor = db.cursor()
#         # sqlQuery = "INSERT INTO user_table(user_name, user_code) VALUES(%s, %s)"
#         # bindData = (user_name, user_code)
#         # cursor.execute(sqlQuery, bindData)
#         # db.commit()
#         # cursor.close()
#         db.close()
#         return "success"
#     except mysql.connector.Error as e:
#         if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             return 'Somethign is wrong with username or password'
#         elif e.errno == errorcode.ER_BAD_DB_ERROR:
#             return 'Database does not exist'
#         else:
#             return str(e)
# import MySQLdb
#
#
# def add_user(user_name, user_code):
#     try:
#         connection = MySQLdb.connect(host="mysqlserver", user="root", passwd="alsharif_2022", db="vital_signs")
#         cursor = connection.cursor()
#         sqlQuery = "INSERT INTO user_table(user_name, user_code) VALUES(%s, %s)"
#         bindData = (user_name, user_code)
#         cursor.execute(sqlQuery, bindData)
#         connection.commit()
#         cursor.close()
#         connection.close()
#         return "success"
#     except MySQLdb.connector.Error as e:
#         if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             return 'Somethign is wrong with username or password'
#         elif e.errno == errorcode.ER_BAD_DB_ERROR:
#             return 'Database does not exist'
#         else:
#             return str(e)
#
#
# def authenticate_user(user_name, user_code):
#     try:
#         connection = MySQLdb.connect(host="mysqlserver", user="root", passwd="alsharif_2022", db="vital_signs")
#         cursor = connection.cursor()
#         sqlQuery = "SELECT COUNT(*) as ucount FROM user_table WHERE user_name = %s AND user_code= %s"
#         bindData = (user_name, user_code)
#         cursor.execute(sqlQuery, bindData)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()
#         return row[0]
#     except MySQLdb.connector.Error as e:
#         if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             return 'Somethign is wrong with username or password'
#         elif e.errno == errorcode.ER_BAD_DB_ERROR:
#             return 'Database does not exist'
#         else:
#             return str(e)
