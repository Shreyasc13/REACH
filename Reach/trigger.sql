CREATE TRIGGER update_status AFTER INSERT ON transactions
BEGIN UPDATE food_order SET status=0 WHERE f_id=new.f_id and d_id=new.d_id;
END;

select * from food_order;