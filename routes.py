from flask import Flask,render_template,session,redirect,request,url_for
from models import db,User,Place
from forms import SignUpForm,LogInForm,AddressForm
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
    if 'email' in session:
        return redirect(url_for('home'))
    form=SignUpForm()
    if(request.method == 'POST'):
        if form.validate()==False:
            return render_template('signup.html',form=form)
        else:
            new_user=User(form.f_name.data,form.l_name.data,form.email.data,form.passwd.data)
            db.session.add(new_user)
            db.session.commit()
            session['email']=new_user.email
            return redirect(url_for('home'))
    elif(request.method == 'GET'):
        return render_template('signup.html',form=form)

@app.route("/home",methods=['GET' , 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('LogIn'))
    #return render_template('home.html',email=session['email'])
    form=AddressForm()
    places=[]
    my_coor = (37.4221,-122.0844)
    if request.method == 'POST':
        if(form.validate==False):
            return render_template('home.html',form=form)
        else:
            #get address
            address=form.address.data
            #use address with api
            p=Place()
            my_coor=p.address_to_lat_lon(address)
            places=p.query(address)
            #return result
            return render_template('home.html',form=form,my_coor=my_coor,places=places)
    elif request.method == 'GET':
        return render_template('home.html',form=form,my_coor=my_coor,places=places)

@app.route("/LogIn",methods=['GET' , 'POST'])
def LogIn():
    if 'email' in session:
        return redirect(url_for('home'))
    form=LogInForm()
    if(request.method =='POST'):
        if(form.validate==False):
            return render_template('login.html',form=form)
        else:
            email=form.email.data
            passwd=form.passwd.data
            user=User.query.filter_by(email=email).first()
            if user is not None and user.check_passwd(passwd):
                session['email']=form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('LogIn'))
    elif(request.method == 'GET'):
        return render_template('login.html',form=form)
@app.route("/logout")
def LogOut():
    session.pop('email',None)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
