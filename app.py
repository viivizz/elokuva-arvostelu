import sqlite3
import secrets

from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
import markupsafe

import db
import config
import reviews
import comments
import classes
import users
from constants import MAX_TITLE, MAX_CONTENT, MAX_DIRECTOR, MAX_GENRE, MIN_YEAR, MAX_YEAR



app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login():
    if "user_id" not in session:
        flash("Kirjaudu sisään käyttääksesi tätä toimintoa", "warning")
        return False
    return True

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    all_reviews=reviews.get_reviews()
    return render_template(
        "index.html",
        reviews=all_reviews
    )

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user=users.get_user(user_id)
    if not user:
        abort(404)
    user_reviews=users.get_reviews(user_id)
    return render_template(
        "show_user.html",
        user=user,
        reviews=user_reviews
    )


@app.route("/find_review")
def find_review():
    query=request.args.get("query")
    if query:
        results=reviews.find_reviews(query)
    else:
        query=""
        results=[]
    return render_template(
        "find_review.html",
        query=query,
        results=results
    )


@app.route("/review/<int:review_id>")
def show_review(review_id):
    review=reviews.get_review(review_id)
    if not review:
        abort(404)

    review_classes=classes.get_review_classes(review_id)

    review_comments=comments.get_comments(review_id)
    average_rating=comments.get_average_rating(review_id)
    saved_content=session.pop("saved_content", "")
    saved_rating=session.pop("saved_rating", "")
    return render_template(
        "show_review.html",
        review=review,
        review_classes=review_classes,
        review_comments=review_comments,
        saved_content=saved_content,
        saved_rating=saved_rating,
        average_rating=average_rating
    )


@app.route("/new_review")
def new_review():
    if not require_login():
        return redirect("/login")

    grouped=classes.get_grouped_classes()

    form_data=session.pop("form_data", {})

    return render_template(
        "new_review.html",
        themes=grouped["themes"],
        styles=grouped["styles"],
        audiences=grouped["audiences"],
        form_data=form_data
    )



@app.route("/create_comment", methods=["POST"])
def create_comment():
    if not require_login():
        session["saved_content"]=request.form["content"]
        session["saved_rating"]=request.form["rating"]
        review_id=request.form["review_id"]
        return redirect(f"/login?next=/review/{review_id}")
    check_csrf()

    review_id=int(request.form["review_id"])
    review=reviews.get_review(review_id)
    if not review:
        abort(404)

    content=request.form["content"]
    if not content:
        flash("Kirjoita kommentti (ei voi olla tyhjä)", "warning")
        return redirect(f"/review/{review_id}")
    if len(content)>MAX_CONTENT:
        flash("Kommentti on liian pitkä (max 1000 merkkiä)", "error")
        return redirect(f"/review/{review_id}")

    rating=request.form["rating"]
    if not rating:
        flash("Anna arvosana (1-5 tähteä)", "warning")
        return redirect(f"/review/{review_id}")

    if not rating.isdigit():
        flash("Arvosanan pitää olla numero", "error")
        return redirect(f"/review/{review_id}")
    rating=int(rating)
    if rating < 1 or rating > 5:
        flash("Arvosanan pitää olla välillä 1-5", "error")
        return redirect(f"/review/{review_id}")


    user_id=session["user_id"]

    comments.add_comment(review_id, session["user_id"], content, rating)
    flash("Kommentti luotiin onnistuneesti", "success")
    return redirect(f"/review/{review_id}")


@app.route("/create_review", methods=["POST"])
def create_review():
    if not require_login():
        return redirect("/login")
    check_csrf()

    title= request.form["title"]
    if not title:
        flash("Kirjoita elokuvan nimi (ei voi olla tyhjä)", "warning")
        return redirect("/new_review")
    if len(title)>MAX_TITLE:
        flash("Elokuvan nimi on liian pitkä (max 50 merkkiä)", "error")
        return redirect("/new_review")
    
    content= request.form["content"]
    if not content:
        flash("Kirjoita arvosteluteksti (ei voi olla tyhjä)", "warning")
        return redirect("/new_review")

    if len(content)>MAX_CONTENT:
        flash("Arvosteluteksti on liian pitkä (max 1000 merkkiä)", "error")
        return redirect("/new_review")

    
    director=request.form["director"]
    if not director:
        flash("Kirjoita ohjaajan nimi (ei voi olla tyhjä)", "warning")
        return redirect("/new_review")

    if len(director)>MAX_DIRECTOR:
        flash("Ohjaajan nimi on liian pitkä", "error")
        return redirect("/new_review")
    
    release_year=request.form["release_year"]
    if not release_year:
        session["form_data"]=request.form
        flash("Julkaisuvuosi puuttuu", "warning")
        return redirect("/new_review")

    if not release_year.isdigit():
        session["form_data"]=request.form
        flash("Julkaisuvuoden pitää olla numero", "error")
        return redirect("/new_review")

    release_year=int(release_year)

    if release_year<MIN_YEAR or release_year>MAX_YEAR:
        session["form_data"]=request.form
        flash(f"Julkaisuvuoden pitää olla välillä {MIN_YEAR}-{MAX_YEAR}", "error")
        return redirect("/new_review")

    genre=request.form["genre"]
    if not genre:
        flash("Kirjoita elokuvan genre (ei voi olla tyhjä)", "warning")
        return redirect("/new_review")

    if len(genre)>MAX_GENRE:
        flash("Genre on liian pitkä", "error")
        return redirect("/new_review")
    
    user_id=session["user_id"]

    class_ids=request.form.getlist("classes")

    if not class_ids:
        flash("Valitse vähintään yksi luokka", "warning")
        return redirect("/new_review")

    data= {
        "title": title,
        "content": content,
        "director": director,
        "release_year": release_year,
        "genre": genre,
        "class_ids": class_ids
    }

    review_id=reviews.add_review(data, user_id)

    flash("Arvostelu luotiin onnistuneesti", "success")
    return redirect(f"/review/{review_id}")


@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    if not require_login():
        return redirect("/login")
    
    review=reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    grouped=classes.get_grouped_classes()

    selected=classes.get_review_classes(review_id)
    selected_ids=[c["id"] for c in selected]

    return render_template(
        "edit_review.html",
        review=review,
        themes=grouped["themes"],
        styles=grouped["styles"],
        audiences=grouped["audiences"],
        selected_ids=selected_ids
    )

@app.route("/update_review", methods=["POST"])
def update_review():
    if not require_login():
        return redirect("/login")
    check_csrf()

    review_id=request.form["review_id"]
    review=reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    title= request.form["title"]
    if not title:
        flash("Kirjoita elokuvan nimi (ei voi olla tyhjä)", "warning")
        return redirect(f"/edit_review/{review_id}")
    if len(title)>MAX_TITLE:
        flash("Elokuvan nimi on liian pitkä (max 50 merkkiä)", "error")
        return redirect(f"/edit_review/{review_id}")

    content= request.form["content"]
    if not content:
        flash("Kirjoita arvosteluteksti (ei voi olla tyhjä)", "warning")
        return redirect(f"/edit_review/{review_id}")

    if len(content)>MAX_CONTENT:
        flash("Arvosteluteksti on liian pitkä (max 1000 merkkiä)", "error")
        return redirect(f"/edit_review/{review_id}")


    director=request.form["director"]
    if not director:
        flash("Kirjoita ohjaajan nimi (ei voi olla tyhjä)", "warning")
        return redirect(f"/edit_review/{review_id}")

    if len(director)>MAX_DIRECTOR:
        flash("Ohjaajan nimi on liian pitkä", "error")
        return redirect(f"/edit_review/{review_id}")
    
    release_year=request.form["release_year"]
    if not release_year:
        session["form_data"]=request.form
        flash("Julkaisuvuosi puuttuu", "warning")
        return redirect(f"/edit_review/{review_id}")

    if not release_year.isdigit():
        session["form_data"]=request.form
        flash("Julkaisuvuoden pitää olla numero", "error")
        return redirect(f"/edit_review/{review_id}")

    release_year=int(release_year)

    if release_year<MIN_YEAR or release_year>MAX_YEAR:
        session["form_data"]=request.form
        flash(f"Julkaisuvuoden pitää olla välillä {MIN_YEAR}-{MAX_YEAR}", "error")
        return redirect(f"/edit_review/{review_id}")

    genre=request.form["genre"]
    if not genre:
        flash("Kirjoita elokuvan genre (ei voi olla tyhjä)", "warning")
        return redirect(f"/edit_review/{review_id}")

    if len(genre)>MAX_GENRE:
        flash("Genre on liian pitkä", "error")
        return redirect(f"/edit_review/{review_id}")

    class_ids=request.form.getlist("classes")

    if not class_ids:
        flash("Valitse vähintään yksi luokka", "warning")
        return redirect(f"/edit_review/{review_id}")

    data= {
        "title": title,
        "content": content,
        "director": director,
        "release_year": release_year,
        "genre": genre,
        "class_ids": class_ids
    }

    reviews.update_review(review_id, data)

    flash("Arvostelu päivitetty onnistuneesti", "success")
    return redirect(f"/review/{review_id}")


@app.route("/remove_review/<int:review_id>", methods=["GET", "POST"])
def remove_review(review_id):
    if not require_login():
        return redirect("/login")

    review=reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    if request.method=="GET":
        return render_template("remove_review.html", review=review)
    
    if request.method=="POST":
        check_csrf()
        if request.form.get("remove"):
            reviews.remove_review(review_id)
            return redirect("/")
        return redirect(f"/review/{review_id}")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html", filled={})
    
    if request.method=="POST":
        username = request.form["username"].strip()
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        filled={"username": username}

        if not username:
            flash("Käyttäjänimi ei voi olla tyhjä", "error")
            return render_template("register.html", filled=filled)
        if len(username)<3:
            flash("Käyttäjätunnuksen on oltava vähintään 3 merkkiä", "error")
            return render_template("register.html", filled=filled)


        if password1 != password2:
            flash("Antamasi salasanat eivät ole samat", "error")
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
        except sqlite3.IntegrityError:
            flash("Tunnus on jo varattu", "error")
            return render_template("register.html", filled=filled)

        flash("Tunnus luotu onnistuneesti", "success")
        return redirect("/login")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html", filled={})

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id=users.check_login(username, password)
        if user_id:
            session["user_id"]=user_id
            session["username"] = username
            session["csrf_token"]=secrets.token_hex(16)
            next_page=request.form.get("next")
            if next_page:
                return redirect(next_page)
            return redirect("/")
        
        if not user_id:
            flash("Väärä tunnus tai salasana", "error")
            return render_template("login.html", filled={"username": username})


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


