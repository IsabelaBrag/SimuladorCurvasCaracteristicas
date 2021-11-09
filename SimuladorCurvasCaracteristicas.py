from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import sys
import numpy as np
import matplotlib.pyplot as plt
from tempfile import TemporaryFile



class myTable(object):

    def __init__(self, **kw):
        ws = Tk()
        f = ('Calibri', 12)
        var = StringVar()
        self.root = ws
        self.root.title("Parameters Input")
        self.root.geometry('450x600+450+30')
        self.root.resizable(False,False)
        self.register_type = 1
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
        self.register_mobility = Entry(self.right_frame, font=('Calibri', 11))
        self.register_lenght = Entry(self.right_frame, font=('Calibri', 11))
        self.register_width = Entry(self.right_frame, font=('Calibri', 11))
        self.register_threhold = Entry(self.right_frame, font=('Calibri', 11))
        self.register_thickness = Entry(self.right_frame, font=('Calibri', 11))
        self.register_mobility.place(x=300, y=50, width=80)
        self.register_lenght.place(x=300, y=90, width=80)
        self.register_width.place(x=300, y=130, width=80)
        self.register_threhold.place(x=300, y=170, width=80)
        self.register_thickness.place(x=300, y=210, width=80)
    
        gender_frame_type = LabelFrame(self.right_frame, bg='#CCCCCC', padx=0, pady=0)
        typeN = Radiobutton(gender_frame_type,
                            text='Type N',
                            bg='#CCCCCC',
                            variable=var,
                            value='typeN',
                            command= lambda: self.get_registers_types(var.get()),
                            font=('Calibri', 10),
                            )
       
        typeP = Radiobutton(gender_frame_type,
                            text='Type P',
                            bg='#CCCCCC',
                            variable=var,
                            value='typeP',
                            command= lambda: self.get_registers_types(var.get()),
                            font=('Calibri', 10),
                            )
        gender_frame_type.place(x=270, y=10)
        typeN.pack(side=LEFT)
        typeP.pack(side=RIGHT)

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
        register_numberCurves = ttk.Combobox(self.gender_frame_output, values=["1", "2", "3", "4", "5", "6"], name="labelframe3")
        register_numberCurves.place(x=120, y=200, width=40)
        register_numberCurves.bind('<<ComboboxSelected>>', self.create_entries)
        

        self.output_btn = Button(self.gender_frame_output, 
            width=15, 
            text='Plot OutPut Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            command=self.calculator_output)
        self.output_btn.place(x=45, y= 250, height=25)
        
        self.register_start = Entry(self.gender_frame_output, font=('Calibri', 11))
        self.register_step = Entry(self.gender_frame_output, font=('Calibri', 11))
        self.register_end = Entry(self.gender_frame_output, font=('Calibri', 11))
        self.register_start.place(x=120, y=80, width=40)
        self.register_step.place(x=120, y=120, width=40)
        self.register_end.place(x=120, y=160, width=40)

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
        self.register_start2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        self.register_step2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        self.register_end2 = Entry(self.gender_frame_transfer, font=('Calibri', 11))
        self.register_start2.place(x=120, y=80, width=40)
        self.register_step2.place(x=120, y=120, width=40)
        self.register_end2.place(x=120, y=160, width=40)
        register_numberCurves2 = ttk.Combobox(self.gender_frame_transfer, values=["1", "2", "3", "4", "5", "6"], name="labelframe4")
        register_numberCurves2.place(x=120, y=200, width=40)
        register_numberCurves2.bind('<<ComboboxSelected>>', self.create_entries)

        self.transfer_btn = Button(self.gender_frame_transfer, 
            width=16, 
            text='Plot Transfer Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            name='transfer',
            command=self.calculator_transfer
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

        print(event.widget._name)
        name = event.widget._name
        amount = event.widget.get()
        self.amountVG = amount
        count = 0
        values = []
        # Removes previous entries from the frame
        for entry in self.entries:
            if (name in str(entry)):
                entry.destroy()
            else:
                count+=1
                values.append(entry)

        self.entries = []
        self.entries = values

        for i in range(int(amount)):
            self.entries.append(self.add_new(i, name == "labelframe3"))

        # If numbers of curves is greater than 3, increase window size
        # Else return window to original size
        if int(amount) > 3:
            self.resize("450x640", 2)
        elif count <= 3:
            self.resize("450x600", 1)

    def add_new(self, position, curve):
        """
        Creates a new entry widget by the position specified
        :return: Entry widget
        """
        f = ('Calibri', 11)
        x_position = 40 + (50 * position)

        def clear_search(event):
            new_entry.delete(0, END)
        
        new_entry = Entry(self.gender_frame_output if curve else self.gender_frame_transfer, font=f, fg='grey')
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

    def get_registers_types (self, value):
        
        if value == 'typeP':
            print(value)
            self.register_type = -1

        else:
            self.register_type = 1

    def get_registers_for_meters (self, curve):
        print (curve)
        #Fazer tratamento para metros

        #self.u = float(self.register_mobility.get())*(10**-4)
        self.u = float(0.01)*(10**-4)
        print(self.u)
        #self.Z = float(self.register_lenght.get())*(10**-3)
        self.Z = float(100)*(10**-3)
        print(self.Z)
        #self.L = float(self.register_width.get())*(10**-6)
        self.L = float(100)*(10**-6)
        print(self.L)
        #self.Vth = float(self.register_threhold.get())
        self.Vth = float(1)
        print(self.Vth)
        #self.d = float(self.register_thickness.get())*(10**-9)
        self.d = float(5)*(10**-9)
        print(self.d)
        self.start = float( self.register_start.get() if curve else self.register_start2.get())
        print(self.start)
        self.step = float(self.register_step.get() if curve else self.register_step2.get())
        print(self.step)
        self.end = float(self.register_end.get() if curve else self.register_end2.get())
        print(self.end)

        self.VG = []
        self.VDS = []

        label_name = "labelframe3"
        if not curve:
            label_name = "labelframe4"

        for entry in self.entries:
            if (label_name in str(entry)):
                if curve:
                    self.VG.append(float(entry.get()))
                else:
                    self.VDS.append(float(entry.get()))

        print(self.VG)
        print('---VDS------>')
        print(self.VDS)

    def calculator_transfer (self):
        self.calculator_output(False)

    def calculator_output (self, curve = True):
        self.get_registers_for_meters(curve)
        eo = 8.85*(10**-12)
        k = 4
        Ci = (eo*k)/self.d
#Calculo p/ "Output curve" (IdxVds)- Regiao linear (Vd<(Vg-Vth)) e Região Saturação (Vd>(Vg-Vth))  
#function result = calcule_output(type)
        Rep = int(self.end/self.step)
        referencia = self.register_type
        passo = self.step
        start = int(self.start)
        Id = np.zeros((Rep,2))
        

        plt.figure()

        if(curve):
            Vds = self.start*referencia
            for Vg in self.VG:
                for j in range(start, Rep):
                    if ((Vg*referencia)<self.Vth and referencia == -1) or ((Vg*referencia)>self.Vth and referencia == 1):
                        if (Vds>=((Vg*referencia)-self.Vth) and referencia == -1) or (Vds<=((Vg*referencia)-self.Vth) and referencia == 1):
                            Id[j,0]=(self.Z/self.L)*self.u*Ci*((Vg*referencia)-self.Vth-(Vds/2))*Vds
                        elif (Vds<=((Vg*referencia)-self.Vth) and referencia == - 1) or (Vds>=((Vg*referencia)-self.Vth) and referencia == 1):
                            Id[j,0]=((self.Z*self.u*Ci)/(2*self.L))*(((Vg*referencia)-self.Vth)**2)
                    Id[j,1]=Vds
                    Vds=Vds+(passo*referencia)

                Vds=self.start*referencia
                
                x=(Id[:,1])
                y=(Id[:,0])
                print('-------')
                print('aaaaaaaaaaa')
                print(x,y)
                plt.plot(x,y, label = 'Vg = ')
                Vg=Vg+1
        else:
            Vg=self.start*referencia

            for Vds in self.VDS:
                for j in range(start, Rep):
                    if (Vg<self.Vth and referencia == -1) or (Vg>self.Vth and referencia == 1):
                        if ((Vds*referencia)>=(Vg-self.Vth) and referencia == -1) or ((Vds*referencia)<=(Vg-self.Vth) and referencia == 1):
                            Id[j,0]=(self.Z/self.L)*self.u*Ci*(Vg-self.Vth-((Vds*referencia)/2))*(Vds*referencia)
                        elif ((Vds*referencia)<=(Vg-self.Vth) and referencia == - 1) or ((Vds*referencia)>=(Vg-self.Vth) and referencia == 1):
                            Id[j,0]=((self.Z*self.u*Ci)/(2*self.L))*((Vg-self.Vth)**2)
                    Id[j,1]=Vg
                    Vg=Vg+(passo*referencia)

                Vg=self.start*referencia
                
                self.x=(Id[:,1])
                self.y=(Id[:,0])
                plt.semilogy(self.x,self.y)
                Vg=Vg+1

        plt.xlabel("Vds(V)" if curve else "Vg(V)", size = 12)
        plt.ylabel("ID(A)", size = 12)
        plt.title("OutPut Curve" if curve else "Transfer Curve", 
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'size': 16})
     
        '''file_name = "calculedValues"
        file = open(file_name + '.dat', 'w')
        file.write("ID(A) " + str(self.x))
        file.write(("VG" if curve else "VDS") + " = " + str(self.y))
        
        #
        file.close()'''
        #data = self.x
        #with open('your_data.dat', 'wb') as your_dat_file:  
        #    your_dat_file.write(struct.pack(len(data), data))
        
        #np.save('ID(A)', self.x)
        #np.save("VDS", self.y)
        plt.tight_layout() #ajustar eixo dos x
        legend = []
        for Value in self.VG if curve else self.VDS:
            legend.append(("VG" if curve else "VDS")+ " = " + str(Value))

        plt.legend(legend)
        plt.show()

        
    def execute(self):
        self.root.mainloop()


def main(args):
    app_proc = myTable()
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
