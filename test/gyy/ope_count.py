import pymysql
import json

codes_list = []
conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
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
    sql = 'SELECT date,mr_content FROM mrqc_result WHERE LEFT(DATE,7) IN (%s)  AND org_id = %s'
    mycursor.execute(sql, ('2021-01', '130000200008'))
    datas = mycursor.fetchall()
    count_ope = 0
    for rows in datas:
        json_data = rows[1]
        json_obj = json.loads(str(json_data))
        operations = json_obj['operations']
        b11c = json_obj['b11c']
        if len(operations)> 0 and b11c != 1:
            for ope in operations:
                if ('c35c' in ope):
                    if str(ope['c35c']) in codes_list:
                        count_ope = count_ope + 1
    print(count_ope)
    conn.commit()
    mycursor.close()
    conn.close()
    print("end~")


get_ope_codes()
get_mr_ope_result()
