SELECT DISTINCT(id)
FROM (SELECT id
      FROM (SELECT id,
                   xe != xs AND ye != ys AND
                   (LEAST((yr - ys) * (xe - xs), (yl - ys) * (xe - xs)) <= (xl - xs) * (ye - ys) AND (xl - xs) * (ye - ys) <= GREATEST((yr - ys) * (xe - xs), (yl - ys) * (xe - xs)) AND LEAST(xs, xe) <= xl AND xl <= GREATEST(xs, xe) OR
                   LEAST((yr - ys) * (xe - xs), (yl - ys) * (xe - xs)) <= (xr - xs) * (ye - ys) AND (xr - xs) * (ye - ys) <= GREATEST((yr - ys) * (xe - xs), (yl - ys) * (xe - xs)) AND LEAST(xs, xe) <= xr AND xr <= GREATEST(xs, xe) OR
                   LEAST((xl - xs) * (ye - ys), (xr - xs) * (ye - ys)) <= (yl - ys) * (xe - xs) AND (yl - ys) * (xe - xs) <= GREATEST((xl - xs) * (ye - ys), (xr - xs) * (ye - ys)) AND LEAST(ys, ye) <= yl AND yl <= GREATEST(ys, ye) OR
                   LEAST((xl - xs) * (ye - ys), (xr - xs) * (ye - ys)) <= (yr - ys) * (xe - xs) AND (yr - ys) * (xe - xs) <= GREATEST((xl - xs) * (ye - ys), (xr - xs) * (ye - ys)) AND LEAST(ys, ye) <= yr AND yr <= GREATEST(ys, ye))
                   OR xe = xs AND xs = xl AND LEAST(ys, ye) < yr AND GREATEST(ys, ye) > yl
                   OR xe = xs AND xs = xr AND LEAST(ys, ye) < yr AND GREATEST(ys, ye) > yl
                   OR ye = ys AND ys = yr AND LEAST(xs, xe) < xl AND GREATEST(xs, xe) > xr
                   OR ye = ys AND ys = yl AND LEAST(xs, xe) < xl AND GREATEST(xs, xe) > xr as intersects
            FROM (SELECT id,
                         begin_x     as xs,
                         begin_y     as ys,
                         end_x       as xe,
                         end_y       as ye,
                         _X_RIGHT_   as xr,
                         _Y_BOTTOM_  as yr,
                         _X_LEFT_    as xl,
                         _Y_TOP_     as yl
                  FROM (SELECT id, begin_x, begin_y, end_x, end_y FROM lines UNION SELECT id, begin_x, begin_y, end_x, end_y FROM polygons) as s4) as s) as s2
      WHERE s2.intersects
      UNION
      SELECT objects.id
      FROM objects
      LEFT JOIN points p on objects.id = p.id
      LEFT JOIN lines l on objects.id = l.id
      LEFT JOIN polygons pg on objects.id = pg.id
      WHERE
            p.x <= _X_RIGHT_ AND p.x >= _X_LEFT_ AND
            p.y <= _Y_TOP_ AND p.y >= _Y_BOTTOM_ OR
            l.begin_x <= _X_RIGHT_ AND l.begin_x >= _X_LEFT_ AND
            l.begin_y <= _Y_TOP_ AND l.begin_y >= _Y_BOTTOM_ OR
            l.end_x <= _X_RIGHT_ AND l.end_x >= _X_LEFT_ AND
            l.end_y <= _Y_TOP_ AND l.end_y >= _Y_BOTTOM_ OR
            pg.begin_x <= _X_RIGHT_ AND pg.begin_x >= _X_LEFT_ AND
            pg.begin_y <= _Y_TOP_ AND pg.begin_y >= _Y_BOTTOM_ OR
            pg.end_x <= _X_RIGHT_ AND pg.end_x >= _X_LEFT_ AND
            pg.end_y <= _Y_TOP_ AND pg.end_y >= _Y_BOTTOM_
) as s3
;