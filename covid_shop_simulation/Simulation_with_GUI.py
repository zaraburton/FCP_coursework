# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:40:01 2021

@author: wills
"""

# import all methods and classes from the tkinter  
import tkinter as tk
import tkcalendar as tkcal
import random
import Infection_rate_data as inf_rate


root = tk.Tk()
root.title('GUI')
root.geometry("1200x690")
root.configure(bg='Grey30')

frame_1 = tk.Frame(root, width = 270, height = 260, bg = "cornflower blue")
frame_1.place(x=10,y=10)

frame_2 = tk.Frame(root, width = 270, height = 400, bg = "SeaGreen2")
frame_2.place(x=10,y=280)

frame_3 = tk.Frame(root, width = 130, height = 130, bg = "MediumPurple2")
frame_3.place(x=290,y=280)

frame_4= tk.Frame(root, width = 760, height = 670, bg = "Orange2")
frame_4.place(x=430,y=10)


calendar = tkcal.Calendar(root, selectmode = "day", year = 2021, month = 1, day = 1)
calendar.place(x=20,y=20)



# Function to take selected date from calendar
def grab_date():
    
    # Present selected date below calendar
    selected_date = calendar.get_date()
    date_label.config(text = "Date selected is " + selected_date)
    
    # Saving selected date as month-year number (e.g. 221 = Feb 2021)
    # this is the same format as the infection rate data function
    
    # If selected_date is 7 characters long then format of month variable is myy
    # If selected_date is 8 characters long then format of month variable is mmyy
    if len(selected_date) == 7:
        
        month = int(selected_date[0] + selected_date[-2] + selected_date[-1])
    elif len(selected_date) == 8:
        
        month = int(selected_date[0] + selected_date[1] + selected_date[-2] + selected_date[-1])
    else:
        #tk.messagebox.showerror(title="error",message="Please select a date between 1st March 2020 and 28th February 2021")
        pass
    print(month)
    # We only want dates between March 2020 (320) and February 2021 (221)
    # Acceptable values:
        #320
        #420
        #520
        #620
        #720
        #820
        #920
        #1020
        #1120
        #1220
        #121
        #221
    # If 2nd to last digit is not two then a wrong date must have been inputted
    if month[-2] != 2:
        tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
    # If last digit of month is greater than 1 then a wrong date must have been inputted
    if month[-1] > 1:
        tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
    # If last digit of month is a 1 and is the first digit is greater than 2 then wrong date inputted
    if month[-1] == 1 and month[1] > 2:
         tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
    # If the length of month is 4 digits and the last digit is a 1 then a wrong date has been inputted
    if len(month) == 4 and month[-1] == 1:
         tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
    
        
    # Saves and rounds output from infection_rate function to 2.d.p
    infection_val = round(inf_rate.infection_rate(month),2)
    
    # Slider set to output from infection_rate function
    infection_slider.set(infection_val)


date_button = tk.Button(root, text = "Select Date", command = grab_date)
date_button.place(x=95,y=215)
date_label = tk.Label(root, text = "                                       ")
date_label.place(x=65,y=245)


infection_slider = tk.Scale(root, from_=0, to=1,digits = 3, resolution = 0.01,length = 200, orient=tk.HORIZONTAL)
infection_slider.place(x=35,y=290)
infection_label = tk.Label(root, text = "Infection rate")
infection_label.place(x=95,y=330)

    

var_mask = tk.IntVar()
var_oneway = tk.IntVar()
tick_box_1 = tk.Checkbutton(root, text='Masks worn', variable=var_mask, onvalue=1, offvalue=0)
tick_box_1.place(x=40,y=610)
tick_box_2 = tk.Checkbutton(root, text='One way system', variable=var_oneway, onvalue=1, offvalue=0)
tick_box_2.place(x=40,y=640)

num_people_enter_slider = tk.Scale(root, from_=1, to=5, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
num_people_enter_slider.place(x=35,y=370)
num_people_enter_label = tk.Label(root, text = "Max number of people who can enter at a time")
num_people_enter_label.place(x=10, y=410)
num_people_enter_slider.set(random.randint(1,5))

time_slider = tk.Scale(root, from_=1, to=500, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
time_slider.place(x=35, y=450)
time_label = tk.Label(root, text = "Number of time steps to run simulation for")
time_label.place(x=20, y=490)
time_slider.set(random.randint(1,500))

max_people_slider = tk.Scale(root, from_=1, to=30, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
max_people_slider.place(x=35, y=530)
max_people_label = tk.Label(root, text = "Max number of people in shop")
max_people_label.place(x=50, y=570)
max_people_slider.set(random.randint(1,30))



def search_function():
    infect_val = infection_slider.get()
    num_people_enter_val = num_people_enter_slider.get()
    time_val = time_slider.get()
    max_people_val = max_people_slider.get()

search_button = tk.Button(root, text = "Enter Inputs", command = search_function, height = 7, width = 14)
search_button.place(x=300,y=290)

    
    



root.mainloop()