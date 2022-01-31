DROP MATERIALIZED VIEW IF EXISTS heroagg_prepatch;
CREATE MATERIALIZED VIEW heroagg_prepatch AS (
	WITH agg AS (
		SELECT heroid,
		COUNT(*) AS times_chosen, 
		AVG(m.depth) AS avg_depth, 
		AVG(p.isvictory::int) AS winrate
		FROM players AS p
		JOIN matches m ON p.matchid = m.id
        WHERE m.startdatetime < to_timestamp(1642542300)
		GROUP BY heroid
	)
	SELECT *,
	ROUND(agg.winrate * 100, 2) AS rounded_winrate,
	ROUND (agg.avg_depth, 2) AS rounded_avg_depth,
	RANK() OVER(ORDER BY winrate DESC) wr_rank,
	RANK() OVER(ORDER BY avg_depth DESC) depth_rank,
	RANK() OVER(ORDER BY times_chosen DESC) popularity_rank
	FROM agg
	JOIN const_heroes AS const_h ON agg.heroid = const_h.id
);
CREATE UNIQUE INDEX ON heroagg_prepatch(heroid);