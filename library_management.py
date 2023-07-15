import mysql.connector
import datetime
import tkinter as tk
from tkinter import ttk
import time
 
def search_tk():
    '''Creates the framework for the searching'''
    def search():
        '''Does the searching in the database'''
        blank = tk.Label(master=frm,text='',font=('Arial',12))
        the_frame = tk.Frame(master=frm)
        blank.grid(row=4,column=0,columnspan=2,sticky='nsew')
        the_frame.grid(row=5,column=0,columnspan=2)
        blank['text'] = 'Result'
        listbox = tk.Listbox(master=the_frame,height=8,width=40)
        listbox.pack(side='left',fill='both')
        y = tk.Scrollbar(master=the_frame)
        y.pack(side='right',fill='both')
        listbox.config(yscrollcommand=y.set)
        y.config(command=listbox.yview)
        name = s_entry.get()
        genre = g_entry.get()
        author = a_entry.get()
        if genre=='All':
            q = 'select book_name from books where book_name like "%{}%" and author like"%{}%"'.format(name,author)
        else:
            q = 'select book_name from books where genre="{}" and book_name like "%{}%" and author like"%{}%"'.format(genre,name,author)
        try:
            curs = con.cursor(buffered=True)
            curs.execute(q)     #searches the database according to the user input
            x = curs.fetchall()
            for i in x:
                listbox.insert(tk.END,i[0])
        except:
            listbox['fg'] = 'tomato'
            listbox['justify'] = 'center'
            listbox.insert(tk.END,'Error')
    selectcolor(1)
    curs = con.cursor(buffered=True)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    curs.execute('select distinct genre from books')
    genres = [j for i in curs for j in i]
    genres.insert(0,'All')
    s_name = tk.Label(master=frm,text='Name: ')
    s_entry = tk.Entry(master=frm)
    a_name = tk.Label(master=frm,text='Author:')
    a_entry = tk.Entry(master=frm)
    g_name = tk.Label(master=frm,text='Genre:')
    g_entry = ttk.Combobox(master=frm,values=genres,state='readonly')
    s_button = tk.Button(master=frm,text='Search',bg='#3cb371',fg='#fff',command=search,width=40)
    s_name.grid(row=0,column=0)
    s_entry.grid(row=0,column=1,sticky='nsew')
    a_name.grid(row=1,column=0)
    a_entry.grid(row=1,column=1,sticky='nsew')
    g_name.grid(row=2,column=0)
    g_entry.grid(row=2,column=1,sticky='nsew')
    s_button.grid(row=3,column=0,columnspan=2,sticky='nsew')
    g_entry.current(0)
    s_entry.focus()

def donate_tk():
    '''Creates framework for entering details for donating'''
    def donate():
        '''Enters the book submited into the database'''
        b_name = b_name_entry.get()
        author = author_entry.get()
        genre = genre_entry.get()
        if b_name=='' or author=='' or genre=='':
            prog['text'] = 'Fill all'
            prog['fg'] = 'tomato'
            return
        curs = con.cursor(buffered=True)
        curs.execute("select book_id from books")
        x = curs.fetchall()
        if x:
            b_id = 'B' + str(int(x[-1][0][1:]) + 1)
            while len(b_id)<6:
                b_id = b_id[0] + '0' + b_id[1:]
        else:
            b_id = 'B00001'
        q = 'insert into books values ("{}","{}","{}","{}","Yes")'.format(b_id,b_name,author,genre)
        try:
            curs = con.cursor(buffered=True)
            curs.execute(q)         #enters the book details into the database
            con.commit()
            b_name_entry.delete(0,tk.END)
            author_entry.delete(0,tk.END)
            genre_entry.delete(0,tk.END)
            prog['text'] = 'Success'
            prog['fg'] = '#3cb371'
        except:
            prog['text'] = 'Error'
            prog['fg'] = 'tomato'
    selectcolor(4)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    b_name_lab = tk.Label(master=frm,text='Book: ')
    b_name_entry = tk.Entry(master=frm)
    author_lab = tk.Label(master=frm,text='Author: ')
    author_entry = tk.Entry(master=frm)
    genre_lab = tk.Label(master=frm,text='Genre: ')
    genre_entry = tk.Entry(master=frm)
    don_button = tk.Button(master=frm,text='Donate',width=40,bg='#3cb371',fg='#fff',command=donate)
    prog = tk.Label(master=frm,text='')
    b_name_lab.grid(row=0,column=0)
    b_name_entry.grid(row=0,column=1,sticky='nsew')
    author_lab.grid(row=1,column=0)
    author_entry.grid(row=1,column=1,sticky='nsew')
    genre_lab.grid(row=2,column=0)
    genre_entry.grid(row=2,column=1,sticky='nsew')
    don_button.grid(row=3,column=0,columnspan=2,sticky='nsew')
    prog.grid(row=4,column=0,columnspan=2,sticky='nsew')
    b_name_entry.focus()

def borrow_tk():
    '''Creates framework for entering details for issueing'''
    def check_available():
        '''Checks if the book is available'''
        def issue():
            '''Marks the book as issued by a reader'''
            try:
                curs = con.cursor(buffered=True)
                r_id = r_id_entry.get()
                curs.execute("select reader_id from user where reader_id='{}'".format(r_id))    #checks if the entered user id is in the database
                if curs.fetchall():
                    curs = con.cursor(buffered=True)
                    curs.execute("select d_date from issued where reader_id='{}' and returned='No'".format(r_id))   #checks if the user has any overdue books
                    x = curs.fetchall()
                    now = datetime.datetime.now().date()
                    c = 0
                    for i in x:
                        left = int(str(i[0] - now).split()[0])
                        if left<0:
                            c += 1
                    if c>0:
                        prog = tk.Label(master=frm,text='Return overdue book',fg='tomato')
                        prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
                        return
                else:
                    prog = tk.Label(master=frm,text='Not a user',fg='tomato')
                    prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
                    return
                curs.execute("select count(*) from issued where reader_id='{}' and returned='No'".format(r_id))     #gets the number of books, the user has at that moment
                if curs.fetchone()[0]>2:
                    prog = tk.Label(master=frm,text='Only 3 books',fg='tomato')
                    prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
                    return
                q2 = 'insert into issued values ("{}","{}","{}","{}","{}","No")'.format(b_id,b_name,r_id,b_date,d_date)     #enters the details of the user along with book into the database
                q3 = 'update books set availability="No" where book_name="{}"'.format(b_name)           #sets the availability of the book as taken so no other user can can issue it
                q4 = "update user set book_at_time=book_at_time+1 where reader_id='{}'".format(r_id)
                q5 = "update user set books=books+1 where reader_id='{}'".format(r_id)                  #updates the reader book count
                curs = con.cursor(buffered=True)
                curs.execute(q2)
                curs.execute(q3)
                curs.execute(q4)
                curs.execute(q5)
                con.commit()
                curs.execute("select d_date from issued where book_id='{}' and returned='No'".format(b_id))     #shows user the due date for the book
                x = curs.fetchone()
                r_id_entry.delete(0,tk.END)
                b_name_entry.delete(0,tk.END)
                prog = tk.Label(master=frm,text='Success\nBook: {}\nDue date: {}'.format(b_id,x[0]),fg='#3cb371')
                prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
            except:
                prog = tk.Label(master=frm,text='Error',fg='tomato')
                prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
        b_name = b_name_entry.get()
        q = 'select availability from books where book_name="{}"'.format(b_name)
        try:
            curs = con.cursor(buffered=True)
            curs.execute(q)
            x = curs.fetchall()
            if x[0][0]=='No':
                prog = tk.Label(master=frm,text='Book not available',fg='tomato')
                blank = tk.Label(master=frm,text='')
                q1 = 'select d_date from issued where book_name="{}"'.format(b_name_entry.get())
                try:
                    curs = con.cursor(buffered=True)
                    curs.execute(q1)        #to find when the book would be returned back
                    y = curs.fetchone()
                    line = "Should be available by {}".format(y[0])
                    line_lab = tk.Label(master=frm,text=line,fg='tomato')
                    line_lab.grid(row=4,column=0,columnspan=2,sticky='nsew')
                    blank.grid(row=5,column=0,rowspan=2,columnspan=2,sticky='nsew')
                except:
                    blank.grid(row=4,column=0,rowspan=3,columnspan=2,sticky='nsew')
                prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
            else:
                prog = tk.Label(master=frm,text='Book available',fg='#3cb371')
                r_id_lab = tk.Label(master=frm,text='Reader ID: ')
                r_id_entry = tk.Entry(master=frm)
                brrw_button = tk.Button(master=frm,text='Issue',bg='#3cb371',fg='#fff',command=issue,width=40)
                try:
                    curs = con.cursor(buffered=True)
                    q1 = 'select book_id from books where book_name="{}"'.format(b_name)
                    curs.execute(q1)
                    x = curs.fetchone()
                    b_id = x[0]
                    b_date = datetime.datetime.now().date()
                    d_date = b_date + datetime.timedelta(days=7)
                except:
                    prog = tk.Label(master=frm,text='Error',fg='tomato')
                    prog.grid(row=6,column=0,columnspan=2,sticky='nsew')
                r_id_lab.grid(row=4,column=0,sticky='nsew')
                r_id_entry.grid(row=4,column=1,sticky='nsew')
                prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
                brrw_button.grid(row=5,column=0,columnspan=2,sticky='nsew')
                r_id_entry.focus()
        except:
            prog = tk.Label(master=frm,text='Book not in Library',fg='tomato')
            blank = tk.Label(master=frm,text='')
            prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
            blank.grid(row=4,column=0,rowspan=3,columnspan=2,sticky='nsew')
    selectcolor(2)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    b_name_lab = tk.Label(master=frm,text='Book: ')
    b_name_entry = tk.Entry(master=frm)
    check_button = tk.Button(master=frm,text='Check Availability',width=40,bg='orange',command=check_available)
    b_name_lab.grid(row=0,column=0)
    b_name_entry.grid(row=0,column=1,sticky='nsew')
    check_button.grid(row=2,column=0,columnspan=2,sticky='nsew')
    b_name_entry.focus()

def retrn_tk():
    '''Creates a framework for entering details for returning a book'''
    def retrn():
        '''Marks the book as returned in the database'''
        curs = con.cursor(buffered=True)
        r_id = r_id_entry.get()
        b_id = b_id_entry.get()
        curs.execute("select book_id from books where book_id='{}'".format(b_id))
        if curs.fetchall():
            pass
        else:
            prog = tk.Label(master=frm,text='Non-valid book',fg='tomato')
            prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
            return
        curs = con.cursor(buffered=True)
        curs.execute("select reader_id from user where reader_id='{}'".format(r_id))
        if curs.fetchone():
            try:
                curs = con.cursor(buffered=True)
                curs.execute("select d_date from issued where reader_id='{}' and book_id='{}' and returned='No'".format(r_id,b_id))
                x = curs.fetchone()
                now = datetime.datetime.now().date()
                left = int(str(x[0] - now).split()[0])
                if left<0:
                    curs = con.cursor(buffered=True)
                    curs.execute("update user set overdue=overdue+1 where reader_id='{}'".format(r_id))
                    con.commit()
            except:
                prog = tk.Label(master=frm,text='Non-valid book',fg='tomato')
                prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
                return
        else:
            prog = tk.Label(master=frm,text='Non-valid user',fg='tomato')
            prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
            return
        try:
            q1 = "update issued set returned='Yes' where reader_id='{}' and book_id='{}'".format(r_id,b_id)
            q2 = "update books set availability='Yes' where book_id='{}'".format(b_id)
            q3 = "update user set book_at_time=book_at_time-1 where reader_id='{}'".format(r_id)
            curs = con.cursor(buffered=True)
            curs.execute(q1)
            curs.execute(q2)
            curs.execute(q3)
            con.commit()
            prog = tk.Label(master=frm,text='Success',fg='#3cb371')
            prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
            r_id_entry.delete(0,tk.END)
            b_id_entry.delete(0,tk.END)
        except:
            prog = tk.Label(master=frm,text='Error',fg='tomato')
            prog.grid(row=3,column=0,columnspan=2,sticky='nsew')
    selectcolor(3)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    r_id_lab = tk.Label(master=frm,text='Reader ID: ')
    r_id_entry = tk.Entry(master=frm)
    b_id_lab = tk.Label(master=frm,text='Book ID: ')
    b_id_entry = tk.Entry(master=frm)
    rtrn_button = tk.Button(master=frm,text='Return',bg='#3cb371',fg='#fff',width=40,command=retrn)
    r_id_lab.grid(row=0,column=0)
    r_id_entry.grid(row=0,column=1,sticky='nsew')
    b_id_lab.grid(row=1,column=0)
    b_id_entry.grid(row=1,column=1,sticky='nsew')
    rtrn_button.grid(row=2,column=0,columnspan=2,sticky='nsew')
    r_id_entry.focus()

def overdue_tk():
    '''Displays all the overdue books and their fine'''
    def overdue_details():
        '''Gives the details of books that are overdue, including the user who borrowed it'''
        details_box = tk.Tk()
        b_name = listbox.get('active')
        try:
            curs = con.cursor(buffered=True)
            curs.execute('select * from issued where book_name="{}" and returned="No"'.format(b_name))
            x = curs.fetchone()
            today = datetime.datetime.now().date()
            d_date = x[4]
            b_date = x[3]
            left = int(str(d_date - today).split()[0])
            fine = (((left*(-1))+7)//7)*15
            details_box.title(b_name)
            details_box.geometry("400x100")
            details_box.rowconfigure([0,1,2,3],weight=1)
            details_box.columnconfigure([0,1],weight=1)
            details_box.resizable(False,False)
            name_lab = tk.Label(master=details_box,text=b_name,font=('Arial',15))
            id_lab = tk.Label(master=details_box,text=x[0])
            id_nlab = tk.Label(master=details_box,text='Book ID: ')
            rid_lab = tk.Label(master=details_box,text=x[2])
            rid_nlab = tk.Label(master=details_box,text='Reader ID: ')
            f_nlab = tk.Label(master=details_box,text='Fine: ')
            f_lab = tk.Label(master=details_box,text="Rs. {}".format(fine))
            name_lab.grid(row=0,column=0,columnspan=2)
            id_nlab.grid(row=1,column=0)
            rid_nlab.grid(row=2,column=0)
            id_lab.grid(row=1,column=1)
            rid_lab.grid(row=2,column=1)
            f_nlab.grid(row=3,column=0)
            f_lab.grid(row=3,column=1)
        except:
            details_box.title('Error')
            error = tk.Label(master=details_box,text='Error',fg='tomato',justify='center')
            error.pack()
        details_box.mainloop()
    selectcolor(5)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    container = tk.Frame(master=frm)
    container.grid(row=0,column=0)
    details = tk.Button(master=frm,text='Get details',width=40,bg='#3cb371',fg='#fff',command=overdue_details)
    details.grid(row=1,column=0,sticky='nsew')
    listbox = tk.Listbox(master=container,width=40)
    listbox.pack(side='left',fill='both')
    y = tk.Scrollbar(master=container)
    y.pack(side='right',fill='both')
    listbox.config(yscrollcommand=y.set)
    y.config(command=listbox.yview)
    try:
        curs = con.cursor(buffered=True)
        curs.execute("select * from issued where returned='No'")
        x = curs.fetchall()
        if x:
            l = []
            for i in x:
                today = datetime.datetime.now().date()
                d_date = i[4]
                b_date = i[3]
                left = int(str(d_date - today).split()[0])
                if left<0:
                    fine = (((left*(-1))+7)//7)*15
                    listbox.insert(tk.END,i[1])
                    l += [i]
            if l:
                pass
            else:
                details['state'] = 'disabled'
        else:
            details['state'] = 'disabled'
    except:
        listbox['fg'] = 'tomato'
        listbox['justify'] = 'center'
        listbox.insert(tk.END,'Error')
        details['state'] = 'disabled'

def user_tk():
    '''Creates a framework which displays the members of the library'''
    def user_details():
        '''Displays the details of the selected member'''
        d_box = tk.Tk()
        r_id,r_name = listbox.get('active').split(': ')
        q = "select mobile,books,overdue,book_at_time from user where reader_id='{}'".format(r_id)
        try:
            d_box.title(r_name)
            d_box.geometry("400x250")
            d_box.rowconfigure([0,1,2,3,4,5,6,7],weight=1)
            d_box.columnconfigure([0,1],weight=1)
            d_box.resizable(False,False)
            container = tk.Frame(master=d_box)
            curs = con.cursor(buffered=True)
            curs.execute(q)
            x = curs.fetchone()
            curs = con.cursor(buffered=True)
            curs.execute("select book_id,book_name,d_date from issued where reader_id='{}' and returned='No'".format(r_id))
            records = curs.fetchall()
            h_id = tk.Label(master=container,text='Book ID',font=('Arial',13))
            h_name = tk.Label(master=container,text='Book Name',font=('Arial',13))
            h_date = tk.Label(master=container,text='Due Date',font=('Arial',13))
            h_id.grid(row=0,column=0,sticky='nsew')
            h_name.grid(row=0,column=1,sticky='nsew')
            h_date.grid(row=0,column=2,sticky='nsew')
            count = 1
            if records:
                for i in records:
                    b_id = tk.Label(master=container,text=i[0],bg='#fff',fg='#4f4f4f')
                    b_name = tk.Label(master=container,text=i[1],bg='#fff',fg='#4f4f4f')
                    d_date = tk.Label(master=container,text=i[2],bg='#fff',fg='#4f4f4f')
                    b_id.grid(row=count,column=0,sticky='nsew')
                    b_name.grid(row=count,column=1,sticky='nsew')
                    d_date.grid(row=count,column=2,sticky='nsew')
                    count += 1
            else:
                txt = tk.Label(master=container,text='None',bg='#fff',fg='#4f4f4f')
                txt.grid(row=1,column=0,columnspan=3,sticky='nsew')
                
            name_lab = tk.Label(master=d_box,text=r_name,font=('Arial',17))
            id_lab = tk.Label(master=d_box,text=r_id)
            id_nlab = tk.Label(master=d_box,text='Reader ID: ')
            m_lab = tk.Label(master=d_box,text=x[0])
            m_nlab = tk.Label(master=d_box,text='Mobile: ')
            b_nlab = tk.Label(master=d_box,text='Books taken: ')
            b_lab = tk.Label(master=d_box,text=x[1])
            o_nlab = tk.Label(master=d_box,text='Overdue books: ')
            o_lab = tk.Label(master=d_box,text=x[2])
            bat_nlab = tk.Label(master=d_box,text='Book at time: ')
            bat_lab = tk.Label(master=d_box,text=x[3])
            filler = tk.Label(master=d_box,text='╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳╳')
            name_lab.grid(row=0,column=0,columnspan=2)
            id_nlab.grid(row=1,column=0)
            m_nlab.grid(row=2,column=0)
            id_lab.grid(row=1,column=1)
            m_lab.grid(row=2,column=1)
            b_nlab.grid(row=3,column=0)
            b_lab.grid(row=3,column=1)
            o_nlab.grid(row=4,column=0)
            o_lab.grid(row=4,column=1)
            bat_nlab.grid(row=5,column=0)
            bat_lab.grid(row=5,column=1)
            filler.grid(row=6,column=0,columnspan=2)
            container.grid(row=7,column=0,columnspan=2)
        except:
            d_box.title('Error')
            error = tk.Label(master=d_box,text='Error',fg='tomato',justify='center')
            error.pack()
    def add_user_tk():
        '''Creates a window which allows a potential member to enter their details'''
        def add_user():
            '''Enters the new member into the database'''
            nonlocal listbox
            m = m_entry.get()
            r_name = r_name_entry.get()
            if m=='' or r_name=='':
                msg = tk.Label(master=create,text='DO NOT LEAVE EMPTY',fg='tomato')
                msg.grid(row=4,column=0,columnspan=2)
                return
            try:
                curs = con.cursor(buffered=True)
                curs.execute("select reader_id from user")
                x = curs.fetchall()
                if x:
                    last = x[-1][0]
                    r_num = int(last[1:]) + 1
                    r_id = 'R' + str(r_num)
                    while len(r_id)<6:
                        r_id = r_id[0] + '0' +r_id[1:]
                else:
                    r_id = 'R00001'
                q = "insert into user value ('{}','{}','{}',0,0,0)".format(r_id,r_name,m)
                curs = con.cursor(buffered=True)
                curs.execute(q)
                con.commit()
                msg = tk.Label(master=create,text='Success',fg='#3cb371')
                msg.grid(row=4,column=0,columnspan=2)
                listbox.insert(tk.END,r_id+': '+r_name)
                m_entry.delete(0,tk.END)
                r_name_entry.delete(0,tk.END)
            except:
                msg = tk.Label(master=create,text='ERROR',fg='tomato')
                msg.grid(row=4,column=0,columnspan=2)
        create = tk.Tk()
        create.title("New Reader")
        create.geometry('225x125')
        create.rowconfigure([0,1,2,3],weight=1)
        create.columnconfigure([0,1],weight=1)
        create.resizable(False,False)
        t = tk.Label(master=create,text='Details',font=('Arial',15))
        r_name_lab = tk.Label(master=create,text='Name: ')
        r_name_entry = tk.Entry(master=create)
        m_lab = tk.Label(master=create,text='Mobile no: ')
        m_entry = tk.Entry(master=create)
        j = tk.Button(master=create,text='Join',bg='#3cb371',fg='#fff',command=add_user)
        t.grid(row=0,column=0,columnspan=2)
        r_name_lab.grid(row=1,column=0)
        r_name_entry.grid(row=1,column=1)
        m_lab.grid(row=2,column=0)
        m_entry.grid(row=2,column=1)
        j.grid(row=3,column=0,columnspan=2,sticky='nsew')
        r_name_entry.focus()
        create.mainloop()
    def user_search():
        '''Searches the database for the given user'''
        det['state'] = 'normal'
        delete['state'] = 'normal'
        listbox['fg'] = '#000'
        listbox['justify'] = 'left'
        listbox.delete(0,tk.END)
        user = user_srch.get()
        q = "select reader_id,reader_name from user where reader_name like '%{}%'".format(user)
        try:
            curs = con.cursor(buffered=True)
            curs.execute(q)
            x = curs.fetchall()
            if x:
                for i in x:
                    listbox.insert(tk.END,i[0]+': '+i[1])
            else:
                det['state'] = 'disabled'
                delete['state'] = 'disabled'
        except:
            listbox['fg'] = 'tomato'
            listbox['justify'] = 'center'
            listbox.insert(tk.END,'Error')
            det['state'] = 'disabled'
            delete['state'] = 'disabled'
            print(e)
    def delete_user():
        r_id,r_name = listbox.get('active').split(': ')
        q = "delete from user where reader_id='{}'".format(r_id)
        try:
            curs = con.cursor(buffered=True)
            curs.execute(q)
            con.commit()
            listbox.delete('active')
        except:
            message = tk.Tk()
            message.title('Error')
            text = tk.Label(master=message,text='Unable to delete').pack()
            message.mainloop()
    selectcolor(6)
    global frm
    frm.destroy()
    frm = tk.Frame(master=root,padx=20,pady=10)
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    user_srch = tk.Entry(master=frm)
    sb = tk.Button(master=frm,text='Search',bg='#3cb371',fg='#fff',command=user_search)
    container = tk.Frame(master=frm)
    container.grid(row=1,column=0,columnspan=2)
    listbox = tk.Listbox(master=container,width=40)
    y = tk.Scrollbar(master=container)
    listbox.pack(side='left',fill='both')
    y.pack(side='right',fill='both')
    listbox.config(yscrollcommand=y.set)
    y.config(command=listbox.yview)
    det = tk.Button(master=frm,text='Get details',width=40,command=user_details,bg='#3cb371',fg='#fff')
    add = tk.Button(master=frm,text='New user',width=40,bg='#3cb371',fg='#fff',command=add_user_tk)
    delete = tk.Button(master=frm,text='Remove user',width=40,bg='tomato',fg='#fff',command=delete_user)
    user_srch.grid(row=0,column=0,sticky='nsew')
    sb.grid(row=0,column=1,sticky='nsew')
    det.grid(row=2,column=0,sticky='nsew',columnspan=2)
    add.grid(row=3,column=0,sticky='nsew',columnspan=2)
    delete.grid(row=4,column=0,sticky='nsew',columnspan=2)
    user_srch.focus()
    try:
        curs = con.cursor(buffered=True)
        curs.execute("select reader_id,reader_name from user")
        x = curs.fetchall()
        if x:
            for i in x:
                listbox.insert(tk.END,i[0]+': '+i[1])
        else:
            det['state'] = 'disabled'
            delete['state'] = 'disabled'
    except:
        listbox['fg'] = 'tomato'
        listbox['justify'] = 'center'
        listbox.insert(tk.END,'Error')
        det['state'] = 'disabled'
        delete['state'] = 'disabled'

def selectcolor(n):
    '''Changes the color of the menu item when clicked'''
    search_b['bg'] = '#dbdbdb'
    issue_b['bg'] = '#d4d4d4'
    return_b['bg'] = '#dbdbdb'
    donate_b['bg'] = '#d4d4d4'
    overdue_b['bg'] = '#dbdbdb'
    user_b['bg'] = '#d4d4d4'
    search_b['fg'] = '#3b3b3b'
    issue_b['fg'] = '#3b3b3b'
    return_b['fg'] = '#3b3b3b'
    donate_b['fg'] = '#3b3b3b'
    overdue_b['fg'] = '#3b3b3b'
    user_b['fg'] = '#3b3b3b'
    if n==1:
        search_b['bg'] = '#f0f0f0'
        search_b['fg'] = '#000'
    elif n==2:
        issue_b['bg'] = '#f0f0f0'
        issue_b['fg'] = '#000'
    elif n==3:
        return_b['bg'] = '#f0f0f0'
        return_b['fg'] = '#000'
    elif n==4:
        donate_b['bg'] = '#f0f0f0'
        donate_b['fg'] = '#000'
    elif n==5:
        overdue_b['bg'] = '#f0f0f0'
        overdue_b['fg'] = '#000'
    elif n==6:
        user_b['bg'] = '#f0f0f0'
        user_b['fg'] = '#000'

def exit_prgm():
    '''Exits the program after closing all connections'''
    curs.close()
    con.close()
    root.destroy()
        
def log():
    '''Creates a window for recieving the username and password of mysql database'''
    def check_usernpass(event=None):
        '''Checks whether the username and password are correct'''
        global usr
        global psswrd
        usr = l_e.get()
        psswrd = p_e.get()
        try:
            con = mysql.connector.connect(host='localhost',user=usr,passwd=psswrd)
            con.close()
            login.destroy()
        except:
            l_e.delete(0,tk.END)
            p_e.delete(0,tk.END)
    login = tk.Tk()
    login.title('Database Login')
    login.geometry("200x75")
    login.rowconfigure([0,1,2],weight=1)
    login.columnconfigure([0,1],weight=1)
    login.resizable(False,False)
    l = tk.Label(master=login,text='User: ')
    l_e = tk.Entry(master=login)
    p = tk.Label(master=login,text='Password: ')
    p_e = tk.Entry(master=login,show='*')
    sub = tk.Button(master=login,text='Submit',fg='#fff',bg='#3cb371',command=check_usernpass)
    l.grid(row=0,column=0)
    l_e.grid(row=0,column=1)
    p.grid(row=1,column=0)
    p_e.grid(row=1,column=1)
    sub.grid(row=2,column=0,columnspan=2,sticky='nsew')
    l_e.focus()
    login.bind('<Return>',check_usernpass)
    login.mainloop()

def check_db():
    '''Creates database and tables needed for connectivity program if it doesnt exist'''
    try:
        con = mysql.connector.connect(host='localhost',user=usr,passwd=psswrd)
        curs = con.cursor()
        curs.execute("create database if not exists library")
        curs.execute("use library")
        curs.execute("create table if not exists books (book_id varchar(6),book_name varchar(50),author varchar(25),genre varchar(20),availability varchar(3))")
        curs.execute("create table if not exists issued (book_id varchar(6),book_name varchar(50),reader_id varchar(6),b_date date,d_date date,returned varchar(3))")
        curs.execute("create table if not exists user (reader_id varchar(6),reader_name varchar(25),mobile varchar(15),books int,overdue int,book_at_time int)")
        con.commit()
        curs.close()
        con.close()
    except:
        box = tk.Tk()
        txt = tk.Label(master=box, text='Unable to create\ndatabase/table',fg='tomato')
        txt.pack()
        box.mainloop()

def check_con():
    '''Establishes connection with the the database'''
    try:
        global con
        global curs
        con = mysql.connector.connect(host='localhost',user=usr,passwd=psswrd,database='Library')
        curs = con.cursor()
    except:
        box = tk.Tk()
        txt = tk.Label(master=box, text='Unable to establish connection',fg='tomato')
        txt.pack()
        time.sleep(2)
        exit()
        box.mainloop()

def main():
    '''Creates the main window where user interacts with the database'''
    global root
    global title
    global search_b
    global issue_b
    global return_b
    global donate_b
    global overdue_b
    global user_b
    global exit_b
    global frm
    global ptext
    root = tk.Tk()
    root.title('Library Management')
    root.geometry('500x375')
    root.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
    root.columnconfigure([0,1], weight=1)
    root.rowconfigure([0], weight=1,minsize=50)
    root.resizable(False,False)
    title = tk.Label(master=root,text='Library Manager',font=('Georgia',20),bg='#fff',height=2)
    search_b = tk.Button(master=root,text='Search',border=0,font=('Arial',10),fg='#3b3b3b',command=search_tk,bg='#dbdbdb',width=20)
    issue_b = tk.Button(master=root,text='Issue',border=0,font=('Arial',10),fg='#3b3b3b',bg='#d4d4d4',command=borrow_tk)
    return_b = tk.Button(master=root,text='Return',border=0,font=('Arial',10),fg='#3b3b3b',bg='#dbdbdb',command=retrn_tk)
    donate_b = tk.Button(master=root,text='Donate',border=0,font=('Arial',10),fg='#3b3b3b',bg='#d4d4d4',command=donate_tk)
    overdue_b = tk.Button(master=root,text='Overdue',border=0,font=('Arial',10),fg='#3b3b3b',bg='#dbdbdb',command=overdue_tk)
    user_b = tk.Button(master=root,text='Users',border=0,font=('Arial',10),fg='#3b3b3b',bg='#d4d4d4',command=user_tk)
    exit_b = tk.Button(master=root,text='Exit',border=0,font=('Arial',10),bg='tomato',activebackground='red',fg='#fff',command=exit_prgm)
    frm = tk.Frame(master=root,width=300,padx=20,pady=30,bg='#f0f0f0')
    ptext = tk.Label(master=frm,width=40,text='Welcome to the Library Manager.\n If you are a new library,\n add a few books in the \'Donate\' section.\nIf you are a new user, go to the \'Users\' section.\nFeel free to look around.')
    title.grid(row=0,column=0,columnspan=2,sticky='nsew')
    search_b.grid(row=1,column=0,sticky='nsew')
    issue_b.grid(row=2,column=0,sticky='nsew')
    return_b.grid(row=3,column=0,sticky='nsew')
    donate_b.grid(row=4,column=0,sticky='nsew')
    overdue_b.grid(row=5,column=0,sticky='nsew')
    user_b.grid(row=6,column=0,sticky='nsew')
    exit_b.grid(row=7,column=0,sticky='nsew')
    frm.grid(row=1,column=1,rowspan=7,sticky='nsew')
    ptext.grid(row=0,column=0,sticky='nsew')
    root.mainloop()

def start():
    '''Calls the required functions which are used to initialize the program'''
    log()
    check_db()
    check_con()
    main()

start()
