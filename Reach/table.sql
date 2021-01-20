PRAGMA TABLE_INFO('food_order');

ALTER TABLE delivery_info ADD COLUMN password TEXT;

DROP TABLE delivery_info;

CREATE TABLE delivery_info(
    del_id integer PRIMARY KEY AUTOINCREMENT,
    del_name text,
    del_phone integer,
    del_password text,
    del_location text
);