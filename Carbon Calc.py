import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

colors = {
    'background': '#a3b899',
    'button_bg': '#82b8be',
    'button_fg': '#000000',
    'label_fg': '#2d3436',
    'frame_bg': '#f5f5f5',
    'slider_bg': '#4d5d53',
}

window = tk.Tk()
window.geometry("1497x944")
window.title("Carbon Footprint Calculator")
window.configure(bg=colors['background'])

user_inputs = {
    'hours_driving': tk.StringVar(),
    'public_transport_trips': tk.StringVar(),
    'car_type': tk.StringVar(value='None'),
    'domestic_flights': tk.StringVar(),
    'international_flights': tk.StringVar(),
    'meat_meals_per_week': tk.StringVar(),
    'new_devices_per_year': tk.StringVar(),
    'heating_cooling_source': tk.StringVar(value='None'),
    'clothing_purchase_frequency': tk.StringVar(),
    'recycling': tk.StringVar(value='No'),
    'energy_consciousness': tk.IntVar()
}

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(window, maximum=11, variable=progress_var)

questions = [
    "How many hours do you drive per day?",
    "Number of public transport trips per week:",
    "Number of domestic flights per year:",
    "Number of international flights per year:",
    "Number of meat meals per week:",
    "Number of new electronic devices purchased per year:",
    "Car type:",
    "Primary source of heating/cooling:",
    "How often do you purchase new clothing or household items?",
    "On a scale of 1-5, how conscious are you about energy usage?",
    "Do you actively recycle?"
]

widgets = [
    tk.Entry(window, textvariable=user_inputs['hours_driving']),
    tk.Entry(window, textvariable=user_inputs['public_transport_trips']),
    tk.Entry(window, textvariable=user_inputs['domestic_flights']),
    tk.Entry(window, textvariable=user_inputs['international_flights']),
    tk.Entry(window, textvariable=user_inputs['meat_meals_per_week']),
    tk.Entry(window, textvariable=user_inputs['new_devices_per_year']),
    ttk.Combobox(window, textvariable=user_inputs['car_type'], values=['Electric', 'Hybrid', 'Petrol/Diesel', 'None']),
    ttk.Combobox(window, textvariable=user_inputs['heating_cooling_source'], values=['Gas', 'Electric', 'Solar', 'None']),
    ttk.Combobox(window, textvariable=user_inputs['clothing_purchase_frequency'], values=['Rarely', 'Occasionally', 'Frequently']),
    ttk.Scale(window, from_=1, to=5, orient='horizontal', variable=user_inputs['energy_consciousness'], length=400),
    ttk.Combobox(window, textvariable=user_inputs['recycling'], values=['Yes', 'No', 'Sometimes'])
]

style = ttk.Style()
style.theme_use("clam")
style.configure("TScale", background=colors['background'], troughcolor=colors['frame_bg'], sliderthickness=20, sliderrelief='flat')

current_question = 0

slider_value_label = tk.Label(window, text="1", font=("Arial", 12), bg=colors['background'], fg=colors['label_fg'])

def update_slider_value(value):
    slider_value_label.config(text=f"Energy Consciousness: {int(float(value))}")

def show_intro_screen():
    for widget in window.winfo_children():
        widget.pack_forget()
    global intro_label, start_button
    intro_label = tk.Label(window, text="Welcome to the Carbon Footprint Calculator\nThere are 10 questions to answer.", font=("Impact", 30), bg=colors['background'], fg=colors['label_fg'], pady=20)
    start_button = tk.Button(window, text="Start", command=start_questionnaire, bg=colors['button_bg'], fg=colors['button_fg'], font=("Arial", 12, "bold"), padx=20, pady=10)
    intro_label.pack(pady=50)
    start_button.pack()

def start_questionnaire():
    intro_label.pack_forget()
    start_button.pack_forget()
    progress_bar.pack(pady=20, fill='x')
    show_question(0)
    next_button.pack(side='right', padx=20, pady=20)
    previous_button.pack(side='left', padx=20, pady=20)
    question_label.pack(pady=10)
    widget_frame.pack(pady=20)

def show_question(index):
    widget_frame.pack_forget()
    widgets[index].pack_forget()
    question_label.config(text=questions[index])
    progress_var.set(index + 1)
    widget_frame.pack(pady=20)
    widgets[index].pack(pady=20)
    if isinstance(widgets[index], ttk.Scale):
        slider_value_label.pack(pady=10)
        widgets[index].configure(command=update_slider_value)
    else:
        slider_value_label.pack_forget()

def next_question():
    global current_question
    widgets[current_question].pack_forget()
    slider_value_label.pack_forget()
    if current_question < len(questions) - 1:
        current_question += 1
        show_question(current_question)
    if current_question == len(questions) - 1:
        next_button.config(text="Calculate", command=calculate_emissions)

def previous_question():
    global current_question
    widgets[current_question].pack_forget()
    slider_value_label.pack_forget()
    if current_question > 0:
        current_question -= 1
        show_question(current_question)
    if current_question < len(questions) - 1:
        next_button.config(text="Next", command=next_question)

def calculate_emissions():
    try:
        driving_hours = float(user_inputs['hours_driving'].get()) * 12.5 * 365
        public_transport = int(user_inputs['public_transport_trips'].get()) * 0.6 * 52
        domestic_flights = int(user_inputs['domestic_flights'].get()) * 250
        international_flights = int(user_inputs['international_flights'].get()) * 500
        meat_consumption = int(user_inputs['meat_meals_per_week'].get()) * 5 * 52
        electronic_devices = int(user_inputs['new_devices_per_year'].get()) * 120
        car_emissions = {'Electric': 1800, 'Hybrid': 3000, 'Petrol/Diesel': 4600, 'None': 0}.get(user_inputs['car_type'].get(), 0)
        heating_cooling_emissions = 2800 if user_inputs['heating_cooling_source'].get() == 'Gas' else 4500 if user_inputs['heating_cooling_source'].get() == 'Electric' else 0
        clothing_emissions = {'Rarely': 90, 'Occasionally': 270, 'Frequently': 540}.get(user_inputs['clothing_purchase_frequency'].get(), 0)
        energy_reduction = 0.453 * user_inputs['energy_consciousness'].get() * 100
        recycling_reduction = 0.3 * (driving_hours + public_transport + domestic_flights + international_flights + meat_consumption + electronic_devices + car_emissions + heating_cooling_emissions + clothing_emissions) if user_inputs['recycling'].get() == 'Yes' else 0.15 * (driving_hours + public_transport + domestic_flights + international_flights + meat_consumption + electronic_devices + car_emissions + heating_cooling_emissions + clothing_emissions) if user_inputs['recycling'].get() == 'Sometimes' else 0
        total_emissions = (driving_hours + public_transport + domestic_flights + international_flights + meat_consumption + electronic_devices + car_emissions + heating_cooling_emissions + clothing_emissions) - energy_reduction - recycling_reduction
        display_results(total_emissions)
    except ValueError:
        result_label.config(text="Please enter valid numbers for all fields.")

def display_results(total_emissions):
    for widget in window.winfo_children():
        widget.pack_forget()
    window.geometry("1000x700")
    result_label.pack(pady=20)
    result_label.config(text=f"Your Total Carbon Footprint: {total_emissions:.2f} kg CO2/year", font=("Arial", 16), fg="white")
    categories = ['Driving', 'Public Transport', 'Flights', 'Meat Consumption', 'Electronics', 'Car', 'Heating/Cooling', 'Clothing']
    values = [
        float(user_inputs['hours_driving'].get()) * 12.5 * 365,
        int(user_inputs['public_transport_trips'].get()) * 0.6 * 52,
        int(user_inputs['domestic_flights'].get()) * 250 + int(user_inputs['international_flights'].get()) * 500,
        int(user_inputs['meat_meals_per_week'].get()) * 5 * 52,
        int(user_inputs['new_devices_per_year'].get()) * 120,
        {'Electric': 1800, 'Hybrid': 3000, 'Petrol/Diesel': 4600, 'None': 0}.get(user_inputs['car_type'].get(), 0),
        2800 if user_inputs['heating_cooling_source'].get() == 'Gas' else 4500 if user_inputs['heating_cooling_source'].get() == 'Electric' else 0,
        {'Rarely': 90, 'Occasionally': 270, 'Frequently': 540}.get(user_inputs['clothing_purchase_frequency'].get(), 0)
    ]
    fig, ax = plt.subplots(1, 2, figsize=(15, 7))
    ax[0].pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax[0].set_title("Carbon Footprint Breakdown", fontsize=18, pad=20)
    ax[1].bar(categories, values, color=plt.cm.Paired.colors)
    ax[1].set_title("Carbon Footprint by Category", fontsize=18, pad=20)
    ax[1].set_ylabel("kg CO2/year", fontsize=14)
    ax[1].tick_params(axis='x', rotation=45, labelsize=12)
    fig.tight_layout(pad=3.0)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

question_label = tk.Label(window, text="", font=("Arial", 14), bg=colors['background'], fg=colors['label_fg'])
question_label.pack(pady=10)

widget_frame = tk.Frame(window, bg=colors['frame_bg'])
widget_frame.pack(pady=20)

previous_button = ttk.Button(window, text="Previous", command=previous_question)
next_button = ttk.Button(window, text="Next", command=next_question)

result_label = tk.Label(window, text="", font=("Arial", 14), fg="green")

show_intro_screen()

window.mainloop()