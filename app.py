from datetime import datetime

from logging import debug
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        # dueはdatetime型だから変換をする必要がある
        due = datetime.strptime(due, '%Y-%m-%d')

        # 送られてきた情報を各カラムに当てはめている
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        # commitの時点でデータベースに保存をかけている
        db.session.commit()
        return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    # ↓updateの画面を表示させるための記述
    if request.method == 'GET':
        return render_template('update.html', post=post)
    # ↓updateの実際の実行処理
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        # DBへの反映
        db.session.commit()
        return redirect('/')


@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)


@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    # 削除の時に引数としてpostを渡してあげることによって何を消すのかを教えてる
    db.session.delete(post)
    # 削除しましたよの記録をつけている
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
