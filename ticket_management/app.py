from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 存储门票信息的列表
tickets = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    category = request.form['category']
    price = request.form['price']
    venue = request.form['venue']
    time = request.form['time']
    content = request.form['content']
    
    # 添加新门票到列表
    tickets.append({
        'category': category,
        'price': price,
        'venue': venue,
        'time': time,
        'content': content
    })
    
    return redirect(url_for('view_tickets'))

@app.route('/tickets')
def view_tickets():
    return render_template('tickets.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
