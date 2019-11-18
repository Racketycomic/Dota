from app import app,db
from flask import redirect,url_for,render_template
from flask_login import current_user,login_user,logout_user
from app.forms import LoginForm,RegisterForm,FlaskForm,matchbar
from app.models import logo,player_hero,match,hero,player_match
from app.mainstuff import playertable,matchtable


@app.route('/items',methods=['POST','GET'])
def items():
    return render_template('items.html')

@app.route('/heroes',methods=['POST','GET'])
def heroes():
    return render_template('heroes.html')

@app.route('/')
@app.route('/index',methods=['POST','GET'])

def index():
    return render_template('index.html')

@app.route('/login',methods=['POST','GET'])

def login():
    flag1=0
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    print(form.email.data)
    print(form.password.data)

    if form.validate_on_submit():
        print(form.email.data)
        print(form.password.data)
        user=logo.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flag1=1
            return render_template('login.html',form=form,flag1=flag1)
        login_user(user,remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html',form=form,flag1=flag1)

@app.route('/register',methods=['POST','GET'])

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegisterForm()
    print(form.username.data)
    print(form.email.data)
    if form.validate_on_submit():
        print(form.username.data)
        print(form.email.data)
        user=logo(email=form.email.data,id=form.id.data,username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        user1=playertable()
        user1.getinfo(form.id.data)
        return redirect(url_for('login'))

    return render_template("register.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/performance',methods=['GET','POST'])

def performance():
    id=current_user.get_id()
    user=player_hero.query.filter_by(player_id=id).all()
    for u in user:
        print(u.heroname)
    return render_template('performance.html',user=user)


@app.route('/mids',methods=['POST','GET'])

def mids():
    form=matchbar()
    matches=form.matchid.data
    if form.validate_on_submit():
        print("inside validation of form")
        return redirect('midswid/'+str(matches))
    return render_template('newmatch.html',form=form)

@app.route('/midswid/<int:matches>',methods=["POST","GET"])
def midswid(matches):

    users=match.query.filter_by(mid=matches).all()

    print(users)
    print("inside mid before if")
    if len(users)==0:
        print("inside the if loop in mids")
        matchdetail=matchtable()
        matchdetail.getmatch(matches)
        print("hello")
        users=match.query.filter_by(mid=matches).all()
        radiant=player_match.query.filter_by(team='Radiant',matchid=matches).all()
        dire=player_match.query.filter_by(team='Dire',matchid=matches).all()
        return render_template("matchtable.html",users=users,radiant=radiant,dire=dire)


    radiant=player_match.query.filter_by(team='Radiant',matchid=matches).all()
    dire=player_match.query.filter_by(team='Dire',matchid=matches).all()
    print("outside the if loop ready to execute render")
    return render_template('matchtable.html',users=users,radiant=radiant,dire=dire)
