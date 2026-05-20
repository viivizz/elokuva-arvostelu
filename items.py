import db

def add_item(title, review, info, user_id):
    sql = """INSERT INTO items (title, review, info, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, review, info, user_id])