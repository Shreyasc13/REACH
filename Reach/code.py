from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import sqlite3
from PIL import Image, ImageTk
import mysql.connector


mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="!Ka19p9220",
    auth_plugin='mysql_native_password',
    database='reach',
)
cur=mydb.cursor()


root = Tk()
root.state('zoomed') 
root['bg'] = 'white'
bg1=PhotoImage(file='food5.png')
submit_path = Image.open('icons\submit.png')
submit = ImageTk.PhotoImage(submit_path)
# submit = PhotoImage(file='submit.png')

# bg_img=Image.open('bg1.png')
# text = Label(root, text='Welcome to Reach',background="#0A79DF",fg="white",width=50,padx=10,pady=10)
# text.config(font=("Bold",30))
# text.grid(row=3,column=0,columnspan=8,padx=5,pady=5)

# *****************Add info**************************

def food_db(food_type,food_name, quantity, address,pin_code):
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="!Ka19p9220",
    auth_plugin='mysql_native_password',
    database='reach',
    )
    cur=mydb.cursor()    

    cur.execute("INSERT INTO food_order(f_type,f_nam,quantity, f_location,pin_code) VALUES (%s,%s,%s,%s)",(food_type,food_name, quantity, address,pin_code))

    cur.commit()
    cur.close()


#registration and login database
def register_db(selection,fname,lname,phone,password,org_name,org_location):
    print(selection,fname,lname,phone,password)
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="!Ka19p9220",
    auth_plugin='mysql_native_password',
    database='reach',
    )
    cur=mydb.cursor()
    if selection=="D":
        cur.execute("INSERT INTO donor (f_name,l_name,phone_no,password) VALUES (%s,%s,%s,%s)",(fname,lname,phone,password))
        
       
    elif selection=="V":
        cur.execute("INSERT INTO volunteer (f_name,l_name,phone_no,password,org_name,org_location) VALUES (%s,%s,%s,%s,%s,%s)",(fname,lname,phone,password,org_name,org_location))
    mydb.commit()
# donor = cur.execute("""SELECT * FROM donor WHERE PHONE= %s AND PASSWORD= %s""", ()) 
#donor food donation database
def donor(selected):
    donor_win=Toplevel(root)


    # reg_btn['state'] = 'disabled'
    # login_btn['state'] = 'normal'
    # # return_btn['state'] = 'normal'

    # text.grid_forget()
    # login_frame.grid_forget()
    # # return_frame.grid_forget()

    global donor_frame

    donor_frame = Frame(donor_win, bg='blue', borderwidth=5, padx=20, pady=20)
    # donor_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=40, sticky=N)
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
    
    

    donor_submit = Button(donor_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda: food_db(food_type_combo.get(), food_name_entry.get(), quantity_entry.get(), city_entry.get("1.0",END), pin_code_entry.get()))
    donor_submit.config(font=("Helvetica", 15))
    donor_submit.grid(row=7, column=0, columnspan=3, padx=20, pady=20)

def register():
    register_win=Toplevel(root)
   
    global register_frame,org_name_label,org_location_label
    register_frame = Frame(register_win, bg='blue', borderwidth=5, padx=20, pady=20)
    register_frame.grid(row=3, column=0, columnspan=4, padx=20, pady=40, sticky=N)

   


    def add_org():
        org_name_label['state']='normal'
        org_name_entry['state']='normal'
        org_location_label['state']='normal'
        org_location_entry['state']='normal'


    def rem_org():
        # org_name_entry['bg']='black'
        # org_location_entry['bg']='black'

        org_name_label['state']='disabled'
        org_name_entry['state']='disabled'
        org_location_label['state']='disabled'
        org_location_entry['state']='disabled'

    

    selection=StringVar()

    #selection widget
    Radiobutton(register_frame, text="Donate",variable=selection, value="D", font=("Bold",12),command=rem_org).grid(row=0,column=0)

    Radiobutton(register_frame, text="Volunteer",variable=selection, value="V", font=("Bold",12),command=add_org).grid(row=0,column=1)

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
    org_location_label = Label(register_frame,text="Organization location", padx=5, pady=5, width=15, anchor=W)
    org_location_label.config(font=("Bold",15))
    org_location_label.grid(row=7,column=0, padx=15, pady=15, sticky=W)

    org_location_entry = Entry(register_frame,borderwidth=3,width=15)
    org_location_entry.config(font=8)
    org_location_entry.grid(row=7,column=1, padx=15,sticky=E)

    

    button_submit = Button(register_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:register_db(selection.get(),first_name_entry.get(),last_name_entry.get(),phone_entry.get(),reg_password_entry.get(),org_location_entry.get(),org_location_entry.get()))
    button_submit.config(font=("Helvetica", 15))
    button_submit.grid(row=8, column=0, columnspan=3, padx=20, pady=20)

# login frame
def login():
    login_win=Toplevel(root)
    # reg_btn['state'] = 'normal'
    # login_btn['state'] = 'disable'

    # text.grid_forget()
    # add_customer_frame.grid_forget()
    mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="!Ka19p9220",
    auth_plugin='mysql_native_password',
    database='reach',
    )
    
    cur=mydb.cursor()

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
        cur.execute("SELECT * FROM donor WHERE phone_no=%s AND password=%s",(ph,psw))
        a=cur.fetchall()

        if c=='D':
            if len(a):
                donor(c)
            else:
                messagebox.showerror('error','failed')
        else:
            print("volunteer")
       

    button_submit = Button(login_frame,text="Submit",padx=32,pady=9,fg="white",background="#0ABDE3",borderwidth=2,relief=RAISED, command=lambda:check(selection.get()))
    button_submit.config(font=("Helvetica", 15))
    button_submit.grid(row=7, column=0, columnspan=3, padx=20, pady=20)


head_label = Label(root, text="Reach ",background="#0A79DF",fg="white",width=65,padx=14,pady=10,anchor=W)
head_label.config(font=("Bold",30))


head_label.grid(row=0,column=0,columnspan=5,padx=5,pady=5,sticky=W)

# def clock():
#     hour = time.strftime("%I")
#     min = time.strftime("%M")
#     sec = time.strftime("%S")
#     am_pm = time.strftime("%p")

#     dayNum = time.strftime("%d")
#     month = time.strftime("%b")
#     year = time.strftime("%Y")
#     day = time.strftime("%A")

#     date_label.config(text= dayNum +' '+ month +' '+ year +'   '+ day)

#     time_label.config(text= hour +':'+ min +':'+ sec +' '+ am_pm)
#     time_label.after(1000, clock)

# #time frame
# topframe = Frame(root, bg="#00b894", padx=90)
# topframe.grid(row=1, column=0, columnspan=8, padx=0)

# date_label = Label(topframe, text='', font=("bold", 18), fg="#6D214F", bg="#00b894", pady=5, relief=FLAT)
# date_label.pack(side="left", padx=(0,200), anchor=W)

# # title = Label(topframe, text='RENT-IT', font=("helvetica", 18), fg="white", bg="#00b894", pady=5, relief=FLAT)
# # title.pack(side="left", padx=200, anchor=W)

# time_label = Label(topframe, text='', font=("bold", 18), fg="#6D214F", bg="#00b894", pady=5, relief=FLAT)
# time_label.pack(side="left", padx=(200,0), anchor=E)

# clock()

# topframe = Frame(root, bg="#2ecc72")
# topframe.grid(row=2, column=0, columnspan=8, pady=5,sticky=N)




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


# donate_btn = Button(landing_frame, text="Donate", font=("bold", 18), fg="white", bg="#2ecc72", relief=FLAT,padx=30,pady=30, command=donate)
# donate_btn.place(x=300,y=450)

# volunteer_btn = Button(landing_frame, text="Volunteer", font=("bold", 18), fg="white", bg="#2ecc72", relief=FLAT,padx=60,pady=60)
# volunteer_btn.place(x=700,y=450)



root.mainloop()