USE miRNA;

-- query 1
SELECT DISTINCT gid, g.name
FROM   miRNA m JOIN targets USING (mid) JOIN gene g USING (gid)
WHERE  m.name LIKE '%let-7c%' AND
        gid NOT IN (SELECT gid
                             FROM targets join miRNA USING (mid)
                             WHERE name LIKE '%miR-16%');

-- query 2
SELECT mid, name, COUNT(mid) as c
FROM miRNA JOIN targets USING (mid)
GROUP BY mid
ORDER BY COUNT(*) DESC
LIMIT 10;

-- query 3
SELECT  m1.mid, m1.name, m2.mid, m2.name, COUNT(*) AS common_count
FROM  miRNA m1 JOIN targets t1 USING (mid) JOIN targets t2 USING (gid) JOIN
        miRNA m2 ON t2.mid = m2.mid
WHERE t1.mid < t2.mid
GROUP BY t1.mid, t2.mid
ORDER BY common_count DESC
LIMIT 10;

-- query 4
SELECT COUNT(DISTINCT mid)
FROM targets
WHERE score < -0.6;
