from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(255))
    body = db.Column(db.String(255))

    def __init__(self, header, body):
        self.header = header
        self.body = body




posts = []

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        header = request.form['header']
        body = request.form['body']
        new_post = Blog(header, body)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/blog")

    return render_template('newpost.html',title="New Post")

@app.route("/blog")
def blog(): 

    posts = Blog.query.all()

    return render_template("blog.html", title="Blog", posts=posts)



if __name__ == '__main__':
    app.run()