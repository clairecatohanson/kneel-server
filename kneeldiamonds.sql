-- Run this block to delete and reinitialize the database 
DELETE FROM 'Metals';
DELETE FROM 'Sizes';
DELETE FROM 'Styles';
DELETE FROM 'Orders';

DROP TABLE IF EXISTS 'Metals';
DROP TABLE IF EXISTS 'Sizes';
DROP TABLE IF EXISTS 'Styles';
DROP TABLE IF EXISTS 'Orders';
-- End Block


-- Run this block to seed the database
CREATE TABLE 'Metals' (
'id' INTEGER PRIMARY KEY AUTOINCREMENT, 
'metal' NVARCHAR(160) NOT NULL, 
'price' NUMERIC(5,2) NOT NULL);

CREATE TABLE 'Sizes' (
'id' INTEGER PRIMARY KEY AUTOINCREMENT,
'carats' NUMERIC (4,2) NOT NULL,
'price' NUMERIC(6,2) NOT NULL);

CREATE TABLE 'Styles' (
'id' INTEGER PRIMARY KEY AUTOINCREMENT,
'style' NVARCHAR(160) NOT NULL,
'price' NUMERIC(5,2) NOT NULL);

CREATE TABLE 'Orders' (
'id' INTEGER PRIMARY KEY AUTOINCREMENT, 
'metal_id' INTEGER NOT NULL,
'size_id' INTEGER NOT NULL,
'style_id' INTEGER NOT NULL,
'timestamp' INTEGER NOT NULL,
FOREIGN KEY('metal_id') REFERENCES 'Metals'('id'),
FOREIGN KEY('size_id') REFERENCES 'Sizes'('id'),
FOREIGN KEY('style_id') REFERENCES 'Styles'('id'));

INSERT INTO 'Metals' (metal, price) VALUES ("Sterling Silver", 75.00);
INSERT INTO 'Metals' (metal, price) VALUES ("14K Gold", 250.00);
INSERT INTO 'Metals' (metal, price) VALUES ("24K Gold", 424.99);
INSERT INTO 'Metals' (metal, price) VALUES ("Platinum", 739.99);

INSERT INTO 'Sizes' (carats, price) VALUES (0.5, 405.25);
INSERT INTO 'Sizes' (carats, price) VALUES (0.75, 782.12);
INSERT INTO 'Sizes' (carats, price) VALUES (1.0, 1270);
INSERT INTO 'Sizes' (carats, price) VALUES (1.5, 1997.79);
INSERT INTO 'Sizes' (carats, price) VALUES (2.0, 3600.00);

INSERT INTO 'Styles' (style, price) VALUES ("Classic", 250.00);
INSERT INTO 'Styles' (style, price) VALUES ("Modern", 500.00);
INSERT INTO 'Styles' (style, price) VALUES ("Vintage", 850.00);

INSERT INTO 'Orders' (metal_id, size_id, style_id, timestamp) VALUES (1, 1, 1, datetime());
INSERT INTO 'Orders' (metal_id, size_id, style_id, timestamp) VALUES (2, 3, 2, datetime());
INSERT INTO 'Orders' (metal_id, size_id, style_id, timestamp) VALUES (3, 3, 1, datetime());
INSERT INTO 'Orders' (metal_id, size_id, style_id, timestamp) VALUES (4, 5, 3, datetime());
-- End Block

SELECT o.id, o.metal_id, o.size_id, o.style_id, o.timestamp, m.id AS metalId, m.metal, m.price AS metalPrice, si.id AS sizeId, si.carats, si.price AS sizePrice, st.id AS styleId, st.style, st.price AS stylePrice FROM Orders o
JOIN Metals m ON o.metal_id = m.id
JOIN Sizes si ON o.size_id = si.id
JOIN Styles st ON o.style_id = st.id
WHERE o.id = 3