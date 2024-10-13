from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 确保静态文件夹存在，用于存放图片
if not os.path.exists('static/images'):
    os.makedirs('static/images')

@app.route('/add_ticket_image', methods=['GET', 'POST'])
def add_ticket_image():
    if request.method == 'POST':
        ticket_name = request.form['ticket_name']
        image = request.files['image']

        if image:
            image_path = f'static/images/{image.filename}'
            image.save(image_path)  # 将图片保存到静态文件夹
            flash(f'图片上传成功！门票名称：{ticket_name}')
            return redirect(url_for('add_ticket_image'))
        else:
            flash('请上传一张图片！')

    return render_template('add_ticket_image.html')

if __name__ == '__main__':
    app.run(debug=True)
