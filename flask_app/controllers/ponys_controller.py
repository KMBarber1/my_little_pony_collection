from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models.pony import Pony
from flask_app.models.user import User



@app.route("/dashboard")
def all_collectors():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id": session["user_id"]
    }
    return render_template("all_collectors.html", user = User.get_by_id(data), ponys = Pony.get_all())


@app.route("/new/pony")
def new_pony():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":session["user_id"]
    }
    return render_template("add_pony.html", user = User.get_by_id(data))


@app.route("/edit/pony/<int:id>")
def edit_pony(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":id
    }
    user_data = {
        "id":session["user_id"]
    }
    return render_template("edit_pony.html", edit = Pony.get_one(data), user = User.get_by_id(user_data))





@app.route("/create/pony", methods=["POST"])
def create_pony():
    if "user_id" not in session:
        return redirect("/logout")
    if not Pony.validate_pony(request.form):
        return redirect("/add/pony")
    data = {
        "name": request.form["name"],
        "location_made": request.form["location_made"],
        "comment": request.form["comment"],
        "user_id": session["user_id"]
    }
    Pony.save(data)
    return redirect("/dashboard")


@app.route("/update/pony", methods=["POST"])
def update_pony():
    if "user_id" not in session:
        return redirect("/logout")
    if not Pony.validate_pony(request.form):
            return redirect(f"/edit/pony/{request.form['id']}")

    Pony.update(request.form)
    return redirect("/my_collection")


@app.route("/delete/pony/<int:id>")
def delete_pony(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":id
    }
    Pony.delete(data)
    return redirect("/my_collection")

# @app.route("/pony/<int:id>")
# def pony_research(id):
#     if "user_id" not in session:
#         return redirect("/logout")
#     data = {
#         "id":id
#     }
#     user_data = {
#         "id":session["user_id"]
#     }
#     return render_template("research.html", pony = Pony.get_one(data), user = User.get_by_id(user_data))

@app.route("/pony")
def pony_research():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id": session["user_id"]
    }

    return render_template("research.html", user = User.get_by_id(data))
