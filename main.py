import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        tool_bar = tk.Frame(bg='#d7d8e0', bd='2')
        tool_bar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.update_img = tk.PhotoImage(file='./img/update.png')
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        self.search_img = tk.PhotoImage(file='./img/search.png')

        btn_add_dialog = tk.Button(tool_bar, bg='#d7d8e0', bd='0', image=self.add_img, command=self.open_dialog)
        btn_add_dialog.pack(side=tk.LEFT)
        btn_update_dialog = tk.Button(tool_bar,bg='#d7d8e0', bd='0', image=self.update_img, command=self.open_update_dialog)
        btn_update_dialog.pack(side=tk.LEFT)
        btn_delete_dialog = tk.Button(tool_bar, bg='#d7d8e0', bd='0', image=self.delete_img, command=self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT)
        btn_search_dialog = tk.Button(tool_bar, bg='#d7d8e0', bd='0', image=self.search_img, command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Tel', 'Email', 'Salary'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Name', width=300, anchor=tk.CENTER)
        self.tree.column('Tel', width=150, anchor=tk.CENTER)
        self.tree.column('Email', width=150, anchor=tk.CENTER)
        self.tree.column('Salary', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='ФИО')
        self.tree.heading('Tel', text='Телефон')
        self.tree.heading('Email', text='Почта')
        self.tree.heading('Salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)

    def open_dialog(self):
        Child()

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def view_records(self):
        self.db.cur.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    def open_update_dialog(self):
        Update()

    def update_records(self, name, tel, email, salary):
        self.db.cur.execute('''
        UPDATE db SET name=?, tel=?, email=?, salary=? WHERE id=?''', (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.view_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('''
            DELETE FROM db WHERE id=?''', self.tree.set(selection_item, '#1'))
            db.con.commit()
            self.view_records()

    def open_search_dialog(self):
        Search()

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()] # #


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x250')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50 , y=50)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50, y=80)
        label_email = tk.Label(self, text='Почта')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_tel = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_salary = tk.Entry(self)
        self.entry_name.place(x=120, y=50)
        self.entry_tel.place(x=120, y=80)
        self.entry_email.place(x=120, y=110)
        self.entry_salary.place(x=120, y=140)

        cancel_bnt = tk.Button(self, text='Закрыть', command=self.destroy)
        cancel_bnt.place(x=300, y=200)
        add_btn = tk.Button(self, text='Добавить')
        add_btn.place(x=220, y=200)
        add_btn.bind('<Button-1>', lambda event: self.view.records(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()
        ))


class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.init_edit()

    def init_edit(self):
        self.title('Редактирование')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=200)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy, add='+')


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.db = db
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x200')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Имя')
        label_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=130, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=325, y=150)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=250, y=150)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(
            self.entry_search.get()
        ))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DataBase:
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('DataBase.db')
        self.cur = self.con.cursor()
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS db(
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        salary TEXT)''')
        self.con.commit()

    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''
        INSERT INTO db(name, tel, email, salary) VALUES (?,?,?,?)''', (name, tel, email, salary))
        self.con.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DataBase()
    app = Main(root)
    app.pack()
    root.title('Empl_list')
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()