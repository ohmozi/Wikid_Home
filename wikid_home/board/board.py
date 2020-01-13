from flask import Blueprint, render_template, request, session, redirect
from board import board_dao as db
import os
import time

board_blue = Blueprint('board_blue', __name__)

@board_blue.route('/board_list', defaults={'page': 1})
@board_blue.route('/board_list/<page>')
def board_list(page):
    result = db.get_board_info(page)

    num = result['num'][0]
    range = num % 10
    if range != 0:
        num = int(num / 10)
        num += 1
    else:
        num = int(num / 10)

    data = {}
    data['num'] = num # 끝 페이지 표시하기 위해
    data['boards'] = result['info'] # 가져온 데이터들

    # 마지막 페이지인 경우 남은 개수만큼 보내주기 위해
    if data['num'] == int(page) and range != 0:
        pass
    else:
        range = 10

    html = render_template('board/board_list.html', data=data, i=range, status = 'board_list')
    return html

@board_blue.route('/board_sell_list', defaults={'page': 1})
@board_blue.route('/board_sell_list/<page>')
def board_sell_list(page):
    result = db.get_board_sell_info(page)

    num = result['num'][0]
    range = num % 10
    if range != 0:
        num = int(num / 10)
        num += 1
    else:
        num = int(num / 10)

    data = {}
    data['num'] = num  # 끝 페이지 표시하기 위해
    data['boards'] = result['info']  # 가져온 데이터들

    # 마지막 페이지인 경우 남은 개수만큼 보내주기 위해
    if data['num'] == int(page) and range != 0:
        pass
    else:
        range = 10

    html = render_template('board/board_list.html', data=data, i=range, status = 'board_sell_list')
    return html

@board_blue.route('/board_buy_list', defaults={'page': 1})
@board_blue.route('/board_buy_list/<page>')
def board_buy_list(page):
    result = db.get_board_buy_info(page)

    num = result['num'][0]
    range = num % 10
    if range != 0:
        num = int(num / 10)
        num += 1
    else:
        num = int(num / 10)

    data = {}
    data['num'] = num  # 끝 페이지 표시하기 위해
    data['boards'] = result['info']  # 가져온 데이터들

    # 마지막 페이지인 경우 남은 개수만큼 보내주기 위해
    if data['num'] == int(page) and range != 0:
        pass
    else:
        range = 10

    html = render_template('board/board_list.html', data=data, i=range, status = 'board_buy_list')
    return html



#@board_blue.route('/board_write')
#def board_write():
#    html = render_template('board/board_write.html')
#    return html

@board_blue.route('/board_write1')
def board_write():
    html = render_template('board/board_write1.html')
    return html


@board_blue.route('/board_read1/<content_idx>', defaults={'page' : 1})
@board_blue.route('/board_read1/<content_idx>/<page>')
def board_read(content_idx, page):
    #글 정보를 가져온다.
    data_dic = db.get_content(content_idx)
    data_dic['page'] = page

    html = render_template('board/board_read1.html', data_dic=data_dic, content_idx = int(content_idx))
    return html


@board_blue.route('/board_modify/<content_idx>')
def board_modify(content_idx):
    data_dic = db.get_content(content_idx)

    html = render_template('board/board_modify.html', data_dic = data_dic)
    return html


#@board_blue.route('/board_read/<board_idx>/<content_idx>')
#def board_read(board_idx, content_idx):
    # 글 정보를 가져오기
#    data_idx = board_dao.get_content(content_idx)
#    html = render_template('board/board_read.html', data_dix=data_idx)
#    return html


@board_blue.route('/board_write_pro', methods=['POST'])
def board_write_pro():
    print('write')
    print(request.form)
    # 파라미터 추출
    content_subject = request.form['board_subject']
    print(content_subject)
    content_place = request.form['board_place']
    content_place1 = request.form['board_place1']
    content_place2 = request.form['board_place2']

    if content_place == '광진구':
        content_place = content_place + " " + content_place1
    elif content_place == '송파구':
        content_place = content_place + " " + content_place2

    content_size = request.form['board_size']
    print(content_size)
    content_price = request.form['board_price']
    print(content_price)
    content_start = request.form['board_start']
    print(content_start)
    content_end = request.form['board_end']
    print(content_end)
    content_content = request.form['board_content']
    print(content_content)
    content_writer_idx = session['user_idx']
    #content_board_idx = request.form['board_idx']
    content_status = request.form['board_status']
    print('write2')
    # 파일 데이터를 추출한다.
    if 'board_image' in request.files:
        board_image = request.files['board_image']
        content_file = str(int(time.time())) + board_image.filename

        # os.getcwd()는 main.py의 위치를 알아낼 수 있다.
        a1 = os.getcwd() + '/public/' + content_file
        board_image.save(a1)
    else:
        content_file = None
    print('write3')
    # 저장하기
    content_idx = db.add_content(content_subject, content_status, content_place, content_size,
                                        content_price, content_start, content_end, content_content,
                                        content_writer_idx, content_file)

    # python에서는 문자열과 숫자를 합치지 못한다.
    html = '/board_read1/' + str(content_idx)
    print(f'html: {html}')
    return redirect(html)


# 로그인했는지 확인 (게시판들어갈때 알림창)
@board_blue.route('/board_write_check')
def board_write_check():
    if session['login'] == 'YES' :
        return 'YES'
    else :
        return 'NO'


# 글 삭제 처리
@board_blue.route('/delete_content', methods=['post'])
def delete_content():
    content_idx = request.form['content_idx'],
    pw = request.form['password']

    result = db.delete_content(content_idx, pw)

    if result == 1:
        return 'YES'
    else :
        return 'NO'


@board_blue.route('/board_modify_pro', methods=['post'])
def board_modify_pro() :
    print('write')
    print(request.form)
    # 파라미터 추출
    content_idx = request.form['board_idx']
    content_subject = request.form['board_subject']
    print(content_subject)
    content_place = request.form['board_place']
    content_place1 = request.form['board_place1']
    content_place2 = request.form['board_place2']

    if content_place == '광진구':
        content_place = content_place + " " + content_place1
    elif content_place == '송파구':
        content_place = content_place + " " + content_place2

    content_size = request.form['board_size']
    print(content_size)
    content_price = request.form['board_price']
    print(content_price)
    content_start = request.form['board_start']
    print(content_start)
    content_end = request.form['board_end']
    print(content_end)
    content_content = request.form['board_content']
    print(content_content)
    content_writer_idx = session['user_idx']
    # content_board_idx = request.form['board_idx']
    content_status = request.form['board_status']
    print('write2')
    # 파일 데이터를 추출한다.
    if 'board_image' in request.files:
        board_image = request.files['board_image']
        content_file = str(int(time.time())) + board_image.filename

        # os.getcwd()는 main.py의 위치를 알아낼 수 있다.
        a1 = os.getcwd() + '/public/' + content_file
        board_image.save(a1)
    else:
        content_file = None
    print('write3')
    # 저장하기
    content_idx = db.modify_content(content_idx,content_subject, content_status, content_place, content_size,
                                 content_price, content_start, content_end, content_content,
                                 content_file)

    # python에서는 문자열과 숫자를 합치지 못한다.
    html = '/board_read1/' + str(content_idx)
    print(f'html: {html}')
    return redirect(html)
