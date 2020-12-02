from flask import current_app as app
from flask import render_template,redirect, request, url_for,flash, abort
from . import auth
from flask_login import login_user, login_required, current_user
# from flask_user import UserManager, roles_required
from ..email import mail_message
from datetime import datetime
from flask_mail import Message
from ..models import User, Role, Post, Subscribe

@auth.route('/profile/<uname>')
@login_required
def profile(uname):
	user = User.query.filter_by(username=uname).first()

	if user is None:
		abort(404)

	return render_template("profile/profile.html",user=user)

@auth.route('/profile/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = BioForm()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        flash("Bio updated!","success")
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',bioform =form, user=user)

@auth.route('/profile/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('admin.profile',uname=uname))


@auth.route('/post',methods=['GET','POST'])
@login_required
def post():
    form = PostForm()

    if 'photo' in request.files and form.validate_on_submit():

        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'

        title = form.title.data
        content = form.content.data
        new_post = Post(title=form.title.data, content=form.content.data,pic_path=path)
        db.session.add(new_post)
        db.session.commit()

        subscribed_user = Subscribe.query.all()

        with mail.connect() as conn:
            for user in subscribed_user:
                e = user.email
                name = e.split('@')[0]
                message = 'You have a new post waiting for you,at 60sec_pitch'
                subject = "hello, %s" % name
                msg = Message(recipients=[user.email],
                              body=message,
                              subject=subject)

                conn.send(msg)

        flash("New post created successfully","success")

        return redirect(url_for('admin.post'))

    return render_template('post.html',form = form)




@auth.route('/auth',methods=['GET','POST'])
def admin():
    user_auth = User.query.filter(User.username == 'admin@admin.com').first()
    login_form = LoginForm()
    try:
        if not user_auth:
            user = User()
            user.name='admin',
            user.password=app.config['ADMIN_PASSWORD']
            user.username=app.config['ADMIN_USERNAME']

            user.roles.append(Role(role_name='Admin'))
            user.roles.append(Role(role_name='User'))

            db.session.add(user)
            db.session.commit()
            db.session.close()
        else:
            redirect(url_for('.admin'))
    except:
        db.session.rollback()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    if current_user.is_authenticated:
        return redirect (url_for('main.index'))

    return render_template('admin_login.html', login_form=login_form)