import pymysql
import json

def save_rank_list():
    conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
    mycursor = conn.cursor()
    sql = 'SELECT mr_content FROM mrqc_result '
    ddd = mycursor.execute(sql)
    datas = mycursor.fetchall()
    for rows in datas:
        json_data =rows[0]
        json_obj = json.loads(str(json_data))
        operations = json_obj['operations']
        if len(operations) > 0:
            a48 = json_obj['a48']
            print(a48+':'+str(operations))

    conn.commit()
    mycursor.close()
    conn.close()


save_rank_list()