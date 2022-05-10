from PIL import Image
from flask import Flask, render_template,redirect,flash,url_for,request,abort
from app import app,db,bcrypt
from app.models import *
from .forms import *
from flask_login import login_user, current_user,logout_user,login_required



@app.route('/')
@app.route('/index')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.query.all()
    return render_template('index.html', user=current_user, pitches=pitches)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully. You can now login', 'success')
        return redirect(url_for('signIn'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating the user:(err_msg)')
    return render_template('signUp.html', form= form)



@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('signin.html', title = 'Login', form= form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/comment', methods=['GET', 'POST'])
def comment():
    form=CommentForm()
    return render_template('comment.html', form= form)



@app.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def newpitch():
    form=NewPitchForm()
    if form.validate_on_submit():
        pitch = Pitch(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(pitch)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('newpitch.html', form= form, legend='New Post')



@app.route("/pitch/<int:pitch_id>")
def allPitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    return render_template('Allpitches.html', title=pitch.title, pitch=pitch)


#uppdating a post

@app.route("/pitch/<int:pitch_id>/update", methods=['GET', 'POST'])
@login_required
def update_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    form = NewPitchForm()
    if form.validate_on_submit():
        pitch.title = form.title.data
        pitch.content = form.content.data
        db.session.commit()
        flash('Your pitch has been updated!', 'success')
        return redirect(url_for('pitch', pitch_id=pitch.id))
    elif request.method == 'GET':
        form.title.data = pitch.title
        form.content.data = pitch.content
    return render_template('newpitch.html', title='Update pitch',form=form, legend='Update Pitch')


#deleting a post
@app.route("/pitch/<int:pitch_id>/delete", methods=['POST'])
@login_required
def delete_pitch(pitch_id):
    pitch = Pitch.query.get_or_404(pitch_id)
    if pitch.author != current_user:
        abort(403)
    db.session.delete(pitch)
    db.session.commit()
    flash('Your pitch has been deleted!', 'success')
    return redirect(url_for('index'))


#updating a user profile
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.','success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)

#liking a specific post
@app.route('/like-pitch/<pitch_id>', methods=['GET'])
@login_required
def like(pitch_id):
    pitch = Pitch.query.filter_by(id=pitch_id)
    like = Like.query.filter_by(author=current_user.id, pitch_id=pitch_id).first()
    if not pitch:
        flash('Post does not exist.')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, pitch_id=pitch_id)
        db.session.add(like)
        db.session.commit()
        
    return redirect(url_for('index'))
        
@app.route("/create-comment/<pitch_id>/", methods=['POST', 'GET'])
@login_required
def create_comment(pitch_id):
    comment = request.form.get('text')
    flash('comment updated.')    
    if not comment:
        flash('Comment cannot be empty.')
    else:
        pitch = Pitch.query.filter_by(id=post_id)
        if pitch:
            comment = Comment(comment=comment, author=current_user.id, pitch_id=pitch_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.')
    return redirect(url_for('index'))
    

