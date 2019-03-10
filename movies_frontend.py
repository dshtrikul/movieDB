from tkinter import *
import movies_backend as backend

def search_comm():
    global currentview
    currentview = []
    def check_len(item):
        if len(item) == 0 :
            return None
        else: return item

    list1.delete(0,END)
    arguments = map(check_len,[title_text.get(),genre_text.get(),director_text.get(),country_text.get(),year_text.get()])
    title,genre,director,country,year = tuple(arguments)
    for row in backend.search(title,genre,director,country,year):
        a,b,c,d,e,f = row
        list1.insert(END,"{} | {} | {}".format(c,b,f))
    currentview = list1.get(0,END)

def show_all_comm():
    global currentview
    list1.delete(0,END)
    for row in backend.view_all():
        a,b,c,d,e,f = row
        list1.insert(END,"{} | {} | {}".format(c,b,f))
    currentview = list1.get(0,END)

def get_selected_row(event):

    global selected_tuple
    global index
    index=list1.curselection()[0]
    selected_tuple = list1.get(index)
    get_title = selected_tuple.split(" | ")[1]
    selected_tuple = backend.search(title=get_title)[0]
    # print(selected_tuple)
    e1.delete(0,END)
    e1.insert(0,selected_tuple[1]) # title
    e2.delete(0,END)
    e2.insert(0,selected_tuple[2]) # year
    e3.delete(0,END)
    e3.insert(0,selected_tuple[5]) #director
    e4.delete(0,END)
    e4.insert(0,selected_tuple[4]) # country
    e5.delete(0,END)
    e5.insert(0,selected_tuple[3]) # genre

def add_item_comm():
    backend.insert_row(title_text.get(),genre_text.get(),director_text.get(),country_text.get(),year_text.get())
    ## ADDS all the items found || need to redesign seach to AND clauses
    a,b,c,d,e,f = backend.search(title_text.get(),genre_text.get(),director_text.get(),country_text.get(),year_text.get())[0]
    list1.insert(0,"{} | {} | {}".format(c,b,f))

def delete_item_comm():
    backend.delete_row(selected_tuple[0])
    list1.delete(index)
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)

def update_item_comm():
    global selected_tuple
    backend.update_row(selected_tuple[0],title_text.get(),genre_text.get(),director_text.get(),country_text.get(),year_text.get())
    list1.delete(0,END)
    for item in currentview:
        if item.split(" | ")[1] == selected_tuple[1]:  # title from listbox == title from entry box
            list1.insert(END,"{} | {} | {}".format(year_text.get(),title_text.get(),genre_text.get()))
        else:
            list1.insert(END,item)

def clear_all_comm():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e1.delete(0,END)
    list1.delete(0,END)

v = ('Verdana', 10)
window=Tk()
#*****************************************************************************
l1=Label(window,text='Title')
l1.grid(row=0,column=0, sticky=E)

title_text=StringVar()
e1=Entry(window, textvariable=title_text, font=v)
e1.grid(row=0,column=1,columnspan=4, sticky=W+E)
#*****************************************************************************
l3=Label(window,text='Genre')
l3.grid(row=1,column=0, sticky=E)

genre_text=StringVar()
e3=Entry(window, textvariable=genre_text, font=v)
e3.grid(row=1,column=1,columnspan=4, sticky=W+E)
#*****************************************************************************
l5=Label(window,text='Director')
l5.grid(row=2,column=0, sticky=E)

director_text=StringVar()
e5=Entry(window,textvariable=director_text, font=v)
e5.grid(row=2,column=1,columnspan=4, sticky=W+E)
#*****************************************************************************
l4=Label(window,text='Country')
l4.grid(row=3,column=0, sticky=W+E)

country_text=StringVar()
e4=Entry(window, textvariable=country_text, font=v)
e4.grid(row=3,column=1,columnspan=4, sticky=W+E)
#*****************************************************************************
l2=Label(window,text='Year')
l2.grid(row=4,column=0, sticky=E)

year_text=StringVar()
e2=Entry(window,width = 5,textvariable=year_text, font=v)
e2.grid(row=4,column=1, sticky=W)
#*****************************************************************************
#*****************************************************************************
#*****************************************************************************
b1 = Button(window,text='Search', width=20, command=search_comm)
b1.grid(row=0, column =5, padx=5)
#*****************************************************************************
b2 = Button(window,text='Add Item', width=20, command=add_item_comm)
b2.grid(row=1, column =5, padx=5)
#*****************************************************************************
b3 = Button(window,text='Delete Item', width=20, command=delete_item_comm)
b3.grid(row=2, column=5, padx=5)
#*****************************************************************************
b4 = Button(window,text='Update Item', width=20, command=update_item_comm)
b4.grid(row=3, column=5, padx=5)
#*****************************************************************************
b5 = Button(window,text='Show All', width=20, command=show_all_comm)
b5.grid(row=4, column=5, padx=5)
#*****************************************************************************
b5 = Button(window,text='Clear All', width=20, command=clear_all_comm)
b5.grid(row=4, column=4)
#*****************************************************************************
#*****************************************************************************
list1 = Listbox(window, width = 150, height=30,)
list1.grid(row=5, column=0, columnspan=6, sticky=W+E+N+S, padx=5)

list1.bind('<<ListboxSelect>>', get_selected_row)
#*****************************************************************************
sb1=Scrollbar(window)
sb1.grid(row=5, column=6,sticky=W)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)
#*****************************************************************************
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=0)
window.columnconfigure(3, weight=0)
window.columnconfigure(4, weight=0)
window.columnconfigure(5, weight=0)
window.columnconfigure(6, weight=0)
window.rowconfigure(5, weight=1)

window.mainloop()
