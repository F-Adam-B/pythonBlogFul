from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash


from blog._init_ import app
from .database import session, Entry, User
from getpass import getpass


PAGINATE_BY = 10


@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):

    # zero-indexed page
    page_index = page - 1

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
                           entries=entries,
                           has_next=has_next,
                           has_prev=has_prev,
                           page=page,
                           total_pages=total_pages
                           )


@app.route("/entry/add", methods=["GET"])
@login_required
# renders blog entry form
def add_entry_get():
    return render_template("add_entry.html")


@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user,
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))

# @login_required
# view a single entry by clicking on the title
@app.route("/entry/<id>", methods=["GET"])
def get_entry(id):
    entry = session.query(Entry).filter(Entry.id == id).one()
    return render_template("get_entry.html", entry=entry)


@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry = session.query(Entry).filter(Entry.id == id).one()
    return render_template("edit_entry.html", entry=entry)


@app.route("/entry/<id>/edit", methods=["POST"])
@login_required
def edit_entry_put(id, title=None, content=None):
    entry = session.query(Entry).filter(Entry.id == id).one()
    entry.title = request.form['title'],
    entry.content = request.form['content']
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route("/entry/<id>/delete")
@login_required
def edit_entry_delete(id):
    entry = session.query(Entry).filter(Entry.id == id).one()
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))


@app.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    email = request.form["email"]
    if session.query(User).filter_by(email=email).first():
        flash('User with that e-mail already exists')
        return render_template("signup.html")
    username = request.form["username"]
    # if session.query(User).filter_by(username=username):
    #     flash('User with that e-mail already exists')
    #     return render_template("signup.html")
    password = request.form["password"]
    password_2 = request.form['password_2']
    while len(password) < 4 or password != password_2:
        flash("Passwords don't match. Try again")
        return render_template("signup.html")
    user = User(email=email, username=username, password=generate_password_hash(password))
    session.add(user)
    session.commit()

    return redirect(url_for("login_get"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("entries"))



