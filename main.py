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
            post_id = new_post.id
            return redirect("/case2?id="+ str(post_id))

        return render_template('newpost.html',title="New Post", header = header, body = body, body_error = body_error, header_error = header_error)  
    
    return render_template('newpost.html', title="New Post")

@app.route("/case1")
def case1():

    post_id= request.args.get('id')
    post = Blog.query.get(post_id)

    return render_template('indiv.html', post = post)

@app.route("/case2")
def case2():  

    post_id= request.args.get('id')
    post = Blog.query.get(post_id)
    
    return render_template("indiv.html", post = post)


@app.route("/blog")
def blog(): 

    posts = Blog.query.all()

    return render_template("blog.html", title="All Posts", posts=posts)


if __name__ == '__main__':
    app.run()