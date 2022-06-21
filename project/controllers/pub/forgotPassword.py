from project import app
from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
from flask_mail import Mail, Message
from project.models.Encryption import Encryption
from cryptography.fernet import Fernet

# untuk ini bisa di setting berdasarkan email client
# untuk push bisa di hapus terlebih dahulu
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)


@app.route("/forget_password" , methods=["GET", "POST"])
def pub_forget_password():
    if request.method == 'GET':
        return render_template('auth/forgetpassword.html')
    else:
        email = request.form['email']
        key = Fernet.generate_key()
        encode = Encryption.encrypt(email.encode(), key)
        link = "http://127.0.0.1:5000/change-password/" + str(key.decode()) + "/email/" + str(encode.decode())

        msg = Message('Komunikasi Publik', sender = 'melektechnology@gmail.com', recipients = ['aditia20.riz@gmail.com'])
        msg.body = "Silahkan klik account ini untuk ganti paswword " + link
        mail.send(msg)
        flash('Silahkan cek email anda')
        return render_template('auth/forgetpassword.html')

@app.route("/change-password/<token>/email/<email>" , methods=["GET"])
def pub_change_password(token, email):

    return "hi"

@app.route("/change-password/new-password" , methods=["POST"])
def pub_new_password():
    return "hi"


