import pymysql
import json

org_id = '130000200008'
codes_list = []
conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
mycursor = conn.cursor()
reg_arr = 'T81.0|T81.1|T81.3|T81.7|T81.8|T81.9|J98.402|I26.9|I82.807|A40|A41|R96|J96|E89|R57|I80|K91|N99|J95|M80|Z43'.split(
    "|")

def get_ope_codes():
    sql = "SELECT CODE FROM basic_data WHERE TYPE=%s AND sec_type IN (%s,%s) AND  hospital_type=2"
    mycursor.execute(sql, ('OPERATION_CODE', '手术', '介入治疗'))
    datas = mycursor.fetchall()
    for rows in datas:
        codes = rows[0]
        codes_list.append(codes)
    conn.commit()


def get_mr_ope_result():
    sql = 'SELECT date,mr_content,id FROM mrqc_result WHERE LEFT(DATE,7) IN (%s)  AND org_id = %s'
    mycursor.execute(sql, ('2021-05', org_id))
    datas = mycursor.fetchall()
    complication_count = 0
    for data_row in datas:
        json_obj = json.loads(str(data_row[1]))
        a16 = json_obj['a16']
        if json_obj['b11c'] != 1 and (a16 == '0' or a16 > 28 or a16 == ''):
            operations = json_obj['operations']
            diagnosis = json_obj['diagnosis']
            flag_ope = False
            for ope in operations:
                if 'c35c' in ope and str(ope['c35c']) in codes_list:
                    flag_ope = True
                    break

            if flag_ope:
                for diag in diagnosis:
                    diag_flag1 = False
                    diag_flag2 = False
                    diag_flag3 = False
                    if 'c06c' in diag:
                        for reg in reg_arr:
                            if reg in str(diag['c06c']):
                                diag_flag1 = True
                                break
                        if not str(diag['c06c']).startswith("O") and not str(diag['c06c']).startswith("P"):
                            diag_flag3 = True

                    if diag_flag1 and 'c08c' in diag:
                        if str(diag['c08c']) == '4':
                            diag_flag2 = True

                    if diag_flag1 and diag_flag2 and diag_flag3:
                        complication_count += 1
                        break
    print(complication_count)
    print("end~")


get_mr_ope_result()