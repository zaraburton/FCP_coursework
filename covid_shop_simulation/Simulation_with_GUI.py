# -*- coding: utf-8 -*-
"""
Created on Mon May 17 10:40:01 2021

@author: wills
"""

# import all relevent packages and other python scripts
import tkinter as tk
import tkcalendar as tkcal
import random
import Infection_rate_data as inf_rate
import Initial_Simulation_test as init_sim



# Setup GUI window
root = tk.Tk()
root.title('GUI')
root.geometry("1200x690")
root.configure(bg='Grey30')


# Setup coloured frames to partition GUI
frame_1 = tk.Frame(root, width = 270, height = 260, bg = "cornflower blue")
frame_1.place(x=10,y=10)

frame_2 = tk.Frame(root, width = 270, height = 400, bg = "SeaGreen2")
frame_2.place(x=10,y=280)

frame_3 = tk.Frame(root, width = 130, height = 130, bg = "MediumPurple2")
frame_3.place(x=290,y=280)

frame_4= tk.Frame(root, width = 760, height = 670, bg = "Orange2")
frame_4.place(x=430,y=10)


#Add tkcalendar to GUI
calendar = tkcal.Calendar(root, selectmode = "day",date_pattern = 'mm/dd/yy')
calendar.place(x=20,y=20)



# Function to take selected date from calendar
def grab_date():
    
    # Prints selected date below calendar
    selected_date = calendar.get_date()
    date_label.config(text = "Date selected is " + selected_date)
    
    # Saving selected date as month-year number (e.g. 0221 = Feb 2021)
    # this is the same format as the infection rate data function
    month = (selected_date[0]+selected_date[1]+selected_date[-2]+selected_date[-1])
    
    # month saved as integer to remove all leading zeros
    month = int(month)
    
    # month saved as string again to allow for specific characters of the integer to be referenced
    month = str(month)
  
 

   
    # The following section outlines error messages for when dates are selected where data is not available
    # We only want dates between March 2020 (320) and February 2021 (221) 
    
    # If 2nd to last digit is not two then a wrong date must have been inputted
    if int(month[-2]) != 2:
        tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
        root.destroy()
    # If last digit of month is greater than 1 then a wrong date must have been inputted
    elif int(month[-1]) > 1:
        tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
        root.destroy()
    # If last digit of month is a 1 and is the first digit is greater than 2 then wrong date inputted
    elif int(month[-1]) == 1 and int(month[0]) > 2:
         tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
         root.destroy()
    # If the length of month is 4 digits and the last digit is a 1 then a wrong date has been inputted
    elif len(month) == 4 and int(month[-1]) == 1:
         tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
         root.destroy()
    # If the last digit of month is a 0 and the first digit is less than 3 then wrong date inputted
    elif int(month[-1]) == 0 and int(month[0]) < 3 and len(month) == 3:
         tk.messagebox.showerror(title="Error",message="Please select a date between 1st March 2020 and 28th February 2021")
         root.destroy()
             
    # Convert month back to integer so it can be input into infection_val calculator     
    month = int(month)
        
    # Saves and rounds output from infection_rate function to 2.d.p
    infection_val = round(inf_rate.infection_rate(month),2)
    
    # Slider set to output from infection_rate function
    infection_slider.set(infection_val)

    # Return month variable as a tuple with an arbitrary number as the 1st character
    # This allows the month variable to be used in other functions without defining it as a global variable
    return (1,month)

# Creating button to allow users to select a date
date_button = tk.Button(root, text = "Select Date", command = grab_date)
date_button.place(x=95,y=215)
date_label = tk.Label(root, text = "                                       ")
date_label.place(x=65,y=245)

# Creating slider to allow user to input infection rate
infection_slider = tk.Scale(root, from_=0, to=1,digits = 3, resolution = 0.01,length = 200, orient=tk.HORIZONTAL)
infection_slider.place(x=35,y=290)
infection_label = tk.Label(root, text = "Infection rate")
infection_label.place(x=95,y=330)

    
# Create tick boxes for wearing of masks or one way system
var_mask = tk.IntVar()
var_oneway = tk.IntVar()
tick_box_1 = tk.Checkbutton(root, text='Masks worn', variable=var_mask, onvalue=1, offvalue=0)
tick_box_1.place(x=40,y=610)
tick_box_2 = tk.Checkbutton(root, text='One way system', variable=var_oneway, onvalue=1, offvalue=0)
tick_box_2.place(x=40,y=640)

# Create slider to allow user to input the max number of people who can enter at a time
num_people_enter_slider = tk.Scale(root, from_=1, to=5, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
num_people_enter_slider.place(x=35,y=370)
num_people_enter_label = tk.Label(root, text = "Max number of people who can enter at a time")
num_people_enter_label.place(x=10, y=410)
num_people_enter_slider.set(random.randint(1,5))

# Create slider to allow user to input number of time steps to run simulation for
time_slider = tk.Scale(root, from_=1, to=500, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
time_slider.place(x=35, y=450)
time_label = tk.Label(root, text = "Number of time steps to run simulation for")
time_label.place(x=20, y=490)
time_slider.set(random.randint(1,500))

# Create slider to allow user to input the maximum number of people allowed in the shop
max_people_slider = tk.Scale(root, from_=1, to=30, digits = 1, resolution = 1, length = 200, orient=tk.HORIZONTAL)
max_people_slider.place(x=35, y=530)
max_people_label = tk.Label(root, text = "Max number of people in shop")
max_people_label.place(x=50, y=570)
max_people_slider.set(random.randint(1,30))


# Defining function to take all GUI inputs and use them to run the simulation code
def search_function():
    num_people_enter_val = int(num_people_enter_slider.get())
    time_val = int(time_slider.get())
    max_people_val = int(max_people_slider.get())
    
    # Way of using local variable from other function
    month = grab_date()[1]
    
    # If oneway button selected then assign variable with a 2
    if var_oneway == True:
        path_type = 2
    else:
        path_type = 1
        
    #Runs GUI specific function from the simulation script which runs the simulation using GUI inputs
    
    init_sim.GUI_run(num_people_enter_val, time_val, max_people_val, month, path_type)


# Create button to save all current GUI inputs and use them in simulation
search_button = tk.Button(root, text = "Enter Inputs", command = search_function, height = 7, width = 14)
search_button.place(x=300,y=290)

root.mainloop()