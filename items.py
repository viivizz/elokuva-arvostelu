import db

def add_item(title, review, info, user_id):
    sql = """INSERT INTO items (title, review, info, user_id)
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, review, info, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.review,
                    items.info,
                    users.id user_id,
                    users.username
            FROM items, users
            WHERE items.user_id = users.id AND
                items.id = ?"""
    return db.query(sql, [item_id])[0]


def update_item(item_id, title, review, info):
    sql = """UPDATE items SET title = ?,
                            review = ?,
                            info = ?
                        WHERE id = ?"""
    db.execute(sql, [title, review, info, item_id])


def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql="""SELECT id, title
            FROM items
            WHERE title LIKE ? OR review LIKE ?
            OR info LIKE ?
            ORDER BY id DESC"""
    like="%"+query+"%"
    return db.query(sql, [like, like, like])