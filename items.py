import db

def add_item(title, review, info, user_id):
    sql = """INSERT INTO items (title, review, info, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, review, info, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items. title,
                    items.review,
                    items.info,
                    users.username
            FROM items, users
            WHERE items.user_id = users.id AND
                items.id = ?"""
    return db.query(sql, [item_id])[0]