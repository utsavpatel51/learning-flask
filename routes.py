from flask import Flask,render_template
from models import db,User
from forms import SignUpForm
from flask import *
app=Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kira@localhost/flaskdb'

db.init_app(app)

app.secret_key="devlopment-key"
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/SignUp",methods=['GET' , 'POST'])
def SignUp():
    form=SignUpForm()
    if(request.method == 'POST'):
        if form.validate()==False:
            return render_template('signup.html',form=form)
        else:
            new_user=User(form.f_name.data,form.l_name.data,form.email.data,form.passwd.data)
            db.session.add(new_user)
            db.session.commit()
            return "sucess!!"
    elif(request.method == 'GET'):
        return render_template('signup.html',form=form)
if __name__ == '__main__':
    app.run(debug=True)
