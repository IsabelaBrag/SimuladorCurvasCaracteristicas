from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import sys


class myTable(object):

    def __init__(self, **kw):
        ws = Tk()
        f = ('Calibri', 12)
        var = StringVar()
        self.root = ws
        self.root.title("Parameters Input")
        self.root.geometry('450x600+450+30')
        self.root.resizable(False,False)
        self.create_help_menu()
        self.create_status_welcome()
        self.entries = []

        # self.put_parameters

        self.right_frame = Frame(ws, borderwidth=2, bg="#CCCCCC", relief="solid")
        self.right_frame.place(x=0, y=0, width=450, height=580)

        Label(self.right_frame, text="Select the channel Type", bg='#CCCCCC', font=f).place(x=70, y=12)
        Label(self.right_frame, text="u - mobility(cm²*v^-1*s^-1)", bg='#CCCCCC', font=f).place(x=70, y=50)
        Label(self.right_frame, text="Z - channel length(mm)", bg='#CCCCCC', font=f).place(x=70, y=90)
        Label(self.right_frame, text="L - channel width(µm)", bg='#CCCCCC', font=f).place(x=70, y=130)
        Label(self.right_frame, text="Vth - threhold voltage(V)", bg='#CCCCCC', font=f).place(x=70, y=170)
        Label(self.right_frame, text="d - oxide thickness(nm)", bg='#CCCCCC', font=f).place(x=70, y=210)
        register_mobility = Entry(self.right_frame, font=('Calibri', 11))
        register_lenght = Entry(self.right_frame, font=('Calibri', 11))
        register_width = Entry(self.right_frame, font=('Calibri', 11))
        register_threhold = Entry(self.right_frame, font=('Calibri', 11))
        register_thickness = Entry(self.right_frame, font=('Calibri', 11))
        register_mobility.place(x=300, y=50, width=80)
        register_lenght.place(x=300, y=90, width=80)
        register_width.place(x=300, y=130, width=80)
        register_threhold.place(x=300, y=170, width=80)
        register_thickness.place(x=300, y=210, width=80)

        gender_frame_type = LabelFrame(self.right_frame, bg='#CCCCCC', padx=0, pady=0)
        typeN = Radiobutton(gender_frame_type,
                            text='Type N',
                            bg='#CCCCCC',
                            pady=0,
                            variable=var,
                            value='typeN',
                            font=('Calibri', 10),
                            )
        typeP = Radiobutton(gender_frame_type,
                            text='Type P',
                            bg='#CCCCCC',
                            pady=0,
                            variable=var,
                            value='typeP',
                            font=('Calibri', 10),
                            )
        gender_frame_type.place(x=270, y=10)
        typeN.pack(expand=True, side=LEFT)
        typeP.pack(expand=True, side=LEFT)

        gender_frame_values = LabelFrame(self.right_frame, bg='#CCCCCC', padx=0, pady=0)
        Label(gender_frame_values, text="Values of Curves", bg='#CCCCCC', font=('Calibri', 12, font.BOLD)).grid(sticky=W,
                                                                                                   padx=155)
        gender_frame_values.place(x=0, y=250, width=446)

        self.gender_frame_output = LabelFrame(self.right_frame, bg='#CCCCCC', padx=0, pady=0)
        Label(self.gender_frame_output, text="OutPut Curve", bg='#CCCCCC', font=('Calibri', 12, font.BOLD)).grid(sticky=W,
                                                                                                    padx=55)
        self.gender_frame_output.place(x=0, y=280, width=223, height=295)
        Label(self.gender_frame_output, text="Enter drain/source voltages \n 'VDS'", bg='#CCCCCC',
              font=('Calibri', 12)).grid(
            row=12, sticky=W, padx=15)
        Label(self.gender_frame_output, text="Start", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=80)
        Label(self.gender_frame_output, text="Step", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=120)
        Label(self.gender_frame_output, text="End", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=160)
        Label(self.gender_frame_output, text="N° Curves", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=200)
        register_numberCurves = ttk.Combobox(self.gender_frame_output, values=["1", "2", "3", "4", "5", "6"])
        register_numberCurves.place(x=120, y=200, width=40)
        register_numberCurves.bind('<<ComboboxSelected>>', self.create_entries)
        
        self.output_btn = Button(self.gender_frame_output, 
            width=15, 
            text='Plot OutPut Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            command=None
        )
        self.output_btn.place(x=45, y= 250, height=25)
        self.output_btn.bind('<<Button>>', self.create_entries)

        register_start = Entry(self.gender_frame_output, font=('Calibri', 11))
        register_step = Entry(self.gender_frame_output, font=('Calibri', 11))
        register_end = Entry(self.gender_frame_output, font=('Calibri', 11))
        register_start.place(x=120, y=80, width=40)
        register_step.place(x=120, y=120, width=40)
        register_end.place(x=120, y=160, width=40)

        self.gender_frame_transfer = LabelFrame(self.right_frame, bg='#CCCCCC', padx=0, pady=0)
        Label(self.gender_frame_transfer, text="Transfer Curve", bg='#CCCCCC', font=('Calibri', 12, font.BOLD)).grid(
                                                                                                        sticky=W,
                                                                                                        padx=55)
        self.gender_frame_transfer.place(x=223, y=280, width=223, height=295)
        Label(self.gender_frame_transfer, text="Enter gate voltages \n 'VG'", bg='#CCCCCC', font=('Calibri', 12)).grid(
            sticky=W,
            padx=40)
        Label(self.gender_frame_transfer, text="Start", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=80)
        Label(self.gender_frame_transfer, text="Step", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=120)
        Label(self.gender_frame_transfer, text="End", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=160)
        Label(self.gender_frame_transfer, text="N° Curves", bg='#CCCCCC', font=('Calibri', 12)).place(x=40, y=200)
        register_start2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        register_step2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        register_end2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        register_start2.place(x=120, y=80, width=40)
        register_step2.place(x=120, y=120, width=40)
        register_end2.place(x=120, y=160, width=40)
        register_numberCurves2 = ttk.Combobox(self.gender_frame_transfer, values=["1", "2", "3", "4", "5", "6"])
        register_numberCurves2.place(x=120, y=200, width=40)
        register_numberCurves2.bind('<<ComboboxSelected>>', self.create_entries2)

        self.transfer_btn = Button(self.gender_frame_transfer, 
            width=16, 
            text='Plot Transfer Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            command=None
        )
        self.transfer_btn.place(x=40, y= 250, height=25)

    def create_help_menu(self):
        menu = tk.Menu(self.root)

        helpmenu = tk.Menu(menu, tearoff=0)
        helpmenu.add_command(label="About", command=self.menu_about)

        menu.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menu)

    def menu_about(self):
        msg = "Este programa tem como objetivo a partir dos dados inseridos, realizar a plotagem das curvas características."

        messagebox.showinfo("Thin-film transistors characteristic curve simulator", msg)

    def create_status_welcome(self):
        self.status = tk.Label(self.root,
                               text="Welcome to the characteristic curve simulator! :)",
                               bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def create_entries(self, event):
        """
        Creates a list of entry fields by the amount specified

        :param event: triggered event (Number selected by the user)
        """
        amount = event.widget.get()
        count = 0
        values = []
        # Removes previous entries from the frame
        for entry in self.entries:
            if ("labelframe3" in str(entry)):
                entry.destroy()
            else:
                count+=1
                values.append(entry)

        self.entries = []
        self.entries = values

        for i in range(int(amount)):
            self.entries.append(self.add_new(i))

        # If numbers of curves is greater than 3, increase window size
        # Else return window to original size
        if int(amount) > 3:
            self.resize("450x640", 2)
        elif count <= 3:
            self.resize("450x600", 1)

    def create_entries2(self, event):

        amount = event.widget.get()
        count = 0
        values = []
        for entry in self.entries:
            print("LABEL 2" + str(entry))
            if ("labelframe4" in str(entry)):
                entry.destroy()
                
            else:
                count+=1
                values.append(entry)

        self.entries = []
        self.entries = values
        for j in range(int(amount)):
            self.entries.append(self.add_new2(j))
        print(count)
        if int(amount) > 3:
            self.resize2("450x640", 2)
        elif count <= 3:
            
            self.resize2("450x600", 1)

    def add_new(self, position):
        """
        Creates a new entry widget by the position specified

        :param position: entry field position (starting by "N° Curves" Label)"
        :return: Entry widget
        """
        f = ('Calibri', 11)

        
        x_position = 40 + (50 * position)

        def clear_search(event):
            new_entry.delete(0, END) 
        
        new_entry = Entry(self.gender_frame_output, font=f, fg='grey')
        new_entry.insert(0, "VG" + str(position + 1))
        new_entry.bind("<Button-1>", clear_search)

        # Decide in with row the new entry will be placed
        if position < 3:
            new_entry.place(x=x_position, y=230, width=40)
            
        else:
            new_entry.place(x=x_position - 150, y=260, width=40)

        return new_entry

    def resize(self, new_size, amount):
        """
        Resize the root frame by the new size

        :param amount: how many Calibri all frames will be increased
        :param new_size: Root frame new size
        """
        self.gender_frame_output.place(x=0, y=280, width=223, height=255 + (amount * 40))
        self.gender_frame_transfer.place(x=223, y=280, width=223, height=255 + (amount * 40))
        self.right_frame.place(x=0, y=0, width=450, height=540 + (amount * 40))
        self.transfer_btn.place(x=45, y = (260 if amount == 1 else 295), height=25)
        self.output_btn.place(x=45, y = (260 if amount == 1 else 295), height=25)
        self.root.geometry(new_size)

    def add_new2(self, position):

        x_position = 40 + (50 * position)
        def clear_search2(event):
            new_entry2.delete(0, END) 
        f = ('Calibri', 11)

        new_entry2 = Entry(self.gender_frame_transfer, font=f, fg='grey')
        new_entry2.insert(0, "VDS" + str(position + 1))
        new_entry2.bind("<Button-1>", clear_search2)

        # Decide in with row the new entry will be placed
        if position < 3:
            new_entry2.place(x=x_position, y=230, width=40)
        else:
            new_entry2.place(x=x_position - 150, y=260, width=40)

        return new_entry2

    def resize2(self, new_size, amount):

        self.gender_frame_output.place(x=0, y=280, width=223, height=255 + (amount * 40))
        self.gender_frame_transfer.place(x=223, y=280, width=223, height=255 + (amount * 40))
        self.right_frame.place(x=0, y=0, width=450, height=540 + (amount * 40))
        self.output_btn.place(x=45, y = (260 if amount == 1 else 295), height=25)
        self.transfer_btn.place(x=45, y = (260 if amount == 1 else 295), height=25)
        self.root.geometry(new_size)


    def execute(self):
        self.root.mainloop()


def main(args):
    app_proc = myTable()
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
