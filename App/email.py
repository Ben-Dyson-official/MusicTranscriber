from flask_mail import Message
from App import mail, app
from flask import render_template
from threading import Thread

def send_password_reset_email(user):
    token=user.get_reset_password_token() #creates a token for the user to reset password
    #calls the send email function 
    send_email('NEA Password Reset Link', 
            sender=app.config['ADMINS'][0], 
            recipients=[user.email], 
            text_body=render_template('email/reset_password.txt', user=user, token=token), 
            html_body=render_template('email/reset_password.html', user=user, token=token)
            )
def send_async_email(app, msg): #used for threading
    with app.app_context():
        mail.send(msg)

#actually sends the email
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #sends the message using threading so the website still runs
    Thread(target=send_async_email, args=(app, msg)).start() 
