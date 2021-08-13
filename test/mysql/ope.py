import pymysql
import json

org_id = '130000200012'
codes_list = []
conn = pymysql.connect(host='192.168.8.8', user='root', password='greAtsoft918!', db='area_report_platform_test_cn_yz')
mycursor = conn.cursor()


def get_ope_codes():
    sql = "SELECT CODE FROM basic_data WHERE TYPE=%s AND sec_type IN (%s,%s)"
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
    a48_count = 0
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
            a48_count += 1
    conn.commit()
    mycursor.close()
    conn.close()
    print(a48_count)
    print("end~")


get_ope_codes()
get_mr_ope_result()
