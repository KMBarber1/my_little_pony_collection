from flask import redirect, render_template,request, session
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)







@app.route("/")
def index():
    return render_template("login.html")



@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    data ={
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session["user_id"] = id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')


@app.route("/my_collection")
def show_collection():
    data = {
    "id": session["user_id"]
    }

    return render_template("my_collection.html", user = User.get_one_with_ponys(data))


@app.route("/wishlist")
def show_wanted():
    data = {
        "id": session["user_id"]
    }

    return render_template("wishlist.html", user = User.get_one_with_ponys(data))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")