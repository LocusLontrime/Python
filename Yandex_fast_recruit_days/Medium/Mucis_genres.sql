WITH cte AS
(
  SELECT g.*, g.Id AS child_id
  FROM genre as g
  UNION ALL
  SELECT i.*, c.child_id
  FROM genre i
   JOIN cte AS c ON c.parent_genre_id = i.id
)
SELECT DISTINCT t.id as track_id
, g.id as genre_id
, t.name as track_name
, g.name AS genre_name
  FROM cte as g
  JOIN track_genre as tg ON tg.genre_id = g.child_id
  JOIN track AS t ON t.id = tg.track_id
  ORDER BY t.id, g.id