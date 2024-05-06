
-- Copyright 2024 John Hanley. MIT licensed.

SELECT COUNT(*) FROM owner;
SELECT COUNT(*) FROM apn_address;

.mode markdown

SELECT * FROM (
  SELECT a.apn,
         a.situs_addr,
         CONCAT(o.address, ', ', o.city) AS addr
  FROM apn_address a
  JOIN owner o  ON o.apn = a.apn
)
WHERE situs_addr != addr
;
