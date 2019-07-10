from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name



posts = []

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        post = request.form['post']
        posts.append(post)

    return render_template('index.html',title="New Post", posts=posts)

@app.route("/blog")
def blog(): 

    return render_template("blog.html", title="Blog")





if __name__ == '__main__':
    app.run()