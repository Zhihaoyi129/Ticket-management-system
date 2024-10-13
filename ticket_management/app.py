from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 简单的用户存储（通常应该使用数据库）
users = {}
tickets = []

# 确保静态文件夹存在
if not os.path.exists('static/images'):
    os.makedirs('static/images')

@app.route('/')
def home():
    return redirect(url_for('login'))

# 登录功能
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('登录成功！')
            return redirect(url_for('add_ticket'))
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))

    return render_template('login.html')

# 用户注册及身份录入功能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        real_name = request.form['real_name']
        id_card = request.form['id_card']

        if username in users:
            flash('用户已存在！')
            return redirect(url_for('register'))

        users[username] = {
            'password': generate_password_hash(password),
            'real_name': real_name,
            'id_card': id_card,
            'authenticated': False
        }
        flash('注册成功，请登录！')
        return redirect(url_for('login'))

    return render_template('register.html')

# 添加门票信息
@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
    if 'username' not in session:
        flash('请先登录！')
        return redirect(url_for('login'))

    if request.method == 'POST':
        ticket_name = request.form['ticket_name']
        price = request.form['price']
        location = request.form['location']
        main_actor = request.form['main_actor']
        date = request.form['date']
        image = request.files['image']
        image_path = f'static/images/{image.filename}'
        image.save(image_path)

        tickets.append({
            'name': ticket_name,
            'price': price,
            'location': location,
            'main_actor': main_actor,
            'date': date,
            'image': image_path
        })
        flash('门票添加成功！')
        return redirect(url_for('show_tickets'))

    return render_template('add_ticket.html')

# 展示门票列表
@app.route('/tickets')
def show_tickets():
    return render_template('tickets.html', tickets=tickets)

# 购买门票
@app.route('/purchase/<int:ticket_index>', methods=['GET', 'POST'])
def purchase(ticket_index):
    if 'username' not in session:
        flash('请先登录！')
        return redirect(url_for('login'))

    ticket = tickets[ticket_index]
    if request.method == 'POST':
        username = session['username']
        flash(f'购买成功！您已购买 {ticket["name"]} 门票，价格 {ticket["price"]} 元。')
        return redirect(url_for('show_tickets'))

    return render_template('purchase.html', ticket=ticket)

if __name__ == '__main__':
    app.run(debug=True)
