DROP TABLE IF EXISTS abilityagg;
CREATE TABLE abilityagg AS (
	WITH ability_wr AS (
		SELECT p.selectedrewardabilityid, AVG(m.didwin::int) AS wr
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		GROUP BY p.selectedrewardabilityid
	), ability_clear_time AS (
		SELECT p.selectedrewardabilityid, AVG(m.durationSeconds::int) AS clear_time, COUNT(*) AS num_clears
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		WHERE m.didwin = true
		GROUP BY p.selectedrewardabilityid
	)
	SELECT 
	c_cust_ab.id AS ability_id,
	ROUND (ab_wr.wr * 100, 2) AS ability_wr,
	ROUND (ab_ct.clear_time) * interval '1 sec' AS clear_time,
	ab_ct.num_clears,
	c_cust_ab.name,
	REPLACE(c_cust_ab.abilityname, 'aghsfort_', ''),
	c_cust_ab.displayname,
	c_cust_ab.description
	FROM ability_wr ab_wr 
	JOIN ability_clear_time ab_ct USING(selectedrewardabilityid)
	JOIN const_customAbilites c_cust_ab ON ab_wr.selectedrewardabilityid = c_cust_ab.id
	ORDER BY clear_time ASC
);
SELECT * FROM abilityagg LIMIT 10;