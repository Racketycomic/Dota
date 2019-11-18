from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class logo(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True,index=True)
    email=db.Column(db.String,index=True,unique=True)
    password_hash=db.Column(db.String,index=True)
    username=db.Column(db.String,index=True)
    playertab=db.relationship('player',backref='playerids',lazy='dynamic')
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    @login.user_loader
    def load_user(id):
        return logo.query.get(int(id))

    def __repr__(self):
        return "{} {} {} {}".format(self.id,self.username,self.email,self.password_hash)


class player(db.Model):
    pid=db.Column(db.Integer,db.ForeignKey('logo.id'),primary_key=True)
    no_match=db.Column(db.Integer)
    avg_gpm=db.Column(db.Integer)
    avg_xpm=db.Column(db.Integer)
    no_wins=db.Column(db.Integer)
    no_losses=db.Column(db.Integer)
    avg_kda=db.Column(db.Float)
    mmr=db.Column(db.Integer)

    def __repr__(self):
        return "{} {} {} {} {} {} {} {}".format(self.pid,self.no_match,self.avg_gpm,self.avg_xpm,self.no_wins,self.no_losses,self.avg_kda,self.mmr)


class ana(db.Model):
    hero_id=db.Column(db.Integer,db.ForeignKey('hero.hid'),primary_key=True)
    score=db.Column(db.Float)


class player_hero(db.Model):
    hero_id=db.Column(db.Integer,db.ForeignKey('hero.hid'),primary_key=True)
    score=db.Column(db.Float)
    player_id=db.Column(db.Integer,primary_key=True)
    Performance=db.Column(db.String)
    heroname=db.Column(db.String)


class hero(db.Model):
    hero_name=db.Column(db.String)
    hid=db.Column(db.Integer,primary_key=True)
    tot_match=db.Column(db.Integer)
    wins=db.Column(db.Integer)
    loss=db.Column(db.Integer)
    anatable=db.relationship('ana',backref='heroid',lazy='dynamic')
    player_hero=db.relationship('player_hero',backref="heroid",lazy="dynamic")
    def __repr__(self):
        return "{} {} {} {} {} ".format(self.hero_name,self.hid,self.tot_match,self.wins,self.loss)

class match(db.Model):
    mid=db.Column(db.Integer,primary_key=True)
    tot_kills=db.Column(db.Integer)
    tot_assist=db.Column(db.Integer)
    tot_death=db.Column(db.Integer)
    tot_gold=db.Column(db.Integer)
    tot_xp=db.Column(db.Integer)
    duration=db.Column(db.Float)
    winner=db.Column(db.String)
    pmatchtab=db.relationship('player_match',backref='matchids',lazy='dynamic')

    def __repr__(self):
        return "{} {} {} {} {} {} {} {}".format(self.mid,self.tot_kills,self.tot_assist,self.tot_death,self.tot_gold,self.tot_xp,self.duration,self.winner)

class player_match(db.Model):
    matchid=db.Column(db.Integer,db.ForeignKey('match.mid'),primary_key=True)
    playerid=db.Column(db.Integer,primary_key=True)
    kill_count=db.Column(db.Integer)
    death_count=db.Column(db.Integer)
    assist_count=db.Column(db.Integer)
    kdaratio=db.Column(db.Integer)
    playername=db.Column(db.String)
    xpm=db.Column(db.Integer)
    gpm=db.Column(db.Integer)
    result=db.Column(db.String)
    team=db.Column(db.String)
    heroname=db.Column(db.String)

    def __repr__(self):
        return "{} {} {} {} {} {} {} {} {}".format(self.matchid,self.playerid,self.kill_count,self.death_count,self.assist_count,self.kdaratio,self.playername,self.result,self.heroname)
