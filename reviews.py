import db

def add_review(data, user_id):
    sql = """
        INSERT INTO reviews
        (title, content, director, release_year, genre, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    db.execute(sql, [
        data["title"],
        data["content"],
        data["director"],
        data["release_year"],
        data["genre"],
        user_id
    ])

    review_id=db.last_insert_id()

    sql="""
        INSERT INTO review_classes
        (review_id, class_id)
        VALUES (?,?)
    """

    for class_id in data["class_ids"]:
        db.execute(sql,[review_id, class_id])

    return review_id



def get_reviews():
    sql = """
        SELECT reviews.id, reviews.title,
            users.id user_id, users.username,
            COUNT(comments.id) comment_count,
            AVG(comments.rating) average_rating
        FROM reviews
        JOIN users ON reviews.user_id=users.id
        LEFT JOIN comments ON reviews.id=comments.review_id
        GROUP BY reviews.id
        ORDER BY reviews.id DESC
    """
    return db.query(sql)

def get_review(review_id):
    sql = """
        SELECT reviews.id,
            reviews.title,
            reviews.content,
            reviews.director,
            reviews.release_year,
            reviews.genre,
            users.id user_id,
            users.username
        FROM reviews
        JOIN users ON reviews.user_id=users.id
        WHERE reviews.id = ?
    """
    result=db.query(sql, [review_id])
    return result[0] if result else None


def update_review(review_id, data):
    sql = """
        UPDATE reviews
        SET title = ?,
            content = ?,
            director = ?,
            release_year = ?,
            genre = ?
        WHERE id = ?
    """
    db.execute(sql, [
        data["title"],
        data["content"],
        data["director"],
        data["release_year"],
        data["genre"],
        review_id
    ])

    sql="DELETE FROM review_classes WHERE review_id = ?"
    db.execute(sql, [review_id])

    sql="""
        INSERT INTO review_classes (review_id, class_id)
        VALUES (?,?)
    """

    for class_id in data["class_ids"]:
        db.execute(sql,[review_id, class_id])


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