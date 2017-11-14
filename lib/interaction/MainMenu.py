from tkinter import *
from xml.etree.ElementTree import ElementTree
import datetime

import os


class MainMenu(object):
    def __init__(self):
        self.__user = None
        self.__tk = Tk()
        self.__tk.title("Tågbokning")
        self.__tk.geometry("200x500")
        self.__trains = []

        a = Label(self.__tk, text="Boka tåg")
        a.pack()
        a = Frame(self.__tk)
        a.pack(pady=10)

        self.__btn_get_ticket = Button(self.__tk, text="Get yo tickets",
                                       command=lambda: self.print_ticket())

        self.__user_label = Label(a, text="No user")
        self.__btn_login = Button(a, text="Login", command=lambda: self.promt_login())
        self.__user_label.pack(side=LEFT)
        self.__btn_login.pack(side=LEFT)
        self.__btn_view_train = Button(self.__tk, text="view train", command=lambda: self.view_selected_train())
        self.__btn_view_train["state"] = "disabled"
        self.__btn_view_train.pack()
        self.__train_table = Listbox(height=5)
        self.__train_table.bind('<<ListboxSelect>>', lambda x: self.update_user_info(self.__get_selected_train()))
        self.__train_table.pack(pady=5)
        self.__btn_get_ticket.pack()
        self.__btn_get_ticket["state"] = "disabled"
        self.__btn_user_info_train = Label(self.__tk, text="view train")
        self.__btn_user_info_train.pack()

    def update_user_info(self, train):
        text_to_seat = ""
        if train is not None:
            text_to_seat = train.summary_display(self.__user)

        try:
            self.__btn_user_info_train["text"] = text_to_seat
        except:
            print("cant access btn-user info")

    def print_ticket(self):
        if self.__user is None:
            return
        a = self.__user
        filename = "{}_{}_{}".format(a.get_ID(), a.name, "ticket.txt")
        file = open(filename, "w", encoding="utf-8")
        file.write("Train bookings for: \n{1} ( ID: {0})\n".format(a.get_ID(), a.name))
        for i in self.__trains:
            bookings = i.get_bookings(a)
            if bookings is not None:
                file.write("\nTrain: {}\n".format(i.get_name()))
                file.write(bookings.get_file_string())

        file.close()
        import tkinter.messagebox
        answer = tkinter.messagebox.askyesno("Done", "Tickets are now printed to file\nOpen file?")
        if answer:
            import os, sys

            os.startfile(os.path.join(os.path.dirname(os.path.realpath(sys.modules['__main__'].__file__)), filename))

    def promt_login(self):
        from lib.occupant import Person
        self.__set_user(Person(12345, "Sven"))
        # self.__set_user(Person(11114, "Åke"))
        t = self.__get_selected_train()
        if t is None:
            return
        self.update_user_info(t)

        return True

    def __logout_user(self):
        self.__user_label["text"] = "No user"
        self.__btn_login["command"] = lambda: self.promt_login()
        self.__user = None
        self.__btn_view_train["state"] = "disabled"
        self.__btn_get_ticket["state"] = "disabled"
        t = self.__get_selected_train()
        if t is None:
            return
        self.update_user_info(t)

    def __set_user(self, user):
        from lib.occupant import Occupant
        if not isinstance(user, Occupant):
            raise ValueError("Wrong typ. Needs to be ")
        self.__user_label["text"] = user.__str__()
        self.__btn_login["command"] = lambda: self.__logout_user()
        self.__user = user
        self.__btn_view_train["state"] = "normal"
        self.__btn_get_ticket["state"] = "normal"

    def add_train(self, new_train, compare_time=datetime.datetime.today()):
        """Adds train if the departure time if after right now."""
        from lib.train.train import Train
        if not isinstance(new_train, Train):
            raise ValueError("Not of type Train")

        if new_train.get_schedule().get_departure_time() < compare_time:
            return False

        self.__trains.append(new_train)
        return True

    def __get_selected_train(self):
        """Returns the selected train. Returns None if non is selected."""
        try:
            return self.__trains[(int(self.__train_table.get(self.__train_table.curselection()[0])[1:3])) - 1]
        except IndexError:
            print("Non selected")
            return None

    def view_selected_train(self):
        """Opens a TrainWindow for the selected train."""
        current_train = self.__get_selected_train()
        if current_train is None:
            return
        from lib.interaction.gui import TrainWindow

        # Creates a window for the __train and shows it + hides mainMenu.
        current_train_window = TrainWindow(self, current_train, self.__user)
        self.hide_window()
        current_train_window.display()
        self.unhide_window()
        self.update_user_info(current_train)

        pass

    def unhide_window(self):
        try:
            self.__tk.deiconify()
        except:
            print("already closed()")
        self.update_user_info(self.__get_selected_train())

    def hide_window(self):
        self.__tk.withdraw()

    def populate_train_table(self):
        index = 0
        for train in self.__trains:
            index += 1
            self.__train_table.insert(10, "#{1:2} {0}".format(train.train_table_display(), index))

    def start_ui(self):
        self.populate_train_table()
        self.__tk.mainloop()

    def get_trains(self):
        return self.__trains


if __name__ == '__main__':
    from lib.train.train import Train
    from lib.train.wagon import Wagon

    from lib.booking.schedule import Schedule

    ob = Schedule()
    from lib.booking.destination import Destination

    ob.add_destination(Destination("Fjollträsk"))
    ob.add_destination(Destination("Mesberg"))
    ob.add_destination(Destination("Sumptuna"))

    t1 = Train("X123")
    t1.add_wagon(Wagon(t1, 1, 4, 5))

    t2 = Train("Y321")
    t2.add_wagon(Wagon(t2, 1, 2, 6))

    # a_path = os.path.abspath(os.path.join("a.xml"))
    # a = ElementTree()
    # a.write(a_path)
    #  file = open("../train/train_1.txt", "r", encoding="utf8")
    # t3 = Train.read_from_file(file)
    # file.close()
    t1.set_schedule(ob)
    t2.set_schedule(ob)

    ob = MainMenu()
    ob.add_train(t1)
    ob.add_train(t2)
    # ob.add_train(t3)
    ob.start_ui()
