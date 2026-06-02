import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import db
import config
import items
import users



app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items=items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user=users.get_user(user_id)
    if not user:
        abort(404)
    items=users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)


@app.route("/find_item")
def find_item():
    query=request.args.get("query")
    if query:
        results=items.find_items(query)
    else:
        query=""
        results=[]
    return render_template("find_item.html", query=query, results=results)


@app.route("/item/<int:item_id>")
def show_item(item_id):
    item=items.get_item(item_id)
    if not item:
        abort(404)
    classes=items.get_classes(item_id)
    return render_template("show_item.html", item=item, classes=classes)


@app.route("/new_item")
def new_item():
    require_login()
    classes=items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    title= request.form["title"]
    if not title or len(title)>50:
        abort(403)
    review= request.form["review"]
    if not review or len(review)>1000:
        abort(403)
    info= request.form["info"]
    if not info or len(info)>100:
        abort(403)
    user_id=session["user_id"]

    classes=[]
    for entry in request.form.getlist("classes"):
        if entry:
            parts=entry.split(":")
            classes.append((parts[0], parts[1]))

    items.add_item(title, review, info, user_id, classes)

    return redirect("/")


@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id=request.form["item_id"]
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title= request.form["title"]
    if not title or len(title)>50:
        abort(403)
    review= request.form["review"]
    if not review or len(review)>1000:
        abort(403)
    info= request.form["info"]
    if not info or len(info)>100:
        abort(403)

    items.update_item(item_id, title, review, info)

    return redirect("/item/"+str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item=items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method=="GET":
        return render_template("remove_item.html", item=item)
    
    if request.method=="POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/"+str(item_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register.html", error="Salasanat eivät ole samat")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Tunnus on jo varattu")

    session["message"]="Tunnus luotu onnistuneesti"
    return redirect("/login")

    

@app.route("/login", methods=["GET", "POST"])
def login():
    message=session.pop("message", None)
    if request.method=="GET":
        return render_template("login.html", message=message)

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id=users.check_login(username, password)
        if user_id:
            session["user_id"]=user_id
            session["username"] = username
            return redirect("/")


        return render_template("login.html", error="VIRHE: väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


