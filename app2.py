from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 简单的用户存储（通常应该使用数据库）
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        real_name = request.form['real_name']
        id_card = request.form['id_card']

        # 简单的验证
        if username in users:
            flash('用户已存在！')
            return redirect(url_for('register'))

        # 存储用户信息
        users[username] = {
            'password': generate_password_hash(password),
            'real_name': real_name,
            'id_card': id_card
        }
        flash('注册成功，请进行实名认证！')
        return redirect(url_for('success'))

    return render_template('register.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
