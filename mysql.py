import pymysql.cursors

db_name=input("请输入数据库名：")
db_password=input("请输入数据库密码：")
print("\n--------------------------------------------\n")
db = pymysql.connect(host='localhost',
                     user='root',
                     password=db_password,
                     database=db_name,)
 
cursor = db.cursor()
 
sql = 'show tables'
cursor.execute(sql)
 
rest=cursor.fetchall()
for i in rest:
    print('表名：',i[0])
    for j in i:
        cursor.execute("SELECT GROUP_CONCAT(COLUMN_NAME SEPARATOR ',') FROM information_schema.COLUMNS WHERE TABLE_NAME='{0}' AND TABLE_SCHEMA='{1}';".format(i[0], db_name))
        col_name=cursor.fetchall()[0][0].split(",")
        print('列名：',col_name)
        cardinality_rate=[]
        for k in col_name:
            cursor.execute('SELECT COUNT(DISTINCT {}) / COUNT(*) AS cardinality_rate FROM {};'.format(k,i[0]))
            cardin=cursor.fetchall()[0][0]
            if cardin==None:
                cardinality_rate.append("null")
            else:
                cardinality_rate.append(float(cardin))
        print('基数比：',cardinality_rate)
        print('基数比最大值：',max(cardinality_rate))
        print()
 
db.close()
