from datetime import datetime
from os import name
from statistics import median, variance
from tkinter import *
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button as But
from tempfile import TemporaryFile
from tkinter import filedialog
import pandas as pd
from numpy.core.records import array
from pandas.core.frame import DataFrame
from copy import deepcopy
from scipy import signal
from statistics import *

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
        self.create_file_menu()
        self.create_status_welcome()
        self.entries = []
        
        # self.put_parameters

        self.right_frame = Frame(ws, borderwidth=2, bg="#CCCCCC", relief="solid")
        self.right_frame.place(x=0, y=0, width=450, height=580)
        
        Label(self.right_frame, text="Select the channel Type", bg='#CCCCCC', font=f).place(x=70, y=12)
        Label(self.right_frame, text="μ - mobility(cm²*v^-1*s^-1)", bg='#CCCCCC', font=f).place(x=70, y=50)
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
            command=self.calculator_transfer
        )
        self.transfer_btn.place(x=40, y= 250, height=25)
        
    def create_file_menu(self):
        menuFile = tk.Menu(self.root)

        filemenu = tk.Menu(menuFile, tearoff=0)
        filemenu.add_command(label="Help", command=self.menu_help)
        filemenu.add_command(label="About", command=self.menu_about)

        menuFile.add_cascade(label="File", menu=filemenu)

        self.root.config(menu=menuFile)
        
        
    def get_files(self):

        filename = filedialog.askopenfilename(initialdir="/",
                                            title="Select a File",
                                            filetypes=(("Dat files",
                                                        "*.dat*"),
                                                        ("Text files",
                                                        "*.txt*")))
        return filename
    
    def import_file(self, *args):
        
        file_path = self.get_files()

        with open(file_path, 'r') as file:
            if file_path.endswith(".txt"):
                # Processamento de arquivo .txt
                pass
            if file_path.endswith(".dat"):
                # Processamento de arquivo .dat
                pass
            
            self.Lines = file.readlines()
        
            count = 0
   
            self.array = [[] for i in range(7)]

            for line in self.Lines:
                count += 1
                print(len(line.split()))
                (self.array[0].append(float(line.split()[0])))
                (self.array[1].append(float(line.split()[1])))
                if (len(line.split()) > 2):
                    (self.array[2].append(float(line.split()[2])))
                if (len(line.split()) > 3):
                    (self.array[3].append(float(line.split()[3])))
                if (len(line.split()) > 4):
                    (self.array[4].append(float(line.split()[4])))
                if (len(line.split()) > 5):
                    (self.array[5].append(float(line.split()[5])))
                if (len(line.split()) > 6):
                    (self.array[6].append(float(line.split()[6])))
                
            print(self.array)
            
            self.plot_curves_import()
            
            
    def new_window_for_import_data(self):
        
        new_window = tk.Tk()
        
        new_window.title('File Explorer')
        new_window.geometry("400x450")
        new_window.config(background="white")
        
        
        label_file_explorer = Listbox(new_window)  
        scrollbar = Scrollbar(label_file_explorer)
        scrollbar.pack( side = RIGHT, fill = Y )
        scrollbar.config( command = label_file_explorer.yview )
        
        for line in self.Lines:
            label_file_explorer.insert(END, line)
        
        label_file_explorer.place(width= 400 , height=400)
        
        plot_output_curve = Button(new_window,             
            width=16, 
            text='Plot Output Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.plot_curves_import(True)
         )
        plot_output_curve.place(x = 30, y = 400)
        
        plot_transfer_curve = Button(new_window,             
            width=16, 
            text='Plot Transfer Curve', 
            font=("Calibri",12, font.BOLD), 
            relief=SOLID,
            cursor='hand2',
            command=lambda: self.plot_curves_import(False)
         )
        plot_transfer_curve.place(x = 230, y = 400)
        
        
    def plot_curves_import(self):
        
        self.ax.scatter(self.array[0], self.array[1])
        
        if len(self.array[2]) > 1:
            self.ax.scatter(self.array[0], self.array[2])
        
        if len(self.array[3]) > 1:
            self.ax.scatter(self.array[0], self.array[3])
            
        if len(self.array[4]) > 1: 
            self.ax.scatter(self.array[0], self.array[4])
            
        if len(self.array[5]) > 1: 
            self.ax.scatter(self.array[0], self.array[5])       
            
        if len(self.array[6]) > 1: 
            self.ax.scatter(self.array[0], self.array[6])       
        
        plt.tight_layout()
        
        plt.draw()
        
        self.ax2 = plt.axes([0.635, 0.0001, 0.156, 0.05])
        self.deviations = But(self.ax2, 'Deviation')      
        self.deviations.on_clicked(self.deviation)
        
    #region
    def deviation(self, *args):
        file_name = ("deviation" + str(datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")))
        file = open(file_name +'.dat', 'w+')
        
        for count in range(0,len(self.array_IDs)): 
            dados_simulados = self.array_IDs[count]
            
            print("DADOS SIMULADOS: ", self.array_IDs[count])
            
            media_dados_simulados = mean(dados_simulados)
            
            print("Média dados Simulados: ", media_dados_simulados)
            
            dados_experimentais = self.array[count+1]
            
            print("DADOS EXPERIMENTAIS: ", dados_experimentais)
            
            desvio_padrao_amostral = stdev(dados_experimentais,  media_dados_simulados)
            
            print("Calculo do desvio padrão: ", desvio_padrao_amostral)
                        
            # fator de idealidade
            # media_dados_experimentais = mean(dados_experimentais)
            # Ai = media_dados_experimentais / media_dados_simulados
            # A = float(Ai)
            # print("Fator de Idealidade - A = ", A)
            
            file.write("Curva (" + str(count+1) + "): ")
            file.write(str(desvio_padrao_amostral)+"\n")
            # file.write("Fator de Idealidade A* (" + str(count+1) + "): ")
            # file.write(str(A)+"\n")
            
            self.coeficiente_determinacao()
            
    def coeficiente_determinacao(self):
        
        file_name = ("coeficiente de determinacao" + str(datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")))
        file = open(file_name +'.dat', 'w+')
        
        # 1° Calcular a yex - ysim
        
        for index in range(1,len(self.array)):
        
            if len(self.array[index]) > 1:
                
                subtracao = np.zeros(len(self.array[index]))
                subtracao2 = np.zeros(len(self.array[index]))
                
                for tam in range(len(self.array[index])):
                    
                    subtracao[tam] = (self.array[index][tam] - self.array_IDs[index - 1][tam])**2
                
                somatoria_primeira_parte = sum(subtracao)
                
                print("somatoria_primeira_parte", somatoria_primeira_parte)
                    
                media_valores_experimentais = mean(self.array[index])
                
                for tam2 in range(len(self.array[index])):
                    
                    subtracao2[tam2] = (self.array[index][tam2] - media_valores_experimentais)**2
                    
                print ("subtracao2", subtracao2)
                
                somatoria_segunda_parte = sum(subtracao2)   
                
                print("somatoria_segunda_parte", somatoria_segunda_parte)
                
                coeficiente_rendimento = (1 - (somatoria_primeira_parte/somatoria_segunda_parte))    
                
                print ("coeficiente_rendimento", coeficiente_rendimento )
                
                file.write("Coef. Determinacao (" + str(index) + "): ")
                file.write(str(coeficiente_rendimento)+"\n")
        
            
    def menu_help(self):
        msg = """To run the program you need some rules, see the following instructions: 
               \r1- Select which type of channel is the device to be simulated
               \r2- Insert the data according to the indicated measurement unit
               \r3- Start indicates which position the curve should be started 
               \r4- Step indicates which variation of the curve points
               \r5- End indicates which end position of the curve
               \r6- N° Curves indicates which amount of Vds or Vg is desired
               \r7- According to the number of selected curves, add the values of each Vds or Vg set to form each curve 
               \r8- To plot the desired graph, click on the Plot Output Curve button or the Plot Transfer Curve button 
               \r9- To Import data click on File ---> Import Data, it is allowed to import data only if they are .dat or .txt
               \r10- When plotting each graph, the data calculated by the program are automatically saved"""

        messagebox.showinfo("Instructions for help", msg)
    #endregion   
        
    def menu_about(self):
        
        msg = """This program has as a goal, from the data entered or imported, plot the characteristic curves.
            \rInterface developed by Isabela Bragança Roque using Python 3.8.8 SP, January 19, 2022.
            \rMore information contact --> isabela.roque@unesp.com.br """
        
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
        new_entry.insert(0, ("VG" if curve else "VDS") + str(position + 1))
        
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
        self.u = float(0.7753)*(10**-4)
        print(self.u)
        #self.Z = float(self.register_lenght.get())*(10**-3)
        self.Z = float(5)*(10**-3)
        print(self.Z)
        #self.L = float(self.register_width.get())*(10**-6)
        self.L = float(100)*(10**-6)
        print(self.L)
        #self.Vth = float(self.register_threhold.get())
        self.Vth = float(33.06943)
        print(self.Vth)
        #self.d = float(self.register_thickness.get())*(10**-9)
        self.d = float(300)*(10**-9)
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
        print('Ci : ', Ci)
        arrayDatas_lines = []
        arrayDatas_columns = []
#Calculo p/ "Output curve" (IdxVds)- Regiao linear (Vd<(Vg-Vth)) e Região Saturação (Vd>(Vg-Vth))  

        Rep = int((self.end - self.start)/self.step)
        print('VALORES FINAIS', Rep)
        referencia = self.register_type
        passo = self.step
    
        #Id = np.zeros((int(Rep if Rep>0 else Rep*-1 == Rep ),2))
            
        Id = np.zeros((Rep,2))

        fig = plt.figure()
        
        self.ax = plt.subplot()
        
        self.array_IDs = []
        if(curve):
            Vds = self.start
            for Vg in self.VG:
                for j in range(Rep):
                    if (Vg < self.Vth and referencia == -1) or (Vg >= self.Vth and referencia == 1):
                        if (Vds >= Vg-(self.Vth) and referencia == -1) or (Vds <= Vg-self.Vth and referencia == 1):
                            Id[j,0]=(self.Z/self.L)*self.u*Ci*(Vg-self.Vth-(Vds/2))*Vds
                        elif (Vds <= Vg-(self.Vth) and referencia ==  -1) or (Vds >= Vg-self.Vth and referencia == 1):
                            Id[j,0]=((self.Z*self.u*Ci)/(2*self.L))*((Vg-self.Vth)**2)
                            
                    Id[j,1]=Vds
                    Vds=Vds+passo

                Vds=self.start
                
                x=deepcopy(Id[:,1])
                y=deepcopy(Id[:,0])

                print('aaaaaaaaaaa')
                print(x,y)
                
                self.array_IDs.append(y)
                print ("Testeeeee:", self.array_IDs)
                self.ax.plot(x,y, label = 'Vg = ')
                plt.tight_layout()
                axes = plt.axes([0.81, 0.00001, 0.2, 0.05])
                bnext = But(axes, 'Import Data',color="orange")
                bnext.on_clicked(self.import_file)
                
                
                arrayDatas_columns.append('ID(V), VG = ' + str(Vg))
                arrayDatas_lines.append(y)
                
            arrayDatas_columns.append("VDS(V)")
            arrayDatas_lines.append(x)
            arrayDatas = pd.DataFrame(arrayDatas_lines)
            arrayDatas = arrayDatas.T
            arrayDatas.columns = arrayDatas_columns
            print("DATAFRAME: ", arrayDatas)
            
            file_name_outputcurve = ("outputcurve" + str(datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")) + ".dat")
            arrayDatas.to_string(file_name_outputcurve , index=False)
            
                    
        else:
            Vg=self.start
            for Vds in self.VDS:
                for j in range(Rep):
                    # if (0 < Vg < self.Vth and referencia == 1 ):
                    #     Kp = 1.0    # gain
                    #     tau = 1.0   # time constant
                    #     zeta = 0.72 # damping factor
                    #     # (1) Transfer Function
                    #     num = [Kp]
                    #     den = [tau**2,2*zeta*tau,1]
                    #     sys1 = signal.TransferFunction(num,den)
                    #     t1,y1 =signal.step(sys1)
                    #     Id[j,0] = Id[j-1,0]

                    # if (Vg < self.Vth and referencia == 1)  :
                    #     uef = (Vg - self.Vth)*self.u
                    #     # #uef = (1/Ci)*(self.L/self.Z)*(diff())
                    #     # Id[j,0]=(self.Z/self.L)*uef*10**-8*Ci*(Vg-self.Vth)*(Vds)
                    #     Id[j,0]= 0.0
                    # if (Vg <= 0 and referencia == 1):
                    #if (Vds > (Vg-self.Vth)):
                            
                    #         Id[j,0]=(self.Z/self.L)*-self.u*10**-7*Ci*(Vg-self.Vth)*Vds                   
                    if (Vg < self.Vth and referencia == -1) or (Vg >= self.Vth and referencia == 1):
                        if ((Vds)>=(Vg-self.Vth) and referencia == -1) or ((Vds)<=(Vg-self.Vth) and referencia == 1):
                            Id[j,0]=(self.Z/self.L)*self.u*Ci*(Vg-self.Vth-(Vds/2))*(Vds)
                        elif ((Vds)<=(Vg-self.Vth) and referencia == -1) or ((Vds)>=(Vg-self.Vth) and referencia == 1):
                            Id[j,0]=((self.Z*self.u*Ci)/(2*self.L))*((Vg-self.Vth)**2)
                    
                    
                    Id[j,1]=Vg
                    Vg=Vg+(passo)

                Vg=self.start
                
                x1=deepcopy(Id[:,1])
                y2=deepcopy(Id[:,0])
                
                print("IIIIII***************", x1,y2)
                
                self.array_IDs.append(y2)
                self.ax.plot(x1,y2, label = 'Vg = ')
                
                axes = plt.axes([0.81, 0.00001, 0.2, 0.05])
                bnext = But(axes, 'Import Data',color="orange")
                bnext.on_clicked(self.import_file)
                
                
                arrayDatas_columns.append('ID(V), VDS = ' + str(Vds))
                arrayDatas_lines.append(y2)
                
            arrayDatas_columns.append("VG(V)")
            arrayDatas_lines.append(x1)
            arrayDatas = pd.DataFrame(arrayDatas_lines)
            arrayDatas = arrayDatas.T
            arrayDatas.columns = arrayDatas_columns
            print("DATAFRAME: ", arrayDatas)
            
            file_name_outputcurve = ("transfercurve" + str(datetime.now().strftime("_%m-%d-%Y_%H-%M-%S")) + ".dat")
            arrayDatas.to_string(file_name_outputcurve , index=False)
            
        self.ax.set_xlabel("Vds(V)" if curve else "Vg(V)", size = 12)
        self.ax.set_ylabel("ID(A)", size = 12)
        self.ax.set_title("OutPut Curve" if curve else "Transfer Curve", 
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'size': 16})
     

        # for i in [x,y]
        # for i in x:
        #     file.write(str(i) + '\n')
            
        # file.write('\t' +("VDS" if curve else "VGS") + '\n')
        # for j in y:
        #     file.write('\t' + str(j) + '\n')
        
        # file.close()
        
        #data = self.x
        #with open('your_data.dat', 'wb') as your_dat_file:  
        #    your_dat_file.write(struct.pack(len(data), data))
        
        #np.save('ID(A)', self.x)
        #np.save("VDS", self.y)
        plt.tight_layout() #ajustar eixo dos x
        legend = []
        for Value in self.VG if curve else self.VDS:
            legend.append(("VG" if curve else "VDS")+ " = " + str(Value))

        self.ax.legend(legend)
        plt.show()

        
    def execute(self):
        self.root.mainloop()


def main(args):
    app_proc = myTable()
    app_proc.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
