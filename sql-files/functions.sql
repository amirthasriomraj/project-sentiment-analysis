CREATE OR REPLACE FUNCTION update_brand_aggregates()
RETURNS TRIGGER AS $$
DECLARE
    post_data RECORD;
    sentiment_column TEXT;
BEGIN
    -- Get the associated post
    SELECT p.brand_id, DATE(p.posted_at) AS post_date, p.reach_estimate
    INTO post_data
    FROM posts p
    WHERE p.id = NEW.post_id;

    -- Determine which column to increment
    IF NEW.sentiment_label = 'Positive' THEN
        sentiment_column := 'positive_count';
    ELSIF NEW.sentiment_label = 'Neutral' THEN
        sentiment_column := 'neutral_count';
    ELSIF NEW.sentiment_label = 'Negative' THEN
        sentiment_column := 'negative_count';
    ELSE
        RAISE EXCEPTION 'Invalid sentiment label: %', NEW.sentiment_label;
    END IF;

    -- Insert or update the aggregate row
    EXECUTE format($f$
        INSERT INTO brand_aggregates (brand_id, date, %I, total_reach)
        VALUES ($1, $2, 1, $3)
        ON CONFLICT (brand_id, date) DO UPDATE
        SET %I = brand_aggregates.%I + 1,
            total_reach = brand_aggregates.total_reach + EXCLUDED.total_reach
    $f$, sentiment_column, sentiment_column, sentiment_column)
    USING post_data.brand_id, post_data.post_date, COALESCE(post_data.reach_estimate, 0);

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION update_brand_platform_aggregates()
RETURNS TRIGGER AS $$
DECLARE
    post_data RECORD;
    sentiment_column TEXT;
BEGIN
    -- Get the associated post
    SELECT p.brand_id, DATE(p.posted_at) AS post_date, p.platform, p.reach_estimate
    INTO post_data
    FROM posts p
    WHERE p.id = NEW.post_id;

    -- Determine which column to increment
    IF NEW.sentiment_label = 'Positive' THEN
        sentiment_column := 'positive_count';
    ELSIF NEW.sentiment_label = 'Neutral' THEN
        sentiment_column := 'neutral_count';
    ELSIF NEW.sentiment_label = 'Negative' THEN
        sentiment_column := 'negative_count';
    ELSE
        RAISE EXCEPTION 'Invalid sentiment label: %', NEW.sentiment_label;
    END IF;

    -- Insert or update aggregate by platform
    EXECUTE format($f$
        INSERT INTO brand_platform_aggregates (brand_id, platform, date, %I, total_reach)
        VALUES ($1, $2, $3, 1, $4)
        ON CONFLICT (brand_id, platform, date) DO UPDATE
        SET %I = brand_platform_aggregates.%I + 1,
            total_reach = brand_platform_aggregates.total_reach + EXCLUDED.total_reach
    $f$, sentiment_column, sentiment_column, sentiment_column)
    USING post_data.brand_id, post_data.platform, post_data.post_date, COALESCE(post_data.reach_estimate, 0);

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;





