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

CREATE TABLE themes (
    id INTEGER PRIMARY KEY,
    value TEXT UNIQUE
);

CREATE TABLE styles (
    id INTEGER PRIMARY KEY,
    value TEXT UNIQUE
);

CREATE TABLE audiences (
    id INTEGER PRIMARY KEY,
    value TEXT UNIQUE
);

CREATE TABLE review_classes (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    theme TEXT, style TEXT, audience TEXT
);