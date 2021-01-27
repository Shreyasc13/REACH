PRAGMA TABLE_INFO('food_order');

ALTER TABLE delivery_info ADD COLUMN email TEXT;

drop TABLE volunteer;

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

CREATE TABLE volunteer(
    v_id integer PRIMARY KEY AUTOINCREMENT,
    f_name text,
    l_name text,
    phone_no integer UNIQUE,
    password text NOT NULL,
    org_name text,
    org_location text,
    email text);