import tkinter
import sqlite3
from tkinter import messagebox
from time import ctime


class task_class:
    def __init__(self, root, name):
        self.root = root
        self.name = name
    def task_do_one(self, name, obj, downe):
        database = sqlite3.connect("database.db")
        data = self.database.cursor().execute(f"""
            SELECT * FROM data WHERE name LIKE '{name}'
        """).fetchall()
        data = data[0]
        date = data[-1]
        date += "\t" + ctime()
        done = data[2]
        if not done:
            done = 0
        done += 1
        database.cursor().execute(f"""
            UPDATE data
            SET 
                date='{date}',
                done={done}
            WHERE 
                name 
                LIKE 
                '{name}'
        """)
        database.commit()
        self.fetch_button_data(name, obj, downe)


    def task_undo_one(self, name, obj, downe):
        database = sqlite3.connect("database.db")
        data = self.database.cursor().execute(f"""
                SELECT * FROM data WHERE name LIKE '{name}'
            """).fetchall()
        data = data[0]
        done = data[2]
        if not done:
            done = 0
        done -= 1
        database.cursor().execute(f"""
                UPDATE data
                SET 
                    done={done}
                WHERE 
                    name 
                    LIKE 
                    '{name}'
            """)
        database.commit()
        self.fetch_button_data(name, obj, downe)


    def task_delete(self, name, obj):
        database = sqlite3.connect("database.db")
        ask = messagebox.askyesno("ASK", f"Are you sure you want to delete \nTask Name : {name}")
        print(ask)
        if ask:
            database.cursor().execute(f"""
                DELETE FROM data WHERE
                    name 
                    LIKE 
                    '{name}'
                    ;
            """)
            database.commit()
            self.root.update()
            obj.destroy()


    def fetch_button_data(self, name, obj, done):
        data = self.database.cursor().execute(f"SELECT * FROM data WHERE name like '{name}'").fetchall()
        data = data[0]
        print(data)
        # if len(data[-1]) != len(date):
        #     button_y += 20
        # date.config(text=data[-1])
        done.config(text=f"{data[2]}/{data[1]}")

        obj.update()


    def task_menu_gui(self, name):
        max_width = 450
        max_heigth = 300
        button_y = 200
        t_name = tkinter.Tk()
        t_name.title(name)
        t_name.config(bg="black", height=max_heigth, width=max_width)
        self.database = sqlite3.connect("database.db")
        data = self.database.cursor().execute(f"SELECT * FROM data WHERE name like '{name}'").fetchall()
        data = data[0]
        t_name_la = tkinter.Label(t_name, text="Task Name : ", font=50, bg="black", fg="white")
        t_name_la.place(x=20, y=50)
        t_name_la2 = tkinter.Label(t_name, text=f"{name}", font=50, bg="black", fg="white")
        t_name_la2.place(x=120, y=50)
        t_task_la = tkinter.Label(t_name, text="Task : ", font=50, bg="black", fg="white")
        t_task_la.place(x=20, y=100)
        t_task_la2 = tkinter.Label(t_name, text=f"{data[2]}/{data[1]}", font=50, bg="black", fg="white")
        t_task_la2.place(x=120, y=100)
        # t_date_la = tkinter.Label(t_name, text="Dates : ", font=50, bg="black", fg="white")
        # t_date_la.place(x=20, y=150)
        # t_date_la2 = tkinter.Label(t_name, text=f"{data[3]}", bg="black", fg="white")
        # t_date_la2.place(x=120, y=150)
        t_name_do_button = tkinter.Button(t_name, text="Add One ", bg="green", fg="white", height=1, width=7,
                                          command=lambda: self.task_do_one(name, t_name, t_task_la2))
        t_name_do_button.place(x=10, y=200)
        t_name_undo_button = tkinter.Button(t_name, text="Decrease One ", bg="yellow", fg="black", height=1, width=9,
                                            command=lambda: self.task_undo_one(name, t_name, t_task_la2))
        t_name_undo_button.place(x=110, y=200)
        t_name_delete_button = tkinter.Button(t_name, text="Delete", bg="magenta", fg="black", height=1, width=7,
                                              command=lambda: self.task_delete(name, t_name))
        t_name_delete_button.place(x=220, y=200)
        t_name_exit_button = tkinter.Button(t_name, text="Exit", bg="red", fg="white", height=1, width=9,
                                            command=t_name.destroy)
        t_name_exit_button.place(x=310, y=200)
        t_name.after(10, lambda: self.fetch_button_data(name, t_name, t_task_la2))
        t_name.mainloop()
    def run(self):
        self.task_menu_gui(self.name)

class MainClass:
    def __init__(self):
        self.data_base = sqlite3.connect("database.db")
        self.data_base.cursor().execute("""
        CREATE TABLE IF NOT EXISTS 'data' (
                "name" TEXT UNIQUE,
                "to_do" INT,
                "done" INT,
                "date" TEXT,
	            PRIMARY KEY("name")
            );
        """)
        self.data_base.commit()
        self.root = tkinter.Tk()
        self.max_heigth = 450
        self.max_width = 400
        self.data = []
        self.database_manager()
    def creat_task(self):
        self.data_base = sqlite3.connect("database.db")
        # self.data_base.cursor().execute("")
        name = self.task_name_en.get()
        to_do = self.task_parts_en.get()
        if not name :
            messagebox.showerror('name error', 'fill the name section !')
            return
        # ?try:
        self.data_base.cursor().execute(f"""
            INSERT INTO data (
                name,
                to_do,
                date
            ) VALUES (
                "{name}",
                "{to_do}",
                "Created : {ctime()}\nDo: "
            );
        """)
        self.data_base.commit()
        messagebox.showinfo("Successful", f"your task created successfully as : {name}")
        # except:
        #     messagebox.showerror('insertion error', 'there was an error while importing to the database !')
        self.database_manager()
    def database_manager(self):
        self.data = []
        self.database = sqlite3.connect("database.db")
        self.cursor = self.database.cursor()
        data = self.cursor.execute("select * from data;").fetchall()
        for obj in data:
            if obj[0]:
                self.data.append([obj[0], obj[1], obj[2], obj[3]])
        self.button_creator()
    def button_creator(self):
        x = 1
        y = 200
        counter = 0
        self.button_list = []
        obj_list_of_task_gui = []
        for task in self.data:
            globals()[f"self.{task[0]}"] = tkinter.Button(text=f"{task[0]}", bg="yellow", fg="black", height=1, width=7)


        for btn in self.data:
            globals()[f"self.{btn[0]}"].place(x=x, y=y)
            globals()[f"{btn[0]}_class"] = task_class(self.root, btn[0])
            globals()[f"self.{btn[0]}"].config(command=globals()[f"{btn[0]}_class"].run)
            x += 100
            counter += 1
            if counter >= 4:
                counter = 0
                y += 50
                x = 1
            if y >= self.max_heigth:
                self.max_heigth += 100
                self.root.update()
        self.root.update()
    def button_destroy(self):
        database = sqlite3.connect("database.db")
        newdata = database.cursor().execute("SELECT * FROM data;").fetchall()
        newData =[]
        for obj in newdata:
            if obj[0]:
                newData.append([obj[0], obj[1], obj[2], obj[3]])
        print(newData)
        print(self.data)
        if self.data != newData:
            for obj in newData :
                try:
                    self.data.remove(obj)
                except:
                    pass
            for obj in self.data:
                globals()[f"self.{obj[0]}"].destroy()
    def GUI(self):

        self.root.title("Hattson Task-To-Do")
        self.root.config(height=self.max_heigth, width=self.max_width, bg="black")
        self.task_name_la = tkinter.Label(self.root, text="Task Name : ", fg="white", bg='black')
        self.task_name_la.place(x=20, y=50)
        self.task_name_en = tkinter.Entry(self.root, bg="white", fg="black")
        self.task_name_en.place(x=200, y=50)
        self.task_parts_la = tkinter.Label(self.root, bg="black", fg="white", text="Task Parts : ")
        self.task_parts_la.place(x=20, y=100)
        self.task_parts_en = tkinter.Spinbox(self.root, bg="white", fg="black", from_=1, to=200)
        self.task_parts_en.place(x=200, y=100)
        self.ref_btn = tkinter.Button(self.root, bg="blue", text="Refresh", fg="white", command=self.button_destroy)
        self.ref_btn.place(x=105, y=150)
        self.submit_btn = tkinter.Button(self.root, bg="green", fg="white", text="Create Task", command=self.creat_task, height=1, width=7)
        self.submit_btn.place(x=282, y=150)

        self.exit_btn = tkinter.Button(self.root, bg="red", fg="white", text="Exit", command=self.root.destroy, height=1, width=3)
        self.exit_btn.place(x=200, y=150)
        # self.button_creator()

        self.root.mainloop()

    def run(self):
        self.GUI()


app = MainClass()
app.run()



