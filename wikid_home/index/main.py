from flask import Blueprint, render_template, session

main_blue = Blueprint('main_blue', __name__)

@main_blue.route('/start')      # 로그인세션을 위한 첫 시작에 다른 경로로 접근 - 변경필요
def main():
    session['login' ]='NO'
    html = render_template('index.html')
    return html

@main_blue.route('/')
def index():
    img = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'img4.jpg']

    html = render_template('index.html', data_img=img)
    return html

@main_blue.route('/FAQ')
def faq():
    img = ['faq1.jpg', 'faq2.jpg', 'faq3.jpg', 'faq4.jpg']

    html = render_template('FAQ.html', data_img = img)
    return html