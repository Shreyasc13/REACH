from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import sqlite3
from PIL import Image, ImageTk

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
def register_db(selection,fname,lname,phone,password,org_name,location):

    con=sqlite3.connect('reach2.db')
    cur=con.cursor()
    
    print(selection,fname,lname,phone,password)
    if selection=="D":
        cur.execute("INSERT INTO donor (f_name,l_name,phone_no,password) VALUES (?,?,?,?)",(fname,lname,phone,password))
        
       
    elif selection=="V":
        cur.execute("INSERT INTO volunteer (f_name,l_name,phone_no,password,org_name,org_location) VALUES (?,?,?,?,?,?)",(fname,lname,phone,password,org_name,location))

    elif selection=="DL":
        cur.execute("INSERT INTO delivery_info(del_name,del_phone,del_password,del_location) VALUES(?,?,?,?)",(fname,phone,password,location))

    con.commit()
    con.close()

def food_db(d_id,food_type,foodname,quantity,address,pin):


    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()
        address=address.rstrip("\n")

        values=(d_id,food_type,foodname,quantity,address,pin)
        print(values)
        cur.execute("INSERT INTO food_order(d_id,f_type,f_name,quantity,f_location,pin_code) VALUES (?,?,?,?,?,?)",(d_id,food_type,foodname,quantity,address,pin))

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

            


def volunteer(v_id):
    with sqlite3.connect('reach2.db') as con:
        cur=con.cursor()

        volunteer_win=Toplevel(root)
        volunteer_frame=Frame(volunteer_win,bg='light blue',borderwidth=5,padx=20,pady=20)

        volunteer_frame.pack()

        cur.execute("SELECT * FROM food_order")
        fd=cur.fetchall()
        print(fd)

        cur.execute("SELECT * from delivery_info")
        di=cur.fetchall()
        print(di)

        volunteer_id=v_id

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

        headers=['Food Id','Food Type','Food Name','Quantity','f_location','Pin Code']
        
        for j in range(6):
            e = Entry(volunteer_frame, width=20, borderwidth=2, bg="#7f8c8d", fg='white', highlightthickness=2)
            e.config(highlightbackground = "#900C3F", highlightcolor= "#900C3F", relief=FLAT)
            e.grid(row=0, column=j+2, padx=10, pady=2)
            e.insert(END, headers[j])


        for i in range(len(fd)):
            for j in range(0,6):

                e = Entry(volunteer_frame, width=20, borderwidth=2, highlightthickness=2)
                e.config(highlightbackground = "red", highlightcolor= "red", relief=FLAT)
                e.grid(row=i+1, column=j+2, padx=10, pady=2)
                e.insert(END, fd[i][j])

           

        del_headers=['Delivery ID','Name','Phone','Location']

        m=len(fd)+2

        for j in range(4):
            e = Entry(volunteer_frame, width=20, borderwidth=2, bg="#7f8c8d", fg='white', highlightthickness=2)
            e.config(highlightbackground = "#900C3F", highlightcolor= "#900C3F", relief=FLAT)
            e.grid(row=m, column=j+2, padx=10, pady=2)
            e.insert(END, del_headers[j])


        for i in range(len(di)):
            for j in range(0,4):


                e = Entry(volunteer_frame, width=20, borderwidth=2, highlightthickness=2)
                e.config(highlightbackground = "red", highlightcolor= "red", relief=FLAT)
                e.grid(row=i+m+1, column=j+2, padx=10, pady=2)
                if j==3:
                    j+=1
                e.insert(END, di[i][j])

                button_submit = Button(volunteer_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:transaction_db(volunteer_id,food_id_entry.get(),delivery_id_entry.get()))
                button_submit.config(font=("Helvetica", 15))
                button_submit.grid(row=8, column=0, columnspan=3, padx=20, pady=20)

def donor(d_id):
    donor_win=Toplevel(root)
    print(d_id)

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
    register_win=Toplevel(root)
   
    global register_frame,org_name_label,location_label
    register_frame = Frame(register_win, bg='blue', borderwidth=5, padx=20, pady=20)
    register_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=40, sticky=N)

   


    def add_org():
        org_name_label['state']='normal'
        org_name_entry['state']='normal'
        location_label['state']='normal'
        location_entry['state']='normal'
        last_name_label['state']='normal'
        last_name_entry['state']='normal'


    def rem_org():
        # org_name_entry['bg']='black'
        # org_location_entry['bg']='black'

        org_name_label['state']='disabled'
        org_name_entry['state']='disabled'
        location_label['state']='disabled'
        location_entry['state']='disabled'
        last_name_label['state']='normal'
        last_name_entry['state']='normal'

    def rem_del():
        last_name_label['state']='disabled'
        last_name_entry['state']='disabled'
        org_name_label['state']='disabled'
        org_name_entry['state']='disabled'

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

    reg_password_entry = Entry(register_frame,borderwidth=3,width=15)
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

    

    button_submit = Button(register_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:register_db(selection.get(),first_name_entry.get(),last_name_entry.get(),phone_entry.get(),reg_password_entry.get(),org_name_entry.get(),location_entry.get()))
    button_submit.config(font=("Helvetica", 15))
    button_submit.grid(row=8, column=0, columnspan=3, padx=20, pady=20)

# login frame
def login():
    login_win=Toplevel(root)
    con=sqlite3.connect('reach2.db')
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

    log_password_entry = Entry(login_frame,borderwidth=3,width=15)
    log_password_entry.config(font=8)
    log_password_entry.grid(row=1,column=1, padx=15,sticky=E)

    def check(c):
        
     
        # print(a)
        ph=reg_phone_entry.get()
        psw=log_password_entry.get()
        

        if c=='D':
            cur.execute("SELECT * FROM donor WHERE phone_no=? AND password=?",(ph,psw))
            a=cur.fetchall()
            print(a)
            if len(a):
                d_id=cur.execute("SELECT d_id FROM donor WHERE phone_no=? AND password=?",(ph,psw)).fetchone()
                print(d_id[0])
                donor(d_id[0])
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