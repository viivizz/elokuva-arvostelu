import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
import db
import config
import reviews
import users
import markupsafe



app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        flash("Kirjaudu sisään käyttääksesi tätä toimintoa")
        return False
    return True


@app.route("/")
def index():
    all_reviews=reviews.get_reviews()
    return render_template("index.html", reviews=all_reviews)

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
    reviews=users.get_reviews(user_id)
    return render_template("show_user.html", user=user, reviews=reviews)


@app.route("/find_review")
def find_review():
    query=request.args.get("query")
    if query:
        results=reviews.find_reviews(query)
    else:
        query=""
        results=[]
    return render_template("find_review.html", query=query, results=results)


@app.route("/review/<int:review_id>")
def show_review(review_id):
    review=reviews.get_review(review_id)
    if not review:
        abort(403)
    classes=reviews.get_classes(review_id)
    comments=reviews.get_comments(review_id)
    return render_template("show_review.html", review=review, classes=classes, comments=comments)


@app.route("/new_review")
def new_review():
    if not require_login():
        return redirect("/login")
    
    themes=reviews.get_themes()
    styles=reviews.get_styles()
    audiences=reviews.get_audiences()

    return render_template("new_review.html", themes=themes, styles=styles, audiences=audiences)



@app.route("/create_comment", methods=["POST"])
def create_comment():
    if not require_login():
        return redirect("/login")

    review_id=int(request.form["review_id"])
    review=reviews.get_review(review_id)
    if not review:
        abort(403)

    content=request.form["content"]
    if not content or len(content)>1000:
        flash("Virhe: kommentti on virheellinen")
        return redirect("/review/"+str(review_id))

    rating=request.form["rating"]
    if not rating:
        flash("Virhe: arvosana puuttuu")
        return redirect("/review/"+str(review_id))

    if not rating.isdigit():
        flash("Virhe: arvosanan pitää olla numero")
        return redirect("/review/"+str(review_id))
    rating=int(rating)
    if rating < 1 or rating > 5:
        flash("Virhe: arvosanan pitää olla välillä 1-5")
        return redirect("/review/"+str(review_id))


    user_id=session["user_id"]

    reviews.add_comment(review_id, user_id, content, rating)
    flash("Kommentti luotiin onnistuneesti")
    return redirect("/review/"+str(review_id))


@app.route("/create_review", methods=["POST"])
def create_review():
    if not require_login():
        return redirect("/login")
    
    title= request.form["title"]
    if not title or len(title)>50:
        flash("Virhe: elokuvan nimi on virheellinen")
        return redirect("/new_review")
    
    content= request.form["content"]
    if not content or len(content)>1000:
        flash("Virhe: arvosteluteksti on virheellinen")
        return redirect("/new_review")
    
    director=request.form["director"]
    if not director or len(director)>50:
        flash("Virhe: ohjaaja on virheellinen")
        return redirect("/new_review")
    
    release_year=request.form["release_year"]
    if not release_year:
        flash("Virhe: julkaisuvuosi puuttuu")
        return redirect("/new_review")
    
    genre=request.form["genre"]
    if not genre or len(genre)>50:
        flash("Virhe: genre on virheellinen")
        return redirect("/new_review")
    
    user_id=session["user_id"]


    theme=request.form["theme"]
    style=request.form["style"]
    audience=request.form["audience"]

    if theme!="" and theme not in reviews.get_theme_values():
        abort(403)

    if style!="" and style not in reviews.get_style_values():
        abort(403)

    if audience!="" and audience not in reviews.get_audience_values():
        abort(403)

    reviews.add_review(title, content, director, release_year, genre, user_id, theme, style, audience)
    review_id=db.last_insert_id()
    flash("Arvostelu luotiin onnistuneesti")
    return redirect("/review/"+str(review_id))


@app.route("/edit_review/<int:review_id>")
def edit_review(review_id):
    if not require_login():
        return redirect("/login")
    
    review=reviews.get_review(review_id)
    if not review:
        abort(403)
    if review["user_id"] != session["user_id"]:
        abort(403)

    themes=reviews.get_themes()
    styles=reviews.get_styles()
    audiences=reviews.get_audiences()

    classes=reviews.get_classes(review_id)

    return render_template("edit_review.html", review=review, themes=themes, styles=styles, audiences=audiences, classes=classes)


@app.route("/update_review", methods=["POST"])
def update_review():
    if not require_login():
        return redirect("/login")
    
    review_id=request.form["review_id"]
    review=reviews.get_review(review_id)
    if not review:
        abort(404)
    if review["user_id"] != session["user_id"]:
        abort(403)

    title= request.form["title"]
    if not title or len(title)>50:
        flash("Virhe: elokuvan nimi on virheellinen")
        return redirect("/edit_review/"+str(review_id))
    
    content= request.form["content"]
    if not content or len(content)>1000:
        flash("Virhe: arvosteluteksti on virheellinen")
        return redirect("/edit_review/"+str(review_id))
    
    director=request.form["director"]
    if not director or len(director)>50:
        flash("Virhe: ohjaaja on virheellinen")
        return redirect("/edit_review/"+str(review_id))
    
    release_year=request.form["release_year"]
    if not release_year:
        flash("Virhe: julkaisuvuosi puuttuu")
        return redirect("/edit_review/"+str(review_id))
    if not release_year.isdigit():
        flash("Virhe: julkaisuvuoden pitää olla numero")
        return redirect("/edit_review/"+str(review_id))
    
    genre=request.form["genre"]
    if not genre or len(genre)>50:
        flash("Virhe: genre on virheellinen")
        return redirect("/edit_review/"+str(review_id))

    theme=request.form["theme"]
    style=request.form["style"]
    audience=request.form["audience"]

    if theme!="" and theme not in reviews.get_theme_values():
        abort(403)

    if style!="" and style not in reviews.get_style_values():
        abort(403)

    if audience!="" and audience not in reviews.get_audience_values():
        abort(403)

    reviews.update_review(review_id, title, content, director, release_year, genre, theme, style, audience)

    flash("Arvostelu päivitetty onnistuneesti")
    return redirect("/review/"+str(review_id))


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
        if "remove" in request.form:
            reviews.remove_review(review_id)
            return redirect("/")
        else:
            return redirect("/review/"+str(review_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html", filled={})
    
    if request.method=="POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        filled={"username": username}

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
        except sqlite3.IntegrityError:
            flash("Tunnus on jo varattu")
            return render_template("register.html", filled=filled)

        flash("Tunnus luotu onnistuneesti")
        return redirect("/login")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id=users.check_login(username, password)
        if user_id:
            session["user_id"]=user_id
            session["username"] = username
            return redirect("/")
        
        flash("VIRHE: väärä tunnus tai salasana")
        return render_template("login.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


