import pymysql


def get_connection():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='yourpassword', db='yourdb', charset='utf8')

    return conn


def update_user(user_id, user_pw, user_email, user_phone):
    # 쿼리문
    sql = '''update user_table
            set user_pw=%s, user_email=%s, user_phone=%s
            where user_id=%s'''

    # 접속
    conn = get_connection()
    # 쿼리실행
    cursor = conn.cursor()
    cursor.execute(sql, (user_pw, user_email, user_phone, user_id))
    # 접속해제
    conn.commit()
    conn.close()


def add_user(user_name, user_id, user_pw, user_email, user_phone):
    # 쿼리문
    sql = '''insert into user_table
            (user_name, user_id, user_pw, user_email, user_phone)
            values (%s, %s, %s, %s, %s)'''

    # 접속
    conn = get_connection()
    # 쿼리실행
    cursor = conn.cursor()
    cursor.execute(sql, (user_name, user_id, user_pw, user_email, user_phone))
    # 접속해제
    conn.commit()
    conn.close()


# 아이디가 있는지 확인하는 함수
def check_user_id(input_id):
    # 쿼리문
    sql = '''select * from user_table where user_id = %s'''

    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (input_id))
    # 데이터를 가져온다
    result = cursor.fetchone()
    # 가져온 값이 없으면 None이 가져와진다
    conn.close()
    if result == None:
        return 'yes'
    else:
        return 'no'


# 아이디 비밀번호 확인
def check_login(user_id, user_pw):
    # 쿼리문
    sql = '''select user_idx, user_name
             from user_table
             where user_id=%s and user_pw=%s'''
    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, user_pw))
    # 데이터를 가져온다.
    result = cursor.fetchone()

    if result == None:
        conn.close()
        return 'NO'
    else:
        user_idx = result[0]
        conn.close()
        return user_idx


def get_user_info(user_idx):
    # 쿼리문
    sql = '''
        SELECT user_name, user_id, user_email, user_phone
          FROM user_table
         WHERE user_idx = %s;
    '''

    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (user_idx))

    result = cursor.fetchone()

    data_dic = {}
    data_dic['user_name'] = result[0]
    data_dic['user_id'] = result[1]
    data_dic['user_email'] = result[2]
    data_dic['user_phone'] = result[3]

    print(data_dic)

    conn.close()
    if result == None:
        return 'No'
    else:
        return data_dic
