import db

def get_classes():
    sql="SELECT id, name, class_type FROM classes ORDER BY name"
    return db.query(sql)

def get_grouped_classes():
    all_classes=get_classes()

    grouped={
        "themes": [],
        "styles": [],
        "audiences": []
    }

    for c in all_classes:
        if c["class_type"]=="theme":
            grouped["themes"].append(c)
        elif c["class_type"]=="style":
            grouped["styles"].append(c)
        elif c["class_type"]=="audience":
            grouped["audiences"].append(c)
    
    return grouped


def get_review_classes(review_id):
    sql="""
        SELECT classes.id, classes.name, classes.class_type
        FROM review_classes
        JOIN classes ON review_classes.class_id=classes.id
        WHERE review_classes.review_id=?
    """
    return db.query(sql, [review_id])