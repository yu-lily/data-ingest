DROP MATERIALIZED VIEW IF EXISTS heroagg_3d;
CREATE MATERIALIZED VIEW heroagg_3d AS (
	WITH agg AS (
		SELECT heroid,
		COUNT(*) AS times_chosen, 
		AVG(m.depth) AS avg_depth, 
		AVG(p.isvictory::int) AS winrate
		FROM players AS p
		JOIN matches m ON p.matchid = m.id
        WHERE m.startdatetime > (CURRENT_DATE - INTERVAL '3 days')
		GROUP BY heroid
	)
	SELECT *,
	ROUND(agg.winrate * 100, 2) AS rounded_winrate,
	ROUND (agg.avg_depth * 100, 2) AS rounded_avg_depth
	FROM agg
	JOIN const_heroes AS const_h ON agg.heroid = const_h.id
);