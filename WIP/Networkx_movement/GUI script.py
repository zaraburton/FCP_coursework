# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:40:01 2021

@author: wills
"""

# import all methods and classes from the tkinter  
import tkinter as tk
import tkcalendar as tkcal
 
import Infection_rate_data as inf_rate


root = tk.Tk()
root.title('GUI')
root.geometry("600x400")


calendar = tkcal.Calendar(root, selectmode = "day", year = 2021, month = 4, day = 1)
calendar.place(x=10,y=10)


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
        
        month =int(selected_date[0] + selected_date[1] + selected_date[-2] + selected_date[-1])
    else:
        # ** Add error message here **
        pass

    # Saves and rounds output from infection_rate function to 2.d.p
    infection_val = round(inf_rate.infection_rate(month),2)
    
    # Slider set to output from infection_rate function
    infection_slider.set(infection_val)


date_button = tk.Button(root, text = "Select Date", command = grab_date)
date_button.place(x=95,y=200)
date_label = tk.Label(root, text = "")
date_label.place(x=65,y=225)


infection_slider = tk.Scale(root, from_=0, to=1,digits = 3, resolution = 0.01,length = 200, orient=tk.HORIZONTAL)
infection_slider.place(x=35,y=250)
infection_label = tk.Label(root, text = "Infection rate")
infection_label.place(x=95,y=290)

var_mask = tk.IntVar()
var_oneway = tk.IntVar()
tick_box_1 = tk.Checkbutton(root, text='Masks worn', variable=var_mask, onvalue=1, offvalue=0)
tick_box_1.place(x=40,y=320)
tick_box_2 = tk.Checkbutton(root, text='One way system', variable=var_oneway, onvalue=1, offvalue=0)
tick_box_2.place(x=40,y=360)





root.mainloop()