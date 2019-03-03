from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from stancjainfo import app, db, bcrypt
from stancjainfo.forms import RegistrationForm, LoginForm, PostForm, InternetEntryForm
from stancjainfo.models import User, Post, InternetEntry


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/test')
@login_required
def test():
    posts = Post.query.all()
    return render_template('test.html', posts=posts, title='Superposts!')


def is_current_user_an_admin():
    return current_user.is_authenticated and User.query.get(current_user.id).role == 'ADMIN'


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post został utworzony', 'success')
        return redirect(url_for('test'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>')
@login_required
def show_post(post_id):
    post_obj = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post_obj)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post_obj = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post_obj.title = form.title.data
        post_obj.content = form.content.data
        db.session.commit()
        flash("Post zmodyfikowany", 'success')
        redirect(url_for('show_post', post_id=post_obj.id))
    elif request.method == 'GET':
        form.title.data = post_obj.title
        form.content.data = post_obj.content
    return render_template('create_post.html', post=post_obj, form=form)


# noinspection PyArgumentList
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=str(form.username.data).lower(),
                    name=str(form.name.data).capitalize(),
                    surname=str(form.surname.data).capitalize(),
                    email=str(form.email.data).lower(),
                    password=hashed_password,
                    accepted=False,
                    active=True,
                    role='USER')
        db.session.add(user)
        db.session.commit()
        flash(f'Stworzono nowe konto {form.username.data}. Proszę czekać na akceptację', 'success')
        return redirect(url_for('hello_world'))

    return render_template('register.html', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=str(form.username.data).lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            user.last_logged = datetime.now()
            db.session.commit()
            next_page = request.args.get('next')
            flash('Zostałeś zalogowany', 'success')
            return redirect(next_page) if next_page else redirect(url_for('hello_world'))
        else:
            flash('Logowanie nieudane - błędne dane', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.route('/adminpanel')
@login_required
def admin_panel():
    if not is_current_user_an_admin:
        return redirect(url_for('hello_world'))
    return render_template('admin_panel.html')


@app.route('/adminpanel/internet')
@login_required
def admin_internet():
    if not is_current_user_an_admin:
        return redirect(url_for('hello_world'))
    internet_entries = InternetEntry.query.all()
    print(internet_entries)
    return render_template('admin_internet.html', internet_entries=internet_entries)


@app.route('/adminpanel/internet/new', methods=['GET', 'POST'])
@login_required
def admin_add_internet_entry():
    if not is_current_user_an_admin:
        return redirect(url_for('hello_world'))
    form = InternetEntryForm()
    if form.validate_on_submit():
        internet_entry = InternetEntry(
            month=form.month.data,
            year=form.year.data,
            payment_amount=form.payment_amount.data,
            date_of_payment=form.date_of_payment.data,
            penalty=form.penalty.data)
        db.session.add(internet_entry)
        db.session.commit()
        flash('Wpis został utworzony', 'success')
        return redirect(url_for('admin_internet'))
    return render_template('create_internet_entry.html', form=form)


@app.route('/adminpanel/internet/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def show_internet_entry(entry_id):
    internet_entry = InternetEntry.query.get_or_404(entry_id)
    payments = internet_entry.payments
    per_capita = internet_entry.payment_amount / 5  # TODO: inaczej
    return render_template('internet_entry.html', internet_entry=internet_entry, per_capita=per_capita,
                           payments=payments)


@app.route('/internet')
@login_required
def internet():
    internet_entry = InternetEntry.query.order_by(InternetEntry.year.desc(), InternetEntry.month.desc()).first()
    payments = internet_entry.payments
    per_capita = internet_entry.payment_amount / 5
    return render_template('internet_entry.html', internet_entry=internet_entry, per_capita=per_capita,
                           payments=payments)
