import db

def get_themes():
    sql="SELECT value FROM themes ORDER BY id"
    return db.query(sql)

def get_styles():
    sql="SELECT value FROM styles ORDER BY id"
    return db.query(sql)

def get_audiences():
    sql="SELECT value FROM audiences ORDER BY id"
    return db.query(sql)

def get_theme_values():
    values=[]
    for row in get_themes():
        values.append(row["value"])
    return values

def get_style_values():
    values=[]
    for row in get_styles():
        values.append(row["value"])
    return values

def get_audience_values():
    values=[]
    for row in get_audiences():
        values.append(row["value"])
    return values



def add_review(title, content, director, release_year, genre, user_id, theme, style, audience):
    sql = """INSERT INTO reviews (title, content, director, release_year, genre, user_id)
            VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, content, director, release_year, genre, user_id])

    review_id=db.last_insert_id()


    sql="INSERT INTO review_classes (review_id, theme, style, audience) VALUES (?,?,?,?)"
    db.execute(sql,[review_id, theme, style, audience])


def add_comment(review_id, user_id, content, rating):
    sql = """INSERT INTO comments (review_id, user_id, content, rating)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [review_id, user_id, content, rating])

def get_comments(review_id):
    sql="""SELECT comments.content, comments.rating, users.id user_id, users.username
            FROM comments, users
            WHERE comments.review_id=? AND comments.user_id=users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [review_id])


def get_classes(review_id):
    sql="SELECT theme, style, audience FROM review_classes WHERE review_id =?"
    result=db.query(sql, [review_id])
    return result[0] if result else {"theme": "", "style": "", "audience": ""}

def get_reviews():
    sql = """SELECT reviews.id, reviews.title, users.id user_id, users.username,
        COUNT(comments.id) comment_count
      FROM reviews JOIN users ON reviews.user_id=users.id
        LEFT JOIN comments ON reviews.id=comments.review_id
      GROUP BY reviews.id
      ORDER BY reviews.id DESC"""
    return db.query(sql)

def get_review(review_id):
    sql = """SELECT reviews.id,
                    reviews.title,
                    reviews.content,
                    reviews.director,
                    reviews.release_year,
                    reviews.genre,
                    users.id user_id,
                    users.username
            FROM reviews, users
            WHERE reviews.user_id = users.id AND
                reviews.id = ?"""
    result=db.query(sql, [review_id])
    return result[0] if result else None


def update_review(review_id, title, content, director, release_year, genre, theme, style, audience):
    sql = """UPDATE reviews SET title = ?,
                            content = ?,
                            director = ?,
                            release_year = ?,
                            genre = ?
                        WHERE id = ?"""
    db.execute(sql, [title, content, director, release_year, genre, review_id])

    sql="DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql="INSERT INTO review_classes (review_id, theme, style, audience) VALUES (?,?,?,?)"
    db.execute(sql,[review_id, theme, style, audience])


def remove_review(review_id):
    sql = "DELETE FROM comments WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql = "DELETE FROM reviews WHERE id = ?"
    db.execute(sql, [review_id])

def find_reviews(query):
    sql="""SELECT id, title
            FROM reviews
            WHERE title LIKE ? OR content LIKE ?
            OR director LIKE ?
            OR release_year LIKE ?
            OR genre LIKE ?
            ORDER BY id DESC"""
    like="%"+query+"%"
    return db.query(sql, [like, like, like, like, like])