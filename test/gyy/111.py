import pymysql
import json

org_id = '130000200014'
codes_list = []
conn = pymysql.connect(host='192.168.1.35', user='root', password='greAtsoft918!', db='area_report_platform_test_cn')
mycursor = conn.cursor()
# 中医
# reg_arr = 'T81.0|T81.1|T81.3|T81.7|T81.8|T81.9|J98.402|I26.9|I82.807|A40|A41|R96|J96|E89|R57|I80|K91|N99|J95|M80|Z43'.split(
#     "|")
# 西医
reg_arr = 'T81.0|T81.1|T81.3|T81.7|T81.8|T81.9|J98.402|I26.9|I82.805|I82.806|I82.807|A40|A41|R96|J96|E89|R57|I80|K91|J95|S32.4|S72.0|Z43|T88.2|T88.3|T88.5'.split(
    "|")
# print(reg_arr);
def get_ope_codes():
    sql = "SELECT CODE FROM basic_data WHERE TYPE=%s AND sec_type IN (%s,%s) AND  hospital_type=1"
    mycursor.execute(sql, ('OPERATION_CODE', '手术', '介入治疗'))
    datas = mycursor.fetchall()
    for rows in datas:
        codes = rows[0]
        codes_list.append(codes)
    conn.commit()


def get_mr_ope_result():
    sql = 'SELECT date,mr_content,id FROM mrqc_result WHERE LEFT(DATE,7) IN (%s)  AND org_id = %s'
    mycursor.execute(sql, ('2020-05', org_id))
    datas = mycursor.fetchall()
    complication_count = 0
    a48_list = []
    for data_row in datas:
        json_obj = json.loads(str(data_row[1]))
        a48 = json_obj["a48"]
        a16 = ''
        if 'a16' in json_obj:
            a16 = json_obj['a16']
        b11c = ''
        if 'b11c' in json_obj:
            b11c = json_obj['b11c']
        if  b11c != '1' and (a16 == '0' or a16 > '28' or a16 == '-'):
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
                            if not str(diag['c06c']).startswith("O") and not str(diag['c06c']).startswith("P"):
                                if reg in str(diag['c06c']):
                                    diag_flag1 = True
                                if diag_flag1 and 'c08c' in diag:
                                    if str(diag['c08c']) == '4':
                                        diag_flag2 = True
                                if diag_flag1 and diag_flag2:
                                    complication_count += 1
                                    a48_list.append(a48)
                                    break

    print("手术并发症人数 == ", len(set(a48_list)), set(a48_list))
    # print(complication_count)
    print("end~")


get_ope_codes()
get_mr_ope_result()