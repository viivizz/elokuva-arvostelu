CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    title TEXT,
    director TEXT,
    release_year INTEGER,
    genre TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    user_id INTEGER REFERENCES users(id),
    content TEXT,
    rating INTEGER
);


CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class_type TEXT,
    UNIQUE(name, class_type)
);

CREATE TABLE review_classes (
    review_id INTEGER REFERENCES reviews(id),
    class_id INTEGER REFERENCES classes(id),
    PRIMARY KEY (review_id, class_id)
);