WITH ab_combinations AS (
	SELECT matchid, playerslot, p.depth, selectedrewardabilityid, m.didWin, m.depth AS depth_reached
	FROM playerdepthlist AS p
	JOIN const_customAbilites c_cust_ab ON p.selectedrewardabilityid = c_cust_ab.id
	LEFT JOIN const_extractedAbilities c_exc USING(name)
	JOIN matches m ON p.matchid = m.id
	WHERE c_cust_ab.name LIKE '%special%'
)

SELECT ab_sets, COUNT(*), AVG(wr), AVG(avg_depth)
FROM (
	SELECT array_agg(ab_combinations.selectedrewardabilityid) ab_sets, AVG(didwin::int) AS wr, AVG(depth_reached) AS avg_depth
	FROM ab_combinations
	GROUP BY matchid, playerslot
	HAVING count(*) > 1
) AS b
GROUP BY ab_sets
ORDER BY count DESC;