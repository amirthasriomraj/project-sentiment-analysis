CREATE TRIGGER trg_update_brand_aggregates
AFTER INSERT ON sentiment_results
FOR EACH ROW
EXECUTE FUNCTION update_brand_aggregates();


CREATE TRIGGER trg_update_brand_platform_aggregates
AFTER INSERT ON sentiment_results
FOR EACH ROW
EXECUTE FUNCTION update_brand_platform_aggregates();
