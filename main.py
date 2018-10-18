from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:tigasep88@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'tigasep88'

# persistent class -- class that can be stored in the database
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    posts = Blog.query.all()
    return render_template('blog.html', title = "Build a Blog", posts = posts)

@app.route('/newpost', methods = ['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        error_t = ''
        error_b = ''
        # validate
        if not blog_title:
            error_t = 'Please fill in the title'
        if not blog_body:
            error_b = 'Please fill in the body'
        if not error_t and not error_b:
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('newpost.html',
                title = 'Build a Blog',
                error_t = error_t,
                error_b = error_b)
    return render_template('newpost.html', title = 'Build a Blog')

if __name__ == '__main__':
    app.run()