from project import app
from flask import Flask
from flask import render_template, redirect, url_for, request, session, flash
from flask_mail import Mail, Message
from project.models.Encryption import Encryption
from cryptography.fernet import Fernet

# untuk ini bisa di setting berdasarkan email client
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'melektechnology@gmail.com'
app.config['MAIL_PASSWORD'] = 'kmqcpmizgyrrvfou'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)


@app.route("/forget_password" , methods=["GET", "POST"])
def pub_forget_password():
    if request.method == 'GET':
        return render_template('auth/forgetpassword.html')
    else:
        email = request.form['email']
        checkEmail = Encryption.checkEmail(email)
        if (checkEmail == False):
            flash('Gagal, Email tidak ditemukan')
            return render_template('auth/forgetpassword.html', response="error")
    
        key = Fernet.generate_key()
        encode = Encryption.encrypt(email.encode(), key)
        link = "http://127.0.0.1:5000/change-password/" + str(key.decode()) + "/email/" + str(encode.decode())

        msg = Message('Komunikasi Publik', sender = 'melektechnology@gmail.com', recipients = [email])
        msg.body = "Silahkan klik account ini untuk ganti paswword " + link
        mail.send(msg)
        flash('Berhasil, silahkan cek email anda')
        return render_template('auth/forgetpassword.html', response="success")

@app.route("/change-password/<token>/email/<email>" , methods=["GET"])
def pub_change_password(token, email):
    getEmail = Encryption.decrypt(token, email)
    return render_template('auth/changepassword.html', email=getEmail.decode())

@app.route("/change-password/new-password" , methods=["POST"])
def pub_new_password():
    email = request.form['email']
    password = request.form['password']
    validatePassword = request.form['validate_password']
    if (password != validatePassword):
        flash('Gagal, Password yang anda masukkan tidak sesuai')
        return render_template('auth/changepassword.html', response="error", email=email)
    
    changePassword = Encryption.changePassword(email,password)
    flash('Berhasil, Password telah diubah silahkan login')
    return render_template('auth/login.html', response="success")