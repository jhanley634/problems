#! /usr/bin/env python
# Copyright 2023 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/285103/world-weather-application-in-python-using-tkinter
from datetime import datetime
import geocoder
from tkinter import *
import tkinter as tk
import requests
import calendar
from weather_icons import icons_day, icons_mini


def world_weather():

    # Create the window and set the basics
    root = Tk()
    root.title('World Weather by paichiwo')
    root.geometry('350x680+300+200')
    root.resizable(False, False)
    root.config(bg='black')

    # Colors
    l_blue = '#1581ef'
    d_blue = '#1167f2'

    # https://weatherbit.io/ API KEY
    api_key = ''

    def format_date_long(date):
        """ Format date to weekday, day month_name (Monday, 14 May) """
        date_object = datetime.strptime(date, '%Y-%m-%d')
        week_day = calendar.day_name[date_object.weekday()]
        month = date_object.month
        month_name = calendar.month_name[month]
        return f'{week_day[:3]}, {date_object.day} {month_name}'

    def format_date_short(date):
        """ Format date to day month_name (14 May) """
        date_object = datetime.strptime(date, '%Y-%m-%d')
        month = date_object.month
        month_name = calendar.month_name[month]
        return f'{date_object.day} {month_name[:3]}'

    def mtr_sec_to_km_per_hour(ms):
        """ Convert units - m/s to km/h """
        return ms * (1 / 1000) / (1 / 3600)

    def get_user_location():
        ip_location = geocoder.ip('me')
        city = ip_location.city
        country = ip_location.country
        return f"{city}, {country}"

    def get_current_weather(api_key, location):
        try:
            url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={api_key}'
            current_data = requests.get(url).json()
        except requests.exceptions.JSONDecodeError:
            url = f'https://api.weatherbit.io/v2.0/current?postal_code={location}&key={api_key}'
            current_data = requests.get(url).json()
        return current_data

    def get_forecast_weather(api_key, location):
        try:
            f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={location}&key={api_key}&days=4'
            forecast_data = requests.get(f_url).json()
        except requests.exceptions.JSONDecodeError:
            f_url = f'https://api.weatherbit.io/v2.0/forecast/daily?postal_code={location}&key={api_key}&days=4'
            forecast_data = requests.get(f_url).json()
        return forecast_data

    def update_current_weather_main_window(current_data):

        # Main window data
        city = current_data['data'][0]['city_name']
        country = current_data['data'][0]['country_code']
        code = current_data['data'][0]['weather']['code']
        current_temp = str(int(current_data['data'][0]['temp']))
        current_condition = current_data['data'][0]['weather']['description']
        local_time = format_date_long(current_data['data'][0]['datetime'][:-3])
        current_day_or_night = current_data['data'][0]['pod']

        # Update the labels
        city_info.config(text=f'{city}, {country}', fg='white', font=('Noto Sans', 12), justify='center', width=22)
        city_info.place(x=65, y=97)

        if current_day_or_night == 'd':
            weather_icon.config(file=icons_day[code])
            weather_label.place(x=97, y=130)
        else:
            weather_icon.config(file=icons_day[code])  # to update when night icons are made
            weather_label.place(x=97, y=130)

        temp.config(text=current_temp, justify='center', width=2)

        if len(current_temp) == 1:
            temp_symbol.config(text='°', justify='center')
            temp_symbol.place(x=205, y=290)
        else:
            temp_symbol.config(text='°', justify='center')
            temp_symbol.place(x=238, y=290)

        condition.config(text=current_condition, justify='center')
        date_info.config(text=local_time, justify='center')

    def update_current_weather_bottom_row(current_data):

        # Bottom row data
        current_feelslike = str(int(current_data['data'][0]['app_temp']))
        current_wind_speed = str(int(mtr_sec_to_km_per_hour(current_data['data'][0]['wind_spd'])))
        current_humidity = current_data['data'][0]['rh']
        current_cloud_coverage = str(int(current_data['data'][0]['clouds']))
        current_pressure = str(int(current_data['data'][0]['slp']))

        # Update the labels
        feelslike.config(text=f'{current_feelslike}°', justify='center')
        wind.config(text=f'{current_wind_speed} km/h', justify='center')
        humidity.config(text=f'{current_humidity}%', justify='center')
        cloud_coverage.config(text=f'{current_cloud_coverage}%', justify='center')  # change graphics !!!!!!
        pressure.config(text=f'{current_pressure} hPa', justify='center')
        textfield.delete(0, END)

    def create_forecast_data_list(forecast_data):

        forecast_data_list = []

        for forecast_days in forecast_data['data'][1:]:
            forecast_date = format_date_short(forecast_days['datetime'])
            forecast_avg_temp = str(int(forecast_days['temp']))
            forecast_avg_humidity = str(int(forecast_days['rh']))
            forecast_max_wind = str(int(mtr_sec_to_km_per_hour(forecast_days['wind_spd'])))
            forecast_code = forecast_days['weather']['code']

            forecast_data_list.append([forecast_date,
                                       forecast_avg_temp,
                                       forecast_avg_humidity,
                                       forecast_max_wind,
                                       forecast_code])
        return forecast_data_list

    def update_forecast_window(forecast_data_list):

        day_1_date.config(text=forecast_data_list[0][0], justify='center')
        day_1_temp.config(text=f'{forecast_data_list[0][1]}°', justify='center')
        day_1_humidity.config(text=f'{forecast_data_list[0][2]}%', justify='center')
        day_1_wind.config(text=f'{forecast_data_list[0][3]} km/h', justify='center')
        day_1_icon.config(file=icons_mini[forecast_data_list[0][4]])

        day_2_date.config(text=forecast_data_list[1][0], justify='center')
        day_2_temp.config(text=f'{forecast_data_list[1][1]}°', justify='center')
        day_2_humidity.config(text=f'{forecast_data_list[1][2]}%', justify='center')
        day_2_wind.config(text=f'{forecast_data_list[1][3]} km/h', justify='center')
        day_2_icon.config(file=icons_mini[forecast_data_list[1][4]])

        day_3_date.config(text=forecast_data_list[2][0], justify='center')
        day_3_temp.config(text=f'{forecast_data_list[2][1]}°', justify='center')
        day_3_humidity.config(text=f'{forecast_data_list[2][2]}%', justify='center')
        day_3_wind.config(text=f'{forecast_data_list[2][3]} km/h', justify='center')
        day_3_icon.config(file=icons_mini[forecast_data_list[2][4]])

    def get_weather():
        """ Connect to API, get data and update tkinter labels """

        if len(textfield.get()) > 0:
            location = textfield.get()
        else:
            location = get_user_location()

        try:
            current_data = get_current_weather(api_key, location)
            forecast_data = get_forecast_weather(api_key, location)
            forecast_list = create_forecast_data_list(forecast_data)
            update_current_weather_main_window(current_data)
            update_current_weather_bottom_row(current_data)
            update_forecast_window(forecast_list)
        except KeyError:
            city_info.config(text='Enter correct location', fg='yellow', justify='center', width=22)
        except requests.exceptions.ConnectionError:
            get_weather()

    # Create Search box
    search_image = PhotoImage(file='img/current_window.png')
    search_label = Label(image=search_image, bg='black')
    search_label.place(x=22, y=20)
    textfield = tk.Entry(root, cursor='hand2', justify='center', width=23, font=('Noto Sans', 11, 'bold'),
                         bg=d_blue, border=0, fg='white')
    textfield.place(x=60, y=67, height=25)
    textfield.focus()
    textfield.bind('<Return>', lambda event=None: search_button.invoke())
    search_icon = PhotoImage(file='img/magnifying_glass.png')
    search_button = Button(image=search_icon, activebackground=l_blue, borderwidth=0,
                           bg=d_blue, command=get_weather)
    search_button.place(x=268, y=65)

    # Create Current Weather labels

    city_info = Label(text='Enter city name or postcode', font=('Noto Sans', 10), bg=l_blue, fg='white')
    city_info.place(x=90, y=97)
    weather_icon = PhotoImage(file='img/splash_icon.png')
    weather_label = Label(root, image=weather_icon, bg=l_blue)
    weather_label.place(x=105, y=157)
    temp = Label(text='', font=('Noto Sans', 85, 'bold'), bg=l_blue, fg='white')
    temp.place(x=104, y=280, height=111)
    temp_symbol = Label(text='', font=('Noto Sans', 20, 'bold'), height=1, bg=l_blue, fg='white')
    temp_symbol.place(x=206, y=290, width=15)
    condition = Label(text='', font=('Noto Sans', 11), bg=l_blue, fg='white', width=27)
    condition.place(x=53, y=390, height=30)
    date_info = Label(text='', font=('Noto Sans', 8), bg=l_blue, fg='white', width=30)
    date_info.place(x=69, y=418, height=15)

    feelslike = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=3)
    feelslike.place(x=63, y=487, height=15)
    wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
    wind.place(x=100, y=487, height=15)
    humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=4)
    humidity.place(x=163, y=487, height=15)
    cloud_coverage = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=5)
    cloud_coverage.place(x=206, y=487, height=15)
    pressure = Label(text='', font=('Noto Sans', 8, 'bold'), bg=l_blue, fg='white', width=7)
    pressure.place(x=249, y=487, height=15)

    # Create Forecast Weather labels
    day_1_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
    day_1_date.place(x=32, y=535, height=20)
    day_1_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_1_temp.place(x=37, y=555, height=20)
    day_1_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_1_humidity.place(x=37, y=575, height=20)
    day_1_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_1_wind.place(x=37, y=595, height=20)
    day_1_icon = PhotoImage(file='img/dummy_mini.png')
    day_1_icon_label = Label(root, image=day_1_icon, bg='black')
    day_1_icon_label.place(x=53, y=618)

    day_2_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
    day_2_date.place(x=135, y=535, height=20)
    day_2_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_2_temp.place(x=140, y=555, height=20)
    day_2_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_2_humidity.place(x=140, y=575, height=20)
    day_2_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_2_wind.place(x=140, y=595, height=20)
    day_2_icon = PhotoImage(file='img/dummy_mini.png')
    day_2_icon_label = Label(root, image=day_2_icon, bg='black')
    day_2_icon_label.place(x=156, y=618)

    day_3_date = Label(text='', font=('Noto Sans', 9, 'bold'), bg='black', fg='white', width=10)
    day_3_date.place(x=234, y=535, height=20)
    day_3_temp = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_3_temp.place(x=239, y=555, height=20)
    day_3_humidity = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_3_humidity.place(x=239, y=575, height=20)
    day_3_wind = Label(text='', font=('Noto Sans', 8, 'bold'), bg='black', fg='white', width=10)
    day_3_wind.place(x=239, y=595, height=20)
    day_3_icon = PhotoImage(file='img/dummy_mini.png')
    day_3_icon_label = Label(root, image=day_3_icon, bg='black')
    day_3_icon_label.place(x=255, y=618)

    root.mainloop()


if __name__ == '__main__':
    world_weather()
