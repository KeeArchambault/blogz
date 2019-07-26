from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(255))
    body = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, header, body, user):
        self.header = header
        self.body = body
        self.user = user
    

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, email, password):
        self.email = email
        self.password = password      

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/signup')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'email' not in session:
        flash("Login Required")
        return redirect('/login')

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    password = request.args.get("password")
    verify= request.args.get("verify")
    email = request.args.get("email")

    exist_error=""
    email_error= ""
    password_error= ""
    verify_error= ""


    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
              return "<h1>User already exists.</h1> <br> <a href='/signup'><h1 style='text-decoration: none;'>Back</h1></a>"

        if not email or len(email) < 3 or len(email) > 20 or " " in email or email.count("@") != 1 or email.count(".")!= 1:
            email_error = "Please provide a valid email."
            email= ""   

        if not password or len(password) < 3 or len(password) > 20 or " " in password:
            password_error = "Please provide a valid password."
            password= ""
            
        if password:
            if verify != password:
                verify_error="Passwords do not match."
                verify= ""
                
        if not password_error and not verify_error and not email_error:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/newpost')
        else:
            return render_template("signup.html", password=password, password_error=password_error, verify=verify, verify_error=verify_error, email=email, email_error=email_error)

        # else:
        #     return "<h1>Duplicate user</h1>"

    return render_template("signup.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist.', 'error')

    return render_template('login.html')


@app.route('/', methods=['POST', 'GET'])
def index():
        users = User.query.all()
        return render_template("index.html", users=users)  

@app.route("/logout")
def logout():  
    del session['email']
    return redirect("/")

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    header = ""
    body = ""
    body_error = ""
    header_error = ""
   
    if request.method == 'POST':
        user = User.query.filter_by(email=session['email']).first()
        header = request.form['header']
        
        body = request.form['body']
        if not header:
            header_error = "Please enter a valid title."
            
        if not body:
            body_error = "Please write a post."

        if not header_error and not body_error:
          
            new_post = Blog(header, body, user)
            db.session.add(new_post)
            db.session.commit()
    
            return redirect("/case2?id="+ str(new_post.id))
           

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

@app.route("/blog",methods=['POST', 'GET'])
def blog(): 
    

    if "id" in request.args:
       post_id= request.args.get('id')
       posts= Blog.query.filter_by(id= post_id).all()
       return render_template('blog.html', posts= posts, id= post_id)

    elif "Uid" in request.args:
       user_id= request.args.get('Uid')
       blogs= Blog.query.filter_by(owner_id= user_id).all()
       return render_template('blog.html', posts= posts, Uid = user_id)

    else:
       posts= Blog.query.order_by(Blog.id.desc()).all()
       return render_template('blog.html', posts = posts)

    # if request.method == 'GET':
    #     user_id= request.args.get('id')
    
    #     return redirect("/single_user?id=user_id")
    
    # posts = Blog.query.all()
    # return render_template("blog.html", posts = posts)    

@app.route("/single_user")
def single_user():
        user_id= request.args.get('id')
        posts = Blog.query.filter_by(user_id=user_id).all()  
        user = User.query.get(user_id)

        return render_template("single_user.html", posts= posts, user = user)  


if __name__ == '__main__':
    app.run()