CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE platforms (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);


CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    brand_id INT REFERENCES brands(id),
    platform_id INT REFERENCES platforms(id),
    platform VARCHAR(50),
    raw_text TEXT NOT NULL,
    cleaned_text TEXT NOT NULL,
    user_id TEXT,
    original_post_url TEXT,
    posted_at TIMESTAMP,
    language VARCHAR(50),
    reach_estimate BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    like_count INT,
    view_count INT,
    share_count INT,
    comment_count INT,
    followers_count INT,

    state VARCHAR(50),
    country VARCHAR(50)
);


CREATE TABLE sentiment_results (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    sentiment_label TEXT CHECK (sentiment_label IN ('Positive', 'Neutral', 'Negative')),
    sentiment_score NUMERIC(5,4),  
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE named_entities (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    entity_text TEXT,
    entity_label TEXT  
    --start_offset INT
    --end_offset INT
);


-- Daily Overall Sentiment Per Brand

CREATE TABLE brand_aggregates (
    brand_id INT REFERENCES brands(id),
    date DATE NOT NULL,
    positive_count INT DEFAULT 0,
    neutral_count INT DEFAULT 0,
    negative_count INT DEFAULT 0,
    total_reach BIGINT DEFAULT 0,
    PRIMARY KEY (brand_id, date)
);


-- Daily Overall Sentiment Per Brand Per Platform

CREATE TABLE brand_platform_aggregates (
    brand_id INT REFERENCES brands(id),
    platform VARCHAR(50),
    date DATE,
    positive_count INT DEFAULT 0,
    neutral_count INT DEFAULT 0,
    negative_count INT DEFAULT 0,
    total_reach BIGINT DEFAULT 0,
    PRIMARY KEY (brand_id, platform, date)
);


CREATE TABLE top_handles (
    id SERIAL PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    followers_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


