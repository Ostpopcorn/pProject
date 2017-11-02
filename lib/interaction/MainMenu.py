from tkinter import *


class MainMenu(object):
    def __init__(self):
        self.__user = None
        self.__tk = Tk()
        self.__tk.geometry("100x250")
        self.__trains = []

        a = Label(self.__tk, text="Boka tåg")
        a.pack()
        a = Frame(self.__tk)
        a.pack(pady=10)
        self.__user_label = Label(a, text="No user")
        self.__btn_login = Button(a, text="Login", command=lambda: self.promt_login())
        self.__user_label.pack(side=LEFT)
        self.__btn_login.pack(side=LEFT)
        self.__btn_view_train = Button(self.__tk, text="view train", command=lambda: self.view_selected_train())
        self.__btn_view_train["state"] = "disabled"
        self.__btn_view_train.pack()
        self.__train_table = Listbox()
        self.__train_table.pack()

    def promt_login(self):
        from lib.occupant import Person
        self.__set_user(Person(1234,"Sven"))
        return True

    def __logout_user(self):
        self.__user_label["text"] = "No user"
        self.__btn_login["command"] = lambda: self.promt_login()
        self.__user = None
        self.__btn_view_train["state"] = "disabled"

    def __set_user(self, user):
        from lib.occupant import Occupant
        if not isinstance(user, Occupant):
            raise ValueError("Wrong typ. Needs to be ")
        self.__user_label["text"] = user.__str__()
        self.__btn_login["command"] = lambda: self.__logout_user()
        self.__user = user
        self.__btn_view_train["state"] = "normal"

    def add_train(self, new_train):
        if not isinstance(new_train, Train):
            raise ValueError("Not of type Train")
        self.__trains.append(new_train)

    def view_selected_train(self):
        print("hej")
        try:
            currentindex = (int(self.__train_table.get(self.__train_table.curselection()[0])[1:3]))
        except IndexError:
            print("Non selected")
            return
        print(int(self.__train_table.get(self.__train_table.curselection()[0])[1:3]))

        from lib.interaction.gui import TrainWindow

        from lib.booking.schedule import Schedule
        ob = Schedule()
        from lib.booking.destination import Destination
        ob.add_destination(Destination("Fjollträsk"))
        ob.add_destination(Destination("Mesberg"))
        ob.add_destination(Destination("Sumptuna"))
        self.__trains[currentindex - 1].set_schedule(ob)
        a = TrainWindow(self.__trains[currentindex-1],self.__user,[0])
        self.hide_window()
        a.display()
        a.withdraw_root()
        self.unhide_window()

        pass

    def unhide_window(self):
        self.__tk.deiconify()

    def hide_window(self):
        self.__tk.withdraw()

    def populate_train_table(self):
        index = 0
        for train in self.__trains:
            index += 1
            self.__train_table.insert(10, "#{1:2} {0}".format(train.train_table_display(), index))

    def start_ui(self):
        self.__tk.mainloop()


if __name__ == '__main__':
    from lib.train.train import Train
    from lib.train.wagon import Wagon

    t1 = Train("X123")
    t1.add_wagon(Wagon(1, 4, 5))
    t2 = Train("Y321")
    t2.add_wagon(Wagon(1, 2, 6))
    ob = MainMenu()
    ob.add_train(t1)
    ob.add_train(t2)
    ob.populate_train_table()
    ob.start_ui()
