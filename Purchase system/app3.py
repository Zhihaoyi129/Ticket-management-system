from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 简单的用户存储（通常应该使用数据库）
users = {}
purchases = {}  # 记录每个用户的购买情况

tickets = [
    {"id": 1, "name": "音乐会", "price": 100},
    {"id": 2, "name": "展览", "price": 50},
    {"id": 3, "name": "戏剧", "price": 80}
]

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
        flash('注册成功，请进行实名认证！')
        return redirect(url_for('success'))

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    real_name = request.form['real_name']
    id_card = request.form['id_card']

    user = users.get(username)
    if user and user['real_name'] == real_name and user['id_card'] == id_card:
        user['authenticated'] = True
        flash('实名认证成功！')
        return redirect(url_for('show_tickets'))
    else:
        flash('实名认证失败！请检查您的信息。')
        return redirect(url_for('success'))

@app.route('/tickets')
def show_tickets():
    return render_template('tickets.html', tickets=tickets)

@app.route('/purchase/<int:ticket_id>', methods=['GET', 'POST'])
def purchase(ticket_id):
    if request.method == 'POST':
        username = request.form['username']
        if username not in purchases:
            purchases[username] = ticket_id
            ticket = next((t for t in tickets if t['id'] == ticket_id), None)
            flash(f'购买成功！您已购买 {ticket["name"]} 门票，价格 {ticket["price"]} 元。')
            return redirect(url_for('show_tickets'))
        else:
            flash('您已经购买过一张票！')
            return redirect(url_for('show_tickets'))

    return render_template('purchase.html', ticket=next(t for t in tickets if t['id'] == ticket_id))

if __name__ == '__main__':
    app.run(debug=True)
