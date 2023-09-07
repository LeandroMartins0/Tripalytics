-- Question: From the two most commonly appearing regions, which is the latest datasource?
WITH TopTwoRegions AS (
    -- Calculate the two most commonly appearing regions
    SELECT region, COUNT(id) AS region_count
    FROM trips
    GROUP BY region
    ORDER BY region_count DESC
    LIMIT 2
)

-- Find the latest datasource for each of the top two regions
SELECT ttr.region, MAX(t.datetime) AS latest_datetime
FROM trips AS t
JOIN TopTwoRegions AS ttr
ON t.region = ttr.region
GROUP BY ttr.region;

-- Question: What regions has the "cheap_mobile" datasource appeared in?
-- Find the distinct regions where the datasource is "cheap_mobile"
SELECT DISTINCT region
FROM trips
WHERE datasource = 'cheap_mobile';
