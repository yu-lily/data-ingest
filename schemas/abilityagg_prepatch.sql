DROP MATERIALIZED VIEW IF EXISTS abilityagg_prepatch;
CREATE MATERIALIZED VIEW abilityagg_prepatch AS (
	WITH ability_wr AS (
		SELECT p.selectedrewardabilityid, AVG(m.didwin::int) AS wr, COUNT(*) AS total_picks
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		WHERE m.startdatetime < to_timestamp(1642542300)
		GROUP BY p.selectedrewardabilityid
	), ability_clear_time AS (
		SELECT p.selectedrewardabilityid, AVG(m.durationSeconds::int) AS clear_time,
			MIN(m.durationSeconds::int) AS fastest_clear, COUNT(*) AS num_clears
		FROM playerdepthlist AS p
		JOIN matches m ON p.matchid = m.id
		WHERE m.didwin = true AND m.startdatetime < to_timestamp(1642542300)
		GROUP BY p.selectedrewardabilityid
	)
	SELECT
	c_cust_ab.name,
	c_exc.texturename AS icon,
	c_cust_ab.displayname AS shard,
	REGEXP_REPLACE(c_exc.description, '\*\*(.*?)\*\*', '<strong>\1</strong>', 'gm') AS description,
	ROUND (ab_wr.wr * 100, 2) AS winrate,
	ab_ct.num_clears AS clears,
	ab_wr.total_picks AS picks,
	ROUND (ab_ct.clear_time) * interval '1 sec' AS speed
	--ROUND (ab_ct.fastest_clear) * interval '1 sec' AS fastest_clear_time
	FROM ability_wr ab_wr 
	JOIN ability_clear_time ab_ct USING(selectedrewardabilityid)
	JOIN const_customAbilites c_cust_ab ON ab_wr.selectedrewardabilityid = c_cust_ab.id
	LEFT JOIN const_extractedAbilities c_exc USING(name)
	WHERE c_cust_ab.name LIKE '%special%'
	ORDER BY winrate DESC
);
CREATE UNIQUE INDEX ON abilityagg_prepatch(name);