from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import datetime
import sqlite3
from PIL import Image, ImageTk
import smtplib
import re




root = Tk()
root.state('zoomed') 
root['bg'] = 'white'
bg1=PhotoImage(file='food5.png')
submit_path = Image.open('icons\submit.png')
submit = ImageTk.PhotoImage(submit_path)

con=sqlite3.connect('reach2.db')
cur=con.cursor()

# *****************Add info**************************


#registration and login DATABASE

#MAIL function
def mail(del_id,volunteer_id,donor_id,food_id):

    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()

        print(del_id,volunteer_id,donor_id,food_id)

        cur.execute("SELECT f_name,l_name,phone_no from donor where d_id=?",(donor_id,))
        donor_details=cur.fetchall()[0]
        
        d_namef=donor_details[0]
        d_namel=donor_details[1]
        d_phone=donor_details[2]
        d_name=d_namef+" "+d_namel

        print(d_name,d_namel,d_phone)
        # print(donor_details)

        cur.execute("SELECT f_name,l_name,phone_no,org_name,org_location from volunteer where v_id=?",(volunteer_id,))
        volunteer_details=cur.fetchall()[0]
        # print(volunteer_details)
        v_namef=volunteer_details[0]
        v_namel=volunteer_details[1]
        v_phone=volunteer_details[2]
        v_org_name=volunteer_details[3]
        v_org_loc=volunteer_details[4]
        v_name=v_namef+" "+v_namel

        print(v_name,v_phone,v_org_name,v_org_loc)

        cur.execute("SELECT f_location,pin_code from food_order where f_id=?",(food_id,))
        food_details=cur.fetchall()[0]
        # print(food_details)
        del_loc=food_details[0]
        del_pin=food_details[1]
        print(del_loc,del_pin)        


        cur.execute("SELECT email from delivery_info where del_id=?",(del_id,))
        send_email=cur.fetchone()[0]
        print(send_email)

        subject = "New delivery order"

        order="Donor name:"+d_name+"\n"+"Donor phone no.:"+str(d_phone)+"\n"+"Pickup location:"+del_loc+" "+str(del_pin)+"\n"+"Volunteer name:"+v_name+"\n"+"Volunteer phone no.:"+str(v_phone)+"\n"+"Drop off location:"+v_org_name+"\n"+v_org_loc

        # print(order)

        msg = f"Subject:{subject}\n\n{order}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        #INSERT YOUR E-MAIL ID AND PASSWORD
        server.login("reach.donate@gmail.com", "qJ6G3x1vknRX")
        server.sendmail("shreyasc.cs18@sahyadri.edu.in",send_email, msg)

        server.quit()

        messagebox.showinfo("Message Sent", "Message Sent Successfully")

def register_db(selection,fname,lname,phone,password,org_name,location,email):

    con=sqlite3.connect('reach2.db')
    cur=con.cursor()

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if(re.search(regex,email)):  
        print("Valid Email")  
            
    else:  
        messagebox.showwarning('INDEX ERROR','Enter a valid email.')
    
    cur.execute('SELECT phone_no from donor')
    volunteer_phone_no=cur.fetchall()
    cur.execute('SELECT phone_no from volunteer')
    donor_phone_no=cur.fetchall()
    cur.execute('SELECT del_phone from delivery_info')
    delivery_phone_no=cur.fetchall()

    # print(password.isnumeric())

    # phone=int(phone)

    if phone.isnumeric()==True:
        print('valid phone')
    else:
        messagebox.showwarning('INDEX ERROR','Enter a valid phone no.')
        return

    if len(phone)!=10 :
        messagebox.showwarning('INDEX ERROR','Enter a valid 10 digit phone no')
        return

    print(selection,fname,lname,phone,password)
    if selection=="D":
        if fname=='' or lname=='' or phone=='' or password=='':
            messagebox.showwarning('INDEX ERROR', 'Enter all the details.')

        elif int(phone) in [x[0] for x in donor_phone_no]:
            messagebox.showinfo('INDEX ERROR','You already have an account')

        else:
            cur.execute("INSERT INTO donor (f_name,l_name,phone_no,password,email) VALUES (?,?,?,?,?)",(fname,lname,phone,password,email))
            messagebox.showinfo('Registration','Registered successfully.')

        
       
    elif selection=="V":
        # print([x[0] for x in volunteer_phone_no])
        if fname=='' or lname=='' or phone=='' or password=='' or org_name=='' or location=='':
            messagebox.showwarning('INDEX ERROR', 'Enter all the details')

        elif int(phone) in [x[0] for x in volunteer_phone_no]:
            messagebox.showinfo('INDEX ERROR','You already have an account.')

        else:
            cur.execute("INSERT INTO volunteer (f_name,l_name,phone_no,password,org_name,org_location,email) VALUES (?,?,?,?,?,?,?)",(fname,lname,phone,password,org_name,location,email))
            messagebox.showinfo('Registration','Registered as volunteer successfully.')

    elif selection=="DL":
        if fname=='' or phone=='' or password=='' or location=='':
            messagebox.showwarning('INDEX ERROR', 'Enter all the details')

        elif int(phone) in [x[0] for x in delivery_phone_no]:
            messagebox.showinfo('INDEX ERROR','You already have an account.')


        else:
            cur.execute("INSERT INTO delivery_info(del_name,del_phone,del_password,del_location,email) VALUES(?,?,?,?,?)",(fname,phone,password,location,email))
            messagebox.showinfo('Registration','Registered as delivery rep successfully.')


    con.commit()
    con.close()

def food_db(d_id,food_type,foodname,quantity,address,pin):


    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        address=address.rstrip("\n")
        address=address.rstrip("\t")

        if foodname=='' or quantity=='' or address=='' or pin=='':
            messagebox.showinfo('INDEX ERROR', 'Enter the Food details.')
        else:

            values=(d_id,food_type,foodname,quantity,address,pin,'1')
            print(values)
            cur.execute("INSERT INTO food_order(d_id,f_type,f_name,quantity,f_location,pin_code,status) VALUES (?,?,?,?,?,?,?)",(d_id,food_type,foodname,quantity,address,pin,1))
            messagebox.showinfo('INDEX ERROR', 'Thank you for donating.')

def transaction_db(volunteer_id,food_id,delivery_id):
        with sqlite3.connect('reach2.db') as con:
            cur=con.cursor()



            cur.execute("SELECT d_id from food_order where f_id=?", (food_id,))
            donor_id=cur.fetchall()[0][0]
            print(donor_id)
            date_time=str(datetime.datetime.now())
            # print(date_time)
            # print(type(date_time))
            dat, t = date_time.split(" ")
            print(dat)
            t = t.split(".")[0]
            print(t)

            date_time = " ".join((dat, t))
            print(date_time)
            
            cur.execute("INSERT INTO transactions(date_time,d_id,v_id,f_id,del_id) VALUES (?,?,?,?,?)",(date_time,donor_id,volunteer_id,food_id,delivery_id))

            messagebox.showinfo('INDEX ERROR','Thank you, your order has been placed')

            mail(delivery_id,volunteer_id,donor_id,food_id)

            cur.execute("UPDATE food_order SET status=? where f_id=? and d_id=?",(0,food_id,donor_id))

            # cur.execute("""
            #     CREATE TRIGGER update_status AFTER INSERT ON transactions
            #     BEGIN UPDATE food_order SET status=0 WHERE f_id=new.f_id and d_id=new.d_id;
            #     END
            # """)


def update_food_db(f_id,d_id,food_type,foodname,quantity,address,pin):


    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        address=address.rstrip("\n")
        address=address.rstrip("\t")
        if f_id=='':
            messagebox.showwarning('INDEX ERROR', 'Enter the Food ID you want to update.')
        else:   
            values=(food_type,foodname,quantity,address,pin)
            # print(values)
            cur.execute("UPDATE food_order SET f_type=?,f_name=?,quantity=?,f_location=?,pin_code=? where f_id=? and d_id=?",(food_type,foodname,quantity,address,pin,f_id,d_id))
            messagebox.showinfo('INDEX ERROR', 'Updated successfully.')

            # donor_dash(d_id)
            
def donor_dash(d_id):
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        global donor_dash_frame
        donor_id=d_id

        # print(donor_id)

        dash_win=Toplevel(root)
        donor_dash_frame=Frame(dash_win,bg='light blue',borderwidth=5,padx=20,pady=20)

        donor_dash_frame.pack()    

        head_label = Label(donor_dash_frame, text="Dashboard ",background="#0A79DF",fg="white",width=60,padx=10,pady=10,anchor=W)
        head_label.config(font=("Bold",30))


        head_label.grid(row=0,column=0,columnspan=5,padx=5,pady=5,sticky=W)

        cur.execute("SELECT f_id,f_type,f_name,quantity,f_location,pin_code FROM food_order WHERE d_id=? and status=?",(donor_id,'1',))
        dd=cur.fetchall()
        # print(dd)

        headers=['Food Id','Food Type','Food Name','Quantity','Location','Pin Code']
        
        for j in range(6):
            e = Entry(donor_dash_frame, width=20, borderwidth=2, bg="#7f8c8d", fg='white', highlightthickness=2)
            e.config(highlightbackground = "#900C3F", highlightcolor= "#900C3F", relief=FLAT)
            e.grid(row=1, column=j, padx=10, pady=2)
            e.insert(END, headers[j])


        for i in range(len(dd)):
            for j in range(0,6):

                e = Entry(donor_dash_frame, width=20, borderwidth=2, highlightthickness=2)
                e.config(highlightbackground = "red", highlightcolor= "red", relief=FLAT)
                e.grid(row=i+2, column=j, padx=10, pady=2)
                e.insert(END, dd[i][j])
              

        #food ID widget
        food_id_label = Label(donor_dash_frame,text="Selected Food  Id", padx=20, pady=5, width=17, anchor=W)
        food_id_label.config(font=("Bold",15))
        food_id_label.grid(row=len(dd)+4, column=0, padx=10, pady=2)
        food_id_entry = Entry(donor_dash_frame,borderwidth=3,width=22)
        food_id_entry.config(font=8)
        food_id_entry.grid(row=len(dd)+4, column=1, padx=10, pady=2)


        button_edit = Button(donor_dash_frame,text="Edit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:update_food(food_id_entry.get(),d_id))
        button_edit.config(font=("Helvetica", 12))
        button_edit.grid(row=len(dd)+4, column=2, columnspan=3, padx=20, pady=20) 

        button_delete = Button(donor_dash_frame,text="Delete",padx=32,pady=9,fg="white",background="red",borderwidth=2,relief=RAISED, command=lambda:delete_food(food_id_entry.get()))
        button_delete.config(font=("Helvetica", 12))
        button_delete.grid(row=len(dd)+4, column=3, columnspan=3, padx=20, pady=20) 

        button_donate = Button(donor_dash_frame,text="Donate",padx=32,pady=9,fg="white",background="blue",borderwidth=2,relief=RAISED, command=lambda:donor(donor_id))
        button_donate.config(font=("Helvetica", 15))
        button_donate.grid(row=len(dd)+5, column=0, columnspan=3, padx=20, pady=20) 

def update_food(f_id,d_id):
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        global donor_dash_frame
        update_food_win=Toplevel(root)
        # print(d_id)

        if f_id=='':
            messagebox.showwarning('INDEX ERROR', 'Enter the Food ID you want to delete.')
        else:        

            cur.execute("SELECT f_id,f_type,f_name,quantity,f_location,pin_code FROM food_order WHERE f_id=?",(f_id,))
            uf=cur.fetchall()

            food_id=f_id
            global update_food_frame

            update_food_frame = Frame(update_food_win, bg='blue', borderwidth=5, padx=20, pady=20)

            if uf[0][1]=='Veg':
                m='Non-Veg'
            else:
                m='Veg'

            # print(m)
            update_food_frame.pack()
            #Food type widget
            food_type_label = Label(update_food_frame,text="Food Type", padx=5, pady=5, width=17, anchor=W)
            food_type_label.config(font=("Bold",15))
            food_type_label.grid(row=1,column=0, padx=(15,30), pady=15, sticky=W)

            food_type_combo=ttk.Combobox(update_food_frame,font=("Bold",13))
            food_type_combo['values']=(uf[0][1],m)
            food_type_combo.current('0')
            food_type_combo.grid(row=1,column=1, padx=15,sticky=E)



            #food name widget
            food_name_label = Label(update_food_frame,text="Food Name/Category", padx=5, pady=5, width=17, anchor=W)
            food_name_label.config(font=("Bold",15))
            food_name_label.grid(row=2,column=0, padx=15, pady=15, sticky=W)

            food_name_entry = Entry(update_food_frame,borderwidth=3,width=22)
            food_name_entry.config(font=8)
            food_name_entry.grid(row=2,column=1, padx=15,sticky=E)
            food_name_entry.insert(END,uf[0][2])
        

            #food quantity widget
            quantity_label = Label(update_food_frame,text="Quantity", padx=5, pady=5, width=17, anchor=W)
            quantity_label.config(font=("Bold",15))
            quantity_label.grid(row=3,column=0, padx=15, pady=15, sticky=W)

            quantity_entry = Entry(update_food_frame,borderwidth=3,width=22)
            quantity_entry.config(font=8)
            quantity_entry.grid(row=3,column=1, padx=15,sticky=E)
            quantity_entry.insert(END,uf[0][3])

            #city widget
            city_label = Label(update_food_frame,text="Address", padx=5, pady=5, width=17, anchor=W)
            city_label.config(font=("Bold",15))
            city_label.grid(row=4,column=0, padx=15, pady=15, sticky=W)
            
            city_entry = Text(update_food_frame,borderwidth=3,width=22,height=4)
            city_entry.config(font=8)
            city_entry.grid(row=4,column=1, padx=15,sticky=E)
            city_entry.insert(END,uf[0][4])

            #pin code widget
            pin_code_label = Label(update_food_frame,text="Pin code", padx=5, pady=5, width=17, anchor=W)
            pin_code_label.config(font=("Bold",15))
            pin_code_label.grid(row=5,column=0, padx=15, pady=15, sticky=W)

            pin_code_entry = Entry(update_food_frame,borderwidth=3,width=22)
            pin_code_entry.config(font=8)
            pin_code_entry.grid(row=5,column=1, padx=15,sticky=E)
            pin_code_entry.insert(END,uf[0][5])
            

            donor_submit = Button(update_food_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda: update_food_db(food_id,d_id,food_type_combo.get(), food_name_entry.get(), quantity_entry.get(), city_entry.get("1.0",END), pin_code_entry.get()))
            donor_submit.config(font=("Helvetica", 15))
            donor_submit.grid(row=7, column=0, columnspan=3, padx=20, pady=20)

def delete_food(f_id):
        with sqlite3.connect('reach2.db') as con:
            cur=con.cursor()

            food_details=cur.execute("SELECT * FROM food_order where f_id=?",(f_id,)).fetchall()
            food_id=food_details[0][0]
            d_id=food_details[0][1]
            f_type=food_details[0][2]
            f_name=food_details[0][3]
            quantity=food_details[0][4]
            f_location=food_details[0][5]
            pin_code=food_details[0][6]
            status=food_details[0][7]


            if f_id=='':
                messagebox.showwarning('INDEX ERROR', 'Enter the Food ID you want to delete.')
            else:
                cur.execute("DELETE FROM food_order where f_id=?",(f_id,))
                print(food_details[0][0])
                messagebox.showinfo('INDEX ERROR', 'Deleted successfully.')

                # cur.execute("""CREATE TRIGGER after_delete AFTER DELETE ON food_order 
                # BEGIN 
                # INSERT INTO delete_log(f_id,d_id,f_type,f_name,quantity,f_location,pin_code) VALUES(food_id,d_id,f_type,f_name,quantity,f_location,pin_code,status); 
                # END
                # """)



def volunteer(v_id):
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()

        volunteer_win=Toplevel(root)
        volunteer_frame=Frame(volunteer_win,bg='light blue',borderwidth=5,padx=20,pady=20)

        volunteer_frame.pack()

        cur.execute("SELECT f_id,f_type,f_name,quantity,f_location,pin_code FROM food_order WHERE status=?",('1'))
        fd=cur.fetchall()
        # print(fd)

        cur.execute("SELECT * from delivery_info")
        di=cur.fetchall()
        # print(di)

        volunteer_id=v_id

        head_label = Label(volunteer_frame, text="Food",background="#0A79DF",fg="white",width=10,padx=14,pady=10,anchor=W)
        head_label.config(font=("Bold",15))
        head_label.grid(row=0,rowspan=1,column=2,columnspan=1,padx=10, pady=2)

        #food ID widget
        food_id_label = Label(volunteer_frame,text="Selected Food  Id", padx=20, pady=5, width=17, anchor=W)
        food_id_label.config(font=("Bold",15))
        food_id_label.grid(row=2, column=0, padx=10, pady=2)
        food_id_entry = Entry(volunteer_frame,borderwidth=3,width=22)
        food_id_entry.config(font=8)
        food_id_entry.grid(row=2, column=1, padx=10, pady=2)

    

        #delivery id widget
        delivery_id_label = Label(volunteer_frame,text="Selected Delivery Id", padx=20, pady=5, width=17, anchor=W)
        delivery_id_label.config(font=("Bold",15))
        delivery_id_label.grid(row=3, column=0, padx=10, pady=2)

        delivery_id_entry = Entry(volunteer_frame,borderwidth=3,width=22)
        delivery_id_entry.config(font=8)
        delivery_id_entry.grid(row=3, column=1, padx=10, pady=2)

        headers=['Food Id','Food Type','Food Name','Quantity','Loacation','Pin Code']
        
        for j in range(6):
            e = Entry(volunteer_frame, width=20, borderwidth=2, bg="#7f8c8d", fg='white', highlightthickness=2)
            e.config(highlightbackground = "#900C3F", highlightcolor= "#900C3F", relief=FLAT)
            e.grid(row=1, column=j+2, padx=10, pady=2)
            e.insert(END, headers[j])


        for i in range(len(fd)):
            for j in range(6):

                e = Entry(volunteer_frame, width=20, borderwidth=2, highlightthickness=2)
                e.config(highlightbackground = "red", highlightcolor= "red", relief=FLAT)
                e.grid(row=i+2, column=j+2, padx=10, pady=2)
                e.insert(END, fd[i][j])

        head_label = Label(volunteer_frame, text="Delivery",background="#0A79DF",fg="white",width=10,padx=14,pady=10,anchor=W)
        head_label.config(font=("Bold",15))
        head_label.grid(row=len(fd)+2,rowspan=1,column=2,columnspan=1,padx=10, pady=2)

        del_headers=['Delivery ID','Name','Phone','Location']

        m=len(fd)+3 
        for j in range(4):
            e = Entry(volunteer_frame, width=20, borderwidth=2, bg="#7f8c8d", fg='white', highlightthickness=2)
            e.config(highlightbackground = "#900C3F", highlightcolor= "#900C3F", relief=FLAT)
            e.grid(row=m, column=j+2, padx=10, pady=2)
            e.insert(END, del_headers[j])


        for i in range(len(di)):
            for j in range(4):


                e = Entry(volunteer_frame, width=20, borderwidth=2, highlightthickness=2)
                e.config(highlightbackground = "red", highlightcolor= "red", relief=FLAT)
                e.grid(row=i+m+1, column=j+2, padx=10, pady=2)
                if j==3:
                    j+=1
                e.insert(END, di[i][j])

                button_submit = Button(volunteer_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:transaction_db(volunteer_id,food_id_entry.get(),delivery_id_entry.get()))
                button_submit.config(font=("Helvetica", 15))
                button_submit.grid(row=7,rowspan=10, column=0, columnspan=3, padx=20, pady=20)



def donor(d_id):
    donor_win=Toplevel(root)
    # print(d_id)

    donor_id=d_id
    global donor_frame

    donor_frame = Frame(donor_win, bg='blue', borderwidth=5, padx=20, pady=20)

    donor_frame.pack()

    

    #Food type widget
    food_type_label = Label(donor_frame,text="Food Type", padx=5, pady=5, width=17, anchor=W)
    food_type_label.config(font=("Bold",15))
    food_type_label.grid(row=1,column=0, padx=(15,30), pady=15, sticky=W)

    food_type_combo=ttk.Combobox(donor_frame,font=("Bold",13))
    food_type_combo['values']=("Veg","Non-Veg")
    food_type_combo.grid(row=1,column=1, padx=15,sticky=E)



    #food name widget
    food_name_label = Label(donor_frame,text="Food Name/Category", padx=5, pady=5, width=17, anchor=W)
    food_name_label.config(font=("Bold",15))
    food_name_label.grid(row=2,column=0, padx=15, pady=15, sticky=W)

    food_name_entry = Entry(donor_frame,borderwidth=3,width=22)
    food_name_entry.config(font=8)
    food_name_entry.grid(row=2,column=1, padx=15,sticky=E)

  

    #food quantity widget
    quantity_label = Label(donor_frame,text="Quantity", padx=5, pady=5, width=17, anchor=W)
    quantity_label.config(font=("Bold",15))
    quantity_label.grid(row=3,column=0, padx=15, pady=15, sticky=W)

    quantity_entry = Entry(donor_frame,borderwidth=3,width=22)
    quantity_entry.config(font=8)
    quantity_entry.grid(row=3,column=1, padx=15,sticky=E)

    #city widget
    city_label = Label(donor_frame,text="Address", padx=5, pady=5, width=17, anchor=W)
    city_label.config(font=("Bold",15))
    city_label.grid(row=4,column=0, padx=15, pady=15, sticky=W)

    city_entry = Text(donor_frame,borderwidth=3,width=22,height=4)
    city_entry.config(font=8)
    city_entry.grid(row=4,column=1, padx=15,sticky=E)

    #pin code widget
    pin_code_label = Label(donor_frame,text="Pin code", padx=5, pady=5, width=17, anchor=W)
    pin_code_label.config(font=("Bold",15))
    pin_code_label.grid(row=5,column=0, padx=15, pady=15, sticky=W)

    pin_code_entry = Entry(donor_frame,borderwidth=3,width=22)
    pin_code_entry.config(font=8)
    pin_code_entry.grid(row=5,column=1, padx=15,sticky=E)
    
    

    donor_submit = Button(donor_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda: food_db(donor_id,food_type_combo.get(), food_name_entry.get(), quantity_entry.get(), city_entry.get("1.0",END), pin_code_entry.get()))
    donor_submit.config(font=("Helvetica", 15))
    donor_submit.grid(row=7, column=0, columnspan=3, padx=20, pady=20)

def register():
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        register_win=Toplevel(root)
    
        global register_frame,org_name_label,location_label,org_name_entry,location_entry,last_name_label,last_name_entry,last_name_entry
        register_frame = Frame(register_win, bg='blue', borderwidth=5, padx=20, pady=20)
        register_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=40, sticky=N)
    

        def rem_org():
            # org_name_entry['bg']='black'
            # org_location_entry['bg']='black'

            org_name_label['state']='disabled'
            org_name_entry['state']='disabled'
            location_label['state']='disabled'
            location_entry['state']='disabled'
            last_name_label['state']='normal'
            last_name_entry['state']='normal'

        def add_org():
            org_name_label['state']='normal'
            org_name_entry['state']='normal'
            location_label['state']='normal'
            location_entry['state']='normal'
            last_name_label['state']='normal'
            last_name_entry['state']='normal'



        def rem_del():
            org_name_label['state']='disabled'
            org_name_entry['state']='disabled'
            location_label['state']='normal'
            location_entry['state']='normal'

        selection=StringVar()

        #selection widget
        Radiobutton(register_frame, text="Donate",variable=selection, value="D", font=("Bold",12),command=rem_org).grid(row=0,column=0)

        Radiobutton(register_frame, text="Volunteer",variable=selection, value="V", font=("Bold",12),command=add_org).grid(row=0,column=1)

        Radiobutton(register_frame, text="Delivery",variable=selection, value="DL", font=("Bold",12),command=rem_del).grid(row=0,column=2)

        #first name widget
        first_name_label = Label(register_frame,text="First Name", padx=5, pady=5, width=15, anchor=W)
        first_name_label.config(font=("Bold",15))
        first_name_label.grid(row=1,column=0, padx=15, pady=15, sticky=W)

        first_name_entry = Entry(register_frame,borderwidth=3,width=15)
        first_name_entry.config(font=8)
        first_name_entry.grid(row=1,column=1, padx=15,sticky=E)

        #last name widget
        last_name_label = Label(register_frame,text="Last Name", padx=5, pady=5, width=15, anchor=W)
        last_name_label.config(font=("Bold",15))
        last_name_label.grid(row=2,column=0, padx=15, pady=15, sticky=W)

        last_name_entry = Entry(register_frame,borderwidth=3,width=15)
        last_name_entry.config(font=8)
        last_name_entry.grid(row=2,column=1, padx=15,sticky=E)


        #phone number widget
        phone_no_label = Label(register_frame,text="Phone No", padx=5, pady=5, width=15, anchor=W)
        phone_no_label.config(font=("Bold",15))
        phone_no_label.grid(row=4,column=0, padx=15, pady=15, sticky=W)

        phone_entry = Entry(register_frame,borderwidth=3,width=15)
        phone_entry.config(font=8)
        phone_entry.grid(row=4,column=1, padx=15,sticky=E)

        #register password widget
        reg_pasword_label = Label(register_frame,text="Password", padx=5, pady=5, width=15, anchor=W)
        reg_pasword_label.config(font=("Bold",15))
        reg_pasword_label.grid(row=5,column=0, padx=15, pady=15, sticky=W)

        reg_password_entry = Entry(register_frame,show="*",borderwidth=3,width=15)
        reg_password_entry.config(font=8)
        reg_password_entry.grid(row=5,column=1, padx=15,sticky=E)

        #org name widget
        org_name_label = Label(register_frame,text="Organization Name", padx=5, pady=5, width=15, anchor=W)
        org_name_label.config(font=("Bold",15))
        org_name_label.grid(row=6,column=0, padx=15, pady=15, sticky=W)

        org_name_entry = Entry(register_frame,borderwidth=3,width=15)
        org_name_entry.config(font=8)
        org_name_entry.grid(row=6,column=1, padx=15,sticky=E)

        #org location widget
        location_label = Label(register_frame,text="Location", padx=5, pady=5, width=15, anchor=W)
        location_label.config(font=("Bold",15))
        location_label.grid(row=7,column=0, padx=15, pady=15, sticky=W)

        location_entry = Entry(register_frame,borderwidth=3,width=15)
        location_entry.config(font=8)
        location_entry.grid(row=7,column=1, padx=15,sticky=E)

        #org location widget
        email_label = Label(register_frame,text="Email", padx=5, pady=5, width=15, anchor=W)
        email_label.config(font=("Bold",15))
        email_label.grid(row=8,column=0, padx=15, pady=15, sticky=W)

        email_entry = Entry(register_frame,borderwidth=3,width=15)
        email_entry.config(font=8)
        email_entry.grid(row=8,column=1, padx=15,sticky=E)


        

        button_submit = Button(register_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:register_db(selection.get(),first_name_entry.get(),last_name_entry.get(),phone_entry.get(),reg_password_entry.get(),org_name_entry.get(),location_entry.get(),email_entry.get()))
        button_submit.config(font=("Helvetica", 15))
        button_submit.grid(row=9, column=0, columnspan=3, padx=20, pady=20)

    # login frame
def login():
    login_win=Toplevel(root)
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()

        login_frame = Frame(login_win, bg='blue', borderwidth=5, padx=20, pady=20)
        login_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=40, sticky=NSEW)
        
        selection=StringVar()

        #selection widget
        selection_donate=Radiobutton(login_win, text="Donate",variable=selection, value="D", font=("Bold",12))
        selection_donate.grid(row=0,column=0)

        selection_volunteer=Radiobutton(login_win, text="Volunteer",variable=selection, value="V", font=("Bold",12))
        selection_volunteer.grid(row=0,column=1)

        #Reg phone no widget
        reg_phone_label = Label(login_frame,text="Registered phone no.", padx=5, pady=5, width=17, anchor=W)
        reg_phone_label.config(font=("Bold",15))
        reg_phone_label.grid(row=0,column=0, padx=15, pady=15, sticky=W)

        reg_phone_entry = Entry(login_frame,borderwidth=3,width=15)
        reg_phone_entry.config(font=8)
        reg_phone_entry.grid(row=0,column=1, padx=15,sticky=E)

        #login password widget
        log_password_label = Label(login_frame,text="Password", padx=5, pady=5, width=17, anchor=W)
        log_password_label.config(font=("Bold",15))
        log_password_label.grid(row=1,column=0, padx=15, pady=15, sticky=W)

        log_password_entry = Entry(login_frame,show="*",borderwidth=3,width=15)
        log_password_entry.config(font=8)
        log_password_entry.grid(row=1,column=1, padx=15,sticky=E)

        def check(c):
            
        
            # print(c)
            ph=reg_phone_entry.get()
            psw=log_password_entry.get()

            if not ph.isnumeric():
                messagebox.showwarning('INDEX ERROR','Enter a valid phone no.')
                return

            if len(ph)!=10 :
                messagebox.showwarning('INDEX ERROR','Enter a valid 10 digit phone no')
                return
            # print(ph,psw)

            if c=='D':
                cur.execute("SELECT * FROM donor WHERE phone_no=? AND password=?",(ph,psw))
                a=cur.fetchall()
                # print(a)
                if len(a):
                    d_id=cur.execute("SELECT d_id FROM donor WHERE phone_no=? AND password=?",(ph,psw)).fetchone()
                    # print(d_id[0])
                    donor_dash(d_id[0])
                else:
                    messagebox.showerror('error','Wrong credentials')
            elif c=='V':
                cur.execute("SELECT * FROM volunteer WHERE phone_no=? AND password=?",(ph,psw))
                a=cur.fetchall()
                if len(a):
                    v_id=cur.execute("SELECT v_id FROM volunteer WHERE phone_no=? AND password=?",(ph,psw)).fetchone()
                    volunteer(v_id[0])
                else:
                    messagebox.showerror('error','Wrong credentials')
    

        button_submit = Button(login_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:check(selection.get()))
        button_submit.config(font=("Helvetica", 15))
        button_submit.grid(row=7, column=0, columnspan=3, padx=20, pady=20)


head_label = Label(root, text="Reach ",background="#0A79DF",fg="white",width=65,padx=14,pady=10,anchor=W)
head_label.config(font=("Bold",30))


head_label.grid(row=0,column=0,columnspan=5,padx=5,pady=5,sticky=W)

#Landing page
landing_frame=Frame(root)
landing_frame.grid(row=2,column=0,columnspan=8)
label=Label(landing_frame,image=bg1)
label.pack(anchor=NW)

login_btn = Button(landing_frame, text="Login", font=("bold", 18), fg="white", bg="#2ecc72", relief=FLAT,padx=60,pady=20, command=login)
login_btn.place(x=250,y=350)

reg_btn = Button(landing_frame, text="Register", font=("bold", 18), fg="white", bg="#2ecc72", relief=FLAT,padx=60,pady=20, command=register)
reg_btn.place(x=750,y=350)

quote = Label(landing_frame, text='Welcome To Reach',fg="black" , bg="orange")
quote.config(font=("Bold",50))
quote.place(x=350,y=200)





root.mainloop()