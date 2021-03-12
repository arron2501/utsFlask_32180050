from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from models import formMember

# pip install flask-WTF
# pip install flask-sqlalchemy
# pip install pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'y0nnf4n5clu8@#$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root@localhost/utsflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, id, name, address, phone, email, created_at, updated_at):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '[%s, %s, %s, %s, %s, %s, %s]' % \
               (self.id, self.name, self.address, self.phone, self.email, self.created_at, self.updated_at)


@app.route('/')
def index():
    form = formMember()
    return render_template('index.html', form=form, data=Member.query.all())


@app.route('/addmember', methods=['GET', 'POST'])
def addmember():
    form = formMember()
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        member = Member(id, name, address, phone, email, created_at, updated_at)
        db.session.add(member)
        db.session.commit()
        flash("Member added successfully!")
        return redirect(url_for('index'))
    else:
        return render_template('index.html', form=form)


@app.route('/editmember', methods=['GET', 'POST'])
def editmember():
    form = formMember()
    member = Member.query.get(request.form.get('id'))
    if request.method == 'POST':
        member.name = form.name.data
        member.address = form.address.data
        member.phone = form.phone.data
        member.email = form.email.data
        member.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        flash("Member updated successfully!")
        return redirect(url_for('index'))
    else:
        return render_template('index.html', form=form)


@app.route('/deletemember/<id>', methods=['GET', 'POST'])
def deletemember(id):
    member = Member.query.filter_by(id=id).first()
    db.session.delete(member)
    db.session.commit()
    flash("Member deleted successfully!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
