DROP TABLE IF EXISTS abilityagg_3d;
CREATE TABLE abilityagg_3d AS (
	WITH ability_wr AS (
		SELECT p.selectedrewardabilityid, AVG(m.didwin::int) AS wr, COUNT(*) AS total_picks
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		WHERE m.startdatetime > (CURRENT_DATE - INTERVAL '3 days')
		GROUP BY p.selectedrewardabilityid
	), ability_clear_time AS (
		SELECT p.selectedrewardabilityid, AVG(m.durationSeconds::int) AS clear_time, COUNT(*) AS num_clears
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		WHERE m.didwin = true AND m.startdatetime > (CURRENT_DATE - INTERVAL '3 days')
		GROUP BY p.selectedrewardabilityid
	)
	SELECT
	c_exc.texturename AS icon,
	c_cust_ab.displayname AS ability_name,
	REGEXP_REPLACE(c_exc.description, '\*\*(.*?)\*\*', '<strong>\1</strong>', 'gm') AS description,
	ROUND (ab_wr.wr * 100, 2) AS winrate,
	ROUND (ab_ct.clear_time) * interval '1 sec' AS avg_clear_time,
	ab_ct.num_clears AS total_clears,
	ab_wr.total_picks	
	FROM ability_wr ab_wr 
	JOIN ability_clear_time ab_ct USING(selectedrewardabilityid)
	JOIN const_customAbilites c_cust_ab ON ab_wr.selectedrewardabilityid = c_cust_ab.id
	LEFT JOIN const_extractedAbilities c_exc USING(name)
	WHERE c_cust_ab.name LIKE '%special%'
	ORDER BY winrate DESC
);
SELECT * FROM abilityagg_3d LIMIT 10;