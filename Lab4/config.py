import pymysql

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456qwe',
    'db': 'st_exp5',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
op_tip = '请选择>> '
stu_title = ['Sno', 'Sname', 'Ssex', 'Sage', 'Sdept', 'Scholarship']
stu_format = [12, 8, 6, 6, 6, 8]
course_title = ['Cno', 'Cname', 'Cpno', 'Ccredit']
course_format = [8, 14, 8, 6]
sc_title = ['Sno', 'Cno', 'Grade']
sc_format = [12, 8, 8]
sleep_time = 10
