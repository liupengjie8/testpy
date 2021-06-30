import datetime
import time

import pymysql
import json

org_id = '130000200008'
codes_list = []
conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
mycursor = conn.cursor()

def get_ope_codes():
    sql = "SELECT CODE FROM basic_data WHERE TYPE=%s AND sec_type IN (%s,%s) AND  hospital_type=2"
    mycursor.execute(sql, ('OPERATION_CODE', '手术', '介入治疗'))
    datas = mycursor.fetchall()
    for rows in datas:
        codes = rows[0]
        codes_list.append(codes)
    conn.commit()


def get_daytime_dicts():
    sql = "SELECT icd_9_cm3,icd_10_code FROM cdo"
    mycursor.execute(sql)
    datas = mycursor.fetchall()
    return datas

def get_minutes_diff(str1,str2):
    ta = time.strptime(str2, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(str1, "%Y-%m-%d %H:%M:%S")
    y, m, d, H, M, S = ta[0:6]
    dataTimea = datetime.datetime(y, m, d, H, M, S)
    y, m, d, H, M, S = tb[0:6]
    dataTimeb = datetime.datetime(y, m, d, H, M, S)
    secondsDiff = (dataTimea - dataTimeb).total_seconds()
    return secondsDiff/60


def get_mr_ope_result():
    sql = 'SELECT date,mr_content,id FROM mrqc_result WHERE LEFT(DATE,7) IN (%s)  AND org_id = %s'
    mycursor.execute(sql, ('2021-05', org_id))
    datas = mycursor.fetchall()
    day_time_ope =get_daytime_dicts()
    day_ope_count = 0
    for data_row in datas:
        json_obj = json.loads(str(data_row[1]))
        if str(data_row[2]) == '0404b12f-41a5-47bf-91cf-f7a557fd59d4':
            minutes_idff = get_minutes_diff(json_obj['b12'], json_obj['b15'])
            if json_obj['b11c'] != 1 and minutes_idff <= 2880:
                for dic_row in day_time_ope:
                    operations = json_obj['operations']
                    diagnosis = json_obj['diagnosis']
                    flag_ope = False
                    for ope in operations:
                        # a = 'c35c' in ope
                        # b = str(ope['c35c']) in codes_list
                        # c = str(ope['c35c']).startswith(dic_row[0])
                        if 'c35c' in ope and str(ope['c35c']) in codes_list and str(ope['c35c']).startswith(dic_row[0]):
                            flag_ope = True
                            break

                    if flag_ope:
                        flag_diag = False
                        for diag in diagnosis:
                            if 'c06c' in diag and str(diag['c06c']).startswith(dic_row[1]):
                                flag_diag = True
                                break

                        if flag_diag and flag_ope:
                            day_ope_count+=1
    print(day_ope_count)
    print("end~")


get_ope_codes()
get_mr_ope_result()
