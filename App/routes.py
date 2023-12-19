from io import UnsupportedOperation
import os
from crypt import methods
from flask import render_template, flash, redirect, url_for, request, abort
from App import app, db, files
from App.forms import LoginForm, RegistrationForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, UploadForm
from App.models import User, Piece
from App.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
#from werkzeug.utils import secure_filename
from datetime import datetime
import time
from Backend.MusicAnalysis.Music_Analysis_Main import mainMusicAnalysis
from Backend.SheetMusic.Sheet_Music_Main import mainSheetMusic
from PIL import Image

@app.route('/') #setting base route when website is first opened
@app.route('/welcome')
def welcome(): #function sets up welcome page
    return render_template('welcome.html', title='Welcome')

@app.route('/index')
@login_required
def index(): #function sets up home page
    return render_template('index.html', title='NEAHub')

@app.route('/login', methods=['GET', 'POST'])
def login(): #login page
    if current_user.is_authenticated: #if user already logged in redirect to home page
        return redirect(url_for('index'))
    form = LoginForm() #create a object of login form
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() #sql aclhemy query the database
        if user is None or not user.check_password(form.password.data): 
            #if there is no user with the username or the password is incorrect output invalid and redirect to login again
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) #then login if correct
        #sends the user to the home page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    #if no login render the html for the login page sneding in the form
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout') 
def logout():
    logout_user() #logout user
    return redirect(url_for('welcome')) #send to welcome page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: #if user is logged in then send to home page
        return redirect(url_for('index'))
    form = RegistrationForm() #create an object of registration form
    if form.validate_on_submit():
        #create an object of the user
        user = User(username=form.username.data, email=form.email.data)
        #set the password as a hash
        user.set_password(form.password.data)
        #add to the database
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login')) #send the user to the login page
    return render_template('register.html', title='Register', form=form)
        
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404() #gets user from database

    #use aggregate SQL to get the total number of pieces the user has
    totalUserPieces = db.engine.execute('''
    SELECT COUNT(piece.title) FROM piece, user WHERE piece.user_id = user.id AND user.username = (?)
    ''', (username)).scalar()

    #use cross-table parameterised SQL to get a list of the pieces the user has created
    userPiecesList = db.engine.execute('''
    SELECT piece.title, piece.id FROM piece, user WHERE piece.user_id = user.id AND user.username = (?) ORDER BY  piece.timestamp DESC
    ''', (username)).fetchall() #get all the pieces the user has created

    return render_template('user.html', user=user, pieces=userPiecesList, totalUserPieces=totalUserPieces)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = str(datetime.utcnow())[0:16]
        db.session.commit()#add the last seen to the database

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username) #create an object of edit profile form
    if form.validate_on_submit(): #when the form is submitted
        #set new values in the datbase
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            send_password_reset_email(user) #send reset password link to the username entered
        flash('Check your email for instructions to reset your password')
        return(redirect(url_for('login')))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Changes the password and updates the database
        user.set_password(form.password1.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm() #create an object of upload form
    if form.validate_on_submit():
        try: #catch any file uploading errors
            audio_upload_path = '/Users/bendyson/Coding/NEA/App/static/AudioUploads'
            sheet_upload_path = '/Users/bendyson/Coding/NEA/App/static/SheetUploads'

            #checks if user is currently logged in to amend upload path to user folder in upload folder
            if current_user.is_authenticated: 
                #creates the user folder in audio upload folder if there isnt one
                if not os.path.isdir(os.path.join(audio_upload_path, current_user.username)): 
                    os.makedirs(os.path.join(audio_upload_path, current_user.username))
                #creates the user folder in sheet upload folder if there isnt one    
                if not os.path.isdir(os.path.join(sheet_upload_path, current_user.username)): 
                    os.makedirs(os.path.join(sheet_upload_path, current_user.username))
                #Checks if the time signature is valid
                if not(form.timeSignature.data == '34' or form.timeSignature.data == '44'):
                    raise(ValueError)
                
                filename = files.save(form.file.data, os.path.join(audio_upload_path, current_user.username), form.title.data+'.')
                author = current_user.username
                AudioDirectory = os.path.join(audio_upload_path, current_user.username, form.title.data+filename[-4:])
                SheetDirectory = os.path.join(sheet_upload_path, current_user.username, form.title.data+'.png')

                #finds user id of the user creating the piece
                user_id = db.engine.execute('SELECT user.id FROM user WHERE user.username=(?)', (author)).scalar() #finds current user id

                db.engine.execute('''
                    INSERT INTO piece (user_id, title, author, AudioDirectory, SheetDirectory, key, bpm, timeSignature, timestamp)
                    VALUES (?, ? ,? ,?, ?, ? ,?, ?, ?)
                ''', user_id, form.title.data, author, AudioDirectory, SheetDirectory, form.key.data, form.bpm.data, form.timeSignature.data, str(datetime.utcnow())[0:16])
                #adds the piece to the database
                db.session.commit()

            else:
                if not(form.timeSignature.data == '34' or form.timeSignature.data == '44'):
                    raise()
                filename = files.save(form.file.data, audio_upload_path, form.title.data+'.')
                author = 'Unknown'
                AudioDirectory = os.path.join(audio_upload_path, form.title.data+filename[-4:])
                SheetDirectory = os.path.join(sheet_upload_path, form.title.data+'.png')

            #run main programs here
            notes, beats = mainMusicAnalysis(AudioDirectory)
            
            # notes = [['C4'], ['C4'], ['C4'], ['C4']]
            # beats = [600, 1100, 3100, 4100, 5100]

            notes = [['C4'], ['C4'], ['D4'], ['C4'], ['F4'], ['E4'], ['C4'], ['C4'], ['D4'], ['C4'], ['G4'], ['F4'], ['C4'], ['C4'], ['C5'], ['A4'], ['F4'], ['E4'], ['D4'], ['A#4'], ['A#4'], ['A4'], ['F4'], ['G4'], ['F4']]
            beats = [600, 1100, 1600, 2600, 3600, 4600, 6600, 7100, 7600, 8600, 9600, 10600, 12600, 13100, 13600, 14600, 15600, 16600, 17600 , 18600, 19100, 19600, 20600, 21600, 22600, 24600]
            
            mainSheetMusic(notes, beats, form.title.data, form.timeSignature.data, form.bpm.data, SheetDirectory, author)

            flash('Piece has been uploaded')

        except: #any errors
            flash('Upload Not Allowed')
            return render_template('upload.html', form=form)

    return render_template('upload.html', form=form)


@app.route('/piece/<pieceid>', methods=["GET", "POST"])
def piece(pieceid):
    SheetDirectory = db.engine.execute("SELECT SheetDirectory FROM piece WHERE piece.id = (?)", pieceid).scalar()

    #remove first 30 charcters to allow html to access it
    SheetDirectory = SheetDirectory[30:]
    return render_template("showPiece.html", SheetDirectory=SheetDirectory)

