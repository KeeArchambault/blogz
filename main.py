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


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    header = ""
    body = ""
    body_error = ""
    header_error = ""
   
    if request.method == 'POST':
        header = request.form['header']
        body = request.form['body']

        if not header:
            header_error = "Please enter a valid title."
            
        if not body:
            body_error = "Please write a post."

        if not header_error and not body_error:
            new_post = Blog(header, body)
            db.session.add(new_post)
            db.session.commit()
            
            return render_template("/case2")

        return render_template('newpost.html',title="New Post", header = header, body = body, body_error = body_error, header_error = header_error)  
    
    return render_template('newpost.html',title="New Post")

@app.route("/case1")
def case1():

@app.route("/case2")
def case2():    
    ident = Blog.query.filter_by(header=header).id()
    post = Blog.query.filter_by(id = ident).body()

    if

    return render_template("/indiv2.html", id = ident)


@app.route("/blog")
def blog(): 

    posts = Blog.query.all()

    return render_template("blog.html", title="All Posts", posts=posts)



if __name__ == '__main__':
    app.run()