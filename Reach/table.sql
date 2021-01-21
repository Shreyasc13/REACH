PRAGMA TABLE_INFO('food_order');

ALTER TABLE food_order ADD COLUMN satatus INTEGER;

DROP TABLE delivery_info;

CREATE TABLE delivery_info(
    del_id integer PRIMARY KEY AUTOINCREMENT,
    del_name text,
    del_phone integer,
    del_password text,
    del_location text
);

ALTER TABLE food_order RENAME COLUMN satatus TO status;

UPDATE food_order SET status='1' where d_id='2';