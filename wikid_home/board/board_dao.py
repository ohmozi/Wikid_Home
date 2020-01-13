import pymysql
##########
# 데이터베이스 테이블 전반적으로 보수필요  타입, 구성 안맞음
# 현재 임의로 로컬디비 구성만 해놓은 상태
# blob형이던 int형 없이 varchar로 모두 받는다.
# 따라서 게시판 글이 이상하게 나오는 이유는 fetch해서 읽어오는 순서가 다르기때문
##########

# 데이터 베이스에 접속하는 함수
def get_connection() :
    conn = pymysql.connect(host='127.0.0.1', user='root',
            password='oj950306!@', db='minidb', charset='utf8')

    return conn

# 게시판 이름을 가져오는 함수
def get_board_name(board_idx) :
    # 쿼리문
    sql = 'select board_name from board_table where board_idx=%s'
    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (board_idx))
    # 데이터 추출한다.
    result = cursor.fetchone()
    board_name = result[0];

    conn.close()
    return board_name

# 게시글 추가 함수
def add_content(content_subject, content_status, content_place, content_size,
                content_price, content_start,content_end, content_content,
                content_writer_idx,content_file) :
    # 쿼리문
    sql = '''insert into content_table
             (content_subject, content_status, content_place, content_size,
                content_price, content_start,content_end, content_date, content_content,
                content_writer_idx, content_file)
             values (%s, %s, %s, %s, %s, %s,%s, sysdate(), %s, %s,%s)'''
    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (content_subject, content_status, content_place, content_size,
                    content_price, content_start,content_end, content_content,
                    content_writer_idx,content_file))
    conn.commit()

    # 글 번호를 가져오는 쿼리문
    sql2 = '''select max(content_idx)
              from content_table
              where content_status <> 0'''
    cursor.execute(sql2)
    result2 = cursor.fetchone()
    content_idx = result2[0]
    conn.commit()
    conn.close()
    return content_idx

# 게시글 정보를 반환하는 함수
def get_content(content_idx) :
    # 쿼리문
    sql = '''select a2.user_name, a1.content_subject, a1.content_status, a1.content_place,
                    a1.content_size, a1.content_price, a1.content_start, a1.content_end,
                    a1.content_content, a1.content_file, a1.content_date,
                    a1.content_writer_idx
             from content_table a1, user_table a2
             where a1.content_writer_idx = a2.user_idx
                   and a1.content_idx=%s'''

    # 접속
    conn = get_connection()
    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(sql, (content_idx))
    # 데이터를 가져온다.
    result = cursor.fetchone()
    data_dic = {}
    data_dic['user_name'] = result[0]
    data_dic['content_subject'] = result[1]
    data_dic['content_status'] = result[2]
    data_dic['content_place'] = result[3]
    data_dic['content_size'] = result[4]
    data_dic['content_price'] = result[5]
    data_dic['content_start'] = result[6]
    data_dic['content_end'] = result[7]
    data_dic['content_content'] = result[8]
    data_dic['content_file'] = result[9]
    data_dic['content_date'] = result[10]


    data_dic['content_idx'] = content_idx
    #data_dic['content_board_idx'] = result[4]
    data_dic['content_writer_idx'] = result[11]

    conn.close()

    return data_dic

# 게시글 목록 가져오는 함수
def get_board_info(page) :
    # 전체 개수 쿼리문
    sql = '''SELECT COUNT(*) FROM content_table where content_status <> 0;'''
    sql2 = '''select a1.content_idx, a1.content_subject, a2.user_name, a1.content_date, a1.content_status,
                               a1.content_place, a1.content_size, a1.content_start, a1.content_end, a1.content_price, a1.content_file
                                from content_table a1, user_table a2
                                where a1.content_writer_idx = a2.user_idx
                                      and content_status <> 0
                                order by content_idx desc
                                limit 10 offset %s'''
    offset = (int(page) - 1) * 10;

    result = {}
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(sql)
    result['num'] = cursor.fetchone()
    print(result['num'])
    cursor.execute(sql2, (offset))
    result['info'] = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def get_board_sell_info(page) :
    # 전체 개수 쿼리문
    sql = '''SELECT COUNT(*) FROM content_table where content_status = 2;'''
    sql2 = '''select a1.content_idx, a1.content_subject, a2.user_name, a1.content_date, a1.content_status,
                                   a1.content_place, a1.content_size, a1.content_start, a1.content_end, a1.content_price, a1.content_file
                                    from content_table a1, user_table a2
                                    where a1.content_writer_idx = a2.user_idx
                                          and content_status = 2
                                    order by content_idx desc
                                    limit 10 offset %s'''

    offset = (int(page) - 1) * 10;

    result = {}
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(sql)
    result['num'] = cursor.fetchone()
    print(result['num'])
    cursor.execute(sql2, (offset))
    result['info'] = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def get_board_buy_info(page) :
    # 전체 개수 쿼리문
    sql = '''SELECT COUNT(*) FROM content_table where content_status =1;'''
    sql2 = '''select a1.content_idx, a1.content_subject, a2.user_name, a1.content_date, a1.content_status,
                                     a1.content_place, a1.content_size, a1.content_start, a1.content_end, a1.content_price, a1.content_file
                                      from content_table a1, user_table a2
                                      where a1.content_writer_idx = a2.user_idx
                                            and content_status = 1
                                      order by content_idx desc
                                      limit 10 offset %s'''

    offset = (int(page) - 1) * 10;

    result = {}
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(sql)
    result['num'] = cursor.fetchone()
    print(result['num'])
    cursor.execute(sql2, (offset))
    result['info'] = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# 하단 부 pagenation 구성을 위한 함수
def get_pagenation_info(board_idx, page) :
    # 글 전체의 개수를 가져온다.
    sql = '''select count(*) from content_table
             where content_board_idx=%s and content_status=1'''

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (board_idx))
    result = cursor.fetchone()

    count = result[0]
    # 전체 페이지 개수
    page_count = count // 10
    if page_count % 10 > 0 :
        page_count += 1


    # pagenation 최소 값
    min = ((int(page) - 1) // 10) * 10 + 1
    max = min + 9

    if max > page_count :
        max = page_count

    prev = min - 1
    next = max + 1

    print(page_count, max)

    return page_count, min, max, prev, next

# 글 삭제 처리
def delete_content(content_idx, pw):
    sql = 'update content_table c, user_table u set c.content_status=0 where c.content_writer_idx = u.user_idx AND c.content_idx=%s AND u.user_pw=%s;'

    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute(sql, (int(content_idx[0]), pw))

    conn.commit()
    conn.close()

    return result
# 글 수정 처리
def modify_content(content_idx, content_subject,content_status, content_place, content_size, content_price,
                      content_start, content_end, content_content, file_name) :

    sql = '''update content_table set content_subject=%s, content_place=%s, content_size=%s, content_price=%s,
            content_start=%s, content_end=%s, content_content=%s, content_status=%s '''

    if file_name != None :
        sql += ', content_file=%s '

    sql += 'where content_idx=%s'

    conn = get_connection()

    cursor = conn.cursor()

    if file_name != None :
        cursor.execute(sql, (content_subject, content_place, content_size, content_price, content_start,
                             content_end, content_content, int(content_status), file_name, content_idx))
    else :
        cursor.execute(sql, (content_subject, content_place, content_size, content_price, content_start,
                             content_end, content_content, int(content_status), content_idx))
        #파일을 그대로 냅두기

    conn.commit()
    conn.close()

    return content_idx
