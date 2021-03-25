from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Mengimport file model
from models import formPatient

# Plugin flask yang harus terinstall agar aplikasi ini dapat berjalan
# [1] pip install flask-WTF
# [2] pip install flask-sqlalchemy
# [3] pip install pymysql

# Konfigurasi aplikasi
app = Flask(__name__)
app.config['SECRET_KEY'] = 'y0nnf4n5clu8@#$%^&*'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://root@localhost/utsflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# Inisialisasi database, menggunakan SQLAlchemy
class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    complaint = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)

    def __init__(self, id, name, address, phone, email, complaint, created_at, updated_at):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.complaint = complaint
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '[%s, %s, %s, %s, %s, %s, %s, %s]' % \
               (self.id, self.name, self.address, self.phone, self.email, self.complaint, self.created_at, self.updated_at)


# Route ke halaman utama, dan mengirimkan data dari database ke html
@app.route('/')
def index():
    form = formPatient()
    return render_template('index.html', form=form, data=Patients.query.all())


# Route untuk menambah pasien baru
@app.route('/addpatient', methods=['GET', 'POST'])
def addpatient():
    form = formPatient()
    # Apabila methodnya POST, maka aplikasi akan mengirimkan data ke database
    if request.method == 'POST':
        name = form.name.data
        address = form.address.data
        phone = form.phone.data
        email = form.email.data
        complaint = form.complaint.data
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        patient = Patients(id, name, address, phone, email, complaint, created_at, updated_at)
        db.session.add(patient)
        db.session.commit()
        # Pesan flash ketika pasien berhasil ditambahkan
        flash("Patient added successfully!")
        # Dan akan redirect ke halaman utama
        return redirect(url_for('index'))
    # Apabila methodnya GET, maka aplikasi akan menampilkan halaman utama
    else:
        return render_template('index.html', form=form)


# Route untuk mengedit data pasien
@app.route('/editpatient', methods=['GET', 'POST'])
def editpatient():
    form = formPatient()
    # Mengambil data berdasarkan id pasien yang akan diedit
    patient = Patients.query.get(request.form.get('id'))
    # Apabila methodnya POST, maka aplikasi akan mengirimkan data ke database
    if request.method == 'POST':
        patient.name = form.name.data
        patient.address = form.address.data
        patient.phone = form.phone.data
        patient.email = form.email.data
        patient.complaint = form.complaint.data
        patient.updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        # Pesan flash ketika pasien berhasil diubah
        flash("Patient updated successfully!")
        # Dan akan redirect ke halaman utama
        return redirect(url_for('index'))
    # Apabila methodnya GET, maka aplikasi akan menampilkan halaman utama
    else:
        return render_template('index.html', form=form)


# Route untuk menghapus data pasien
@app.route('/deletepatient/<id>', methods=['GET', 'POST'])
def deletepatient(id):
    # Memilih data yang akan dihapus berdasarkan idnya
    patient = Patients.query.filter_by(id=id).first()
    # Menghapus data berdasarkan idnya
    db.session.delete(patient)
    db.session.commit()
    # Pesan flash ketika pasien berhasil dihapus
    flash("Patient deleted successfully!")
    # Dan akan redirect ke halaman utama
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
