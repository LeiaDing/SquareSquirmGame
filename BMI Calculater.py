import tkinter
from tkinter import ttk
from tkinter import messagebox

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
window=tkinter.Tk()
window.title('BMI CALCULATER')
frame=tkinter.Frame(window)
frame.pack()



def Save_and_calculate():
    fname=fname_entry.get()
    lname=lname_entry.get()
    age=age_spinbox.get()
    height1 = height_entry.get()
    weight1 = weight_entry.get()

    #error message:
    error_messages = []
    if not fname:
        error_messages.append("First name must be filled.")
    if not lname:
        error_messages.append("Last name must be filled.")
    if not age:
        error_messages.append("Age must be filled.")
    if not height1:
        error_messages.append("Height must be filled.")
    if not weight1:
        error_messages.append("Weight must be filled.")

    # If there are any error messages, show them and return
    if error_messages:
        messagebox.showwarning("Missing Information", "\n".join(error_messages))

    height = float(height_entry.get())
    weight = float(weight_entry.get())
    BMI = weight / (height) ** 2
    if BMI>=29.2:
        Catogory='Obesity'
    elif BMI>=25:
        Catogory = 'Overweight'
    elif BMI>=18.5:
        Catogory = 'Normalweight'
    else:
        Catogory = 'Underweight'
    with open("BMI.txt", 'a') as BMIfilesave:
        BMIfilesave.write(fname + ' ' + lname + ' ' + age + ''+height1+' '+weight1+' '+str(BMI)+' '+Catogory+'\n')


    BMI_figure_lable.config(text=f"Your BMI:{BMI}")
    BMI_catogory_lable.config(text=f"BMI Catogory:{Catogory}")
    return BMI

def drawpiechart():
    piechartdata = {'underweight': 0, 'normalweight': 0, 'overweight': 0, 'obesity': 0}
    with open("BMI.txt",'r') as file1:
        for line in file1:
            linelist=line.strip().split()
            print(linelist)
            if 'Obesity'==linelist[-1]:
                piechartdata['obesity'] += 1
            elif 'Overweight'==linelist[-1]:
                piechartdata['overweight'] += 1
            elif 'Normalweight'==linelist[-1]:
                piechartdata['normalweight'] += 1
            else:
                piechartdata['underweight'] += 1
    print(piechartdata)


    for widget in BMI_piechart_frame.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots()
    ax.pie(piechartdata.values(), labels=piechartdata.keys(), autopct='%1.1f%%')
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=BMI_piechart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# the window view:

userinfo_frame=tkinter.LabelFrame(frame,text="user information")
userinfo_frame.grid(row=0,column=0)
fname_label=tkinter.Label(userinfo_frame,text="first name")
fname_label.grid(row=0,column=0)
fname_entry=tkinter.Entry(userinfo_frame)
fname_entry.grid(row=0,column=1)
lname_label=tkinter.Label(userinfo_frame,text="last name")
lname_label.grid(row=0,column=2)
lname_entry=tkinter.Entry(userinfo_frame)
lname_entry.grid(row=0,column=3)
age_label=tkinter.Label(userinfo_frame,text='age')
age_spinbox=tkinter.Spinbox(userinfo_frame,from_=18,to=50)
age_label.grid(row=0,column=4)
age_spinbox.grid(row=0,column=5)

BMI_input_frame=tkinter.LabelFrame(frame,text="BMI Input")
BMI_input_frame.grid(row=1,column=0)
height_lable=tkinter.Label(BMI_input_frame,text="Height")
height_lable.grid(row=2,column=0)
height_entry=tkinter.Entry(BMI_input_frame)
height_entry.grid(row=2,column=1)
weight_lable=tkinter.Label(BMI_input_frame,text="weight")
weight_lable.grid(row=2,column=2)
weight_entry=tkinter.Entry(BMI_input_frame)
weight_entry.grid(row=2,column=3)
Calculate_button=tkinter.Button(BMI_input_frame,text="Calculate",command=Save_and_calculate)
Calculate_button.grid(row=2,column=4)
BMI_output_frame=tkinter.LabelFrame(frame,text="BMI Output")
BMI_output_frame.grid(row=3,column=0)

BMI_figure_lable=tkinter.Label(BMI_input_frame,text=f"Your BMI:")
BMI_figure_lable.grid(row=4,column=0)

BMI_catogory_lable=tkinter.Label(BMI_input_frame,text=f"BMI Catogory:")
BMI_catogory_lable.grid(row=4,column=1)

BMI_piechart_frame=tkinter.LabelFrame(frame,text="BMI Piechart")
BMI_piechart_frame.grid(row=5,column=0)
piechart_button=tkinter.Button(frame,text='show piechart',command=drawpiechart)
piechart_button.grid(row=6,column=0)
#titlelabel=tkinter.Label(BMI_piechart_frame,text='piechart')
#titlelabel.grid(row=5,column=0)






window.mainloop()