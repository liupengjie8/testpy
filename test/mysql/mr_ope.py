import pymysql
import json

org_id = '130000200016'
codes_list = []
conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
mycursor = conn.cursor()
sql = "delete from mr_ope_rec"
mycursor.execute(sql)
conn.commit()


def get_ope_codes():
    sql = "SELECT CODE FROM basic_data WHERE TYPE=%s AND sec_type IN (%s,%s) AND  hospital_type=2"
    mycursor.execute(sql, ('OPERATION_CODE', '手术', '介入治疗'))
    datas = mycursor.fetchall()
    for rows in datas:
        codes = rows[0]
        codes_list.append(codes)
    conn.commit()


def get_mr_ope_result():
    sql = 'SELECT date,mr_content FROM mrqc_result_first WHERE LEFT(DATE,7) IN (%s)  AND org_id = %s'
    ddd = mycursor.execute(sql, ('2021-02', org_id))
    datas = mycursor.fetchall()
    for rows in datas:
        date = rows[0]
        json_obj = json.loads(str(rows[1]))
        operations = json_obj['operations']
        if len(operations) > 0:
            a48 = json_obj['a48']
            count_ope = 0
            opes = []
            for ope in operations:
                if 'c35c' in ope:
                    if str(ope['c35c']) in codes_list:
                        count_ope = count_ope + 1
                        opes.append(str(ope['c35c']))
            if count_ope > 0:
                sql_insert = 'INSERT INTO area_report_platform_test_cn.mr_ope_rec (org_id, a48, date, ope_count, opes) VALUES(%s, %s, %s, %s, %s)'
                mycursor.execute(sql_insert, (org_id, str(a48), date, str(count_ope), str(opes)))
    conn.commit()
    mycursor.close()
    conn.close()
    print("end~")


get_ope_codes()
get_mr_ope_result()
