import db

def add_comment(review_id, user_id, content, rating):
    sql = """INSERT INTO comments (review_id, user_id, content, rating)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [review_id, user_id, content, rating])


def get_comments(review_id):
    sql="""
        SELECT comments.content, comments.rating,
            users.id user_id, users.username
        FROM comments, users
        WHERE comments.review_id=? AND comments.user_id=users.id
        ORDER BY comments.id DESC
    """
    return db.query(sql, [review_id])


def get_average_rating(review_id):
    sql="SELECT AVG(rating) AS average FROM comments WHERE review_id=?"
    result=db.query(sql, [review_id])
    return result[0]["average"] if result else None


