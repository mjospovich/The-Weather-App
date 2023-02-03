from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, timezone

import requests


#*app class
class App(tk.Tk):
  WIDTH = 500
  HEIGHT = 600

  def __init__(self):
    super().__init__()

    #*set class variables
    self.city = "Split" #set default city
    self.weather = "Clear_day" #needs to be one of the available keys
    self.weather_image = None
    self.temp = 0
    self.wind_speed = 0
    self.pressure = 0
    self.humidity = 0
    self.local_time = datetime.now().strftime("%H:%M")

    #*load all weather images
    self.weather_images = {}
    self.weather_images["Clear_day"] = PhotoImage(file=r"images\sunny.png")
    self.weather_images["Clear_night"] = PhotoImage(file=r"images\clear_night.png")
    self.weather_images["Rain"] = PhotoImage(file=r"images\rain.png")
    self.weather_images["Cloudy"] = PhotoImage(file=r"images\cloudy.png")
    self.weather_images["Partly_cloudy"] = PhotoImage(file=r"images\partly_cloudy.png")
    self.weather_images["Snow"] = PhotoImage(file=r"images\snow.png")
    self.weather_images["Thunderstorm"] = PhotoImage(file=r"images\stormy.png")
    self.weather_images["Light_rain"] = PhotoImage(file=r"images\light_rain.png")
    self.weather_images["Heavy_rain"] = PhotoImage(file=r"images\heavy_rain.png")
    self.weather_images["Windy"] = PhotoImage(file=r"images\windy.png")

    #*load all wind images
    self.wind_images = {}
    self.wind_images["Wind_low"] = PhotoImage(file=r"images\wind_low.png")
    self.wind_images["Wind_medium"] = PhotoImage(file=r"images\wind_med.png")
    self.wind_images["Wind_strong"] = PhotoImage(file=r"images\wind_strong.png")
    self.wind_images["Wind_extreme"] = PhotoImage(file=r"images\wind_extreme.png")

    #*set window title and icon
    self.title("The Weather App")
    self.iconbitmap(r"images\weather_app.ico")

    #*set window size
    self.geometry(f"{App.WIDTH}x{App.HEIGHT+30}")
    self.resizable(False, False)

    #*frame
    self.frame = Frame(self)
    self.frame.pack()

    #*canvas
    self.canvas = Canvas(self.frame, width=App.WIDTH, height=App.HEIGHT, bg="#e6e6e6")
    self.canvas.pack()

    #*title image
    self.title_img = PhotoImage(file=r"images\title_text.png")
    self.canvas.create_image(App.WIDTH/2, App.HEIGHT/10, image=self.title_img)


    #*search box
    self.search_img = PhotoImage(file=r"images\search_box2.png")
    self.canvas.create_image(App.WIDTH/2, App.HEIGHT/4-25, image=self.search_img)


    #*search entry
    self.search_entry = Entry(self.frame, font=("Arial", 16, "normal"),
                              width=18, borderwidth=0, bg="#e6e6e6",
                              fg="black", highlightthickness=0)
    self.search_entry.insert(0, "Enter a city:")

    self.search_entry.bind("<Button-1>", lambda event: self.search_entry.delete(0, END))
    self.search_entry.bind("<Return>", lambda event: self.get_city())
    
    self.search_entry.place(x=App.WIDTH/2-130, y=App.HEIGHT/4-38)

    #*search button
    self.search_button_img = PhotoImage(file=r"images\search_button.png")
    self.search_button = Button(self.frame, image=self.search_button_img, borderwidth=0,
                                highlightthickness=0, command=self.get_city)
    self.search_button.place(x=App.WIDTH/2+110, y=App.HEIGHT/4-40)

    #*city label
    self.city_label = Label(self.frame, text=self.city, font=("Arial", 20, "normal"),
                            fg="black", bg="#e6e6e6", borderwidth=0, width=20)
    self.city_label.place(x=App.WIDTH/2-160, y=App.HEIGHT/3-28)


    #*blue line frame image
    self.blue_frame_img = PhotoImage(file=r"images\blue_frame.png")
    self.canvas.create_image(App.WIDTH/2, App.HEIGHT/1.62, image=self.blue_frame_img)
    
    #*weather image
    self.weather_img = self.weather_images[self.weather]
    self.weather_canv = self.canvas.create_image(App.WIDTH/2, App.HEIGHT/2.20, image=self.weather_img)

    #*temperature label
    self.temp_label = Label(self.frame, text=f"{self.temp}°C", font=("Arial", 32, "bold"),
                            fg="#2e74b7", bg="#e6e6e6", borderwidth=0, width=4)
    self.temp_label.place(x=App.WIDTH/2-55, y=App.HEIGHT/1.74)

    #*weather label
    self.weather_display = self.weather.replace("_", " ")
    self.weather_display = self.weather_display.title()

    self.weather_label = Label(self.frame, text=self.weather_display,
                               font=("Arial", 26, "bold"),
                               fg="#2e74b7", bg="#e6e6e6", borderwidth=0)

    self.weather_label.place(x=App.WIDTH/2-120, y=App.HEIGHT/1.50, width=240)

    #*wind label
    self.wind_label = Label(self.frame, text="Wind", font=("Arial", 18, "normal"),
                            fg="black", bg="#e6e6e6", borderwidth=0, width=4)
    self.wind_label.place(x=App.WIDTH-282, y=App.HEIGHT/1.32)

    #*wind image
    self.set_wind_image()
    self.wind_img = self.wind_images[self.wind]
    self.wind_canv = self.canvas.create_image(App.WIDTH-254, App.HEIGHT/1.17, image=self.wind_img)

    #*wind speed label
    self.wind_speed_kph = self.wind_speed*3.6
    self.wind_speed_kph = round(self.wind_speed_kph, 0)

    self.wind_speed_label = Label(self.frame, text=f"{self.wind_speed_kph} km/h",
                                  font=("Arial", 16, "normal"), fg="black", bg="#e6e6e6",
                                  borderwidth=0, width=9)
    self.wind_speed_label.place(x=App.WIDTH-301, y=App.HEIGHT/1.11)

    #*humidity label
    self.humidity_label = Label(self.frame, text="Humidity", font=("Arial", 18, "normal"),
                                fg="black", bg="#e6e6e6", borderwidth=0, width=8)
    self.humidity_label.place(x=App.WIDTH-450, y=App.HEIGHT/1.32)
    #self.humidity_label.place(x=App.WIDTH/3 + 22, y=App.HEIGHT/1.32)

    #*humidity image
    self.humidity_img = PhotoImage(file=r"images\humidity.png")
    self.canvas.create_image(App.WIDTH-390, App.HEIGHT/1.17, image=self.humidity_img)
    #self.canvas.create_image(App.WIDTH/3 + 82, App.HEIGHT/1.17, image=self.humidity_img)

    #*humidity percentage label
    self.humidity_percentage_label = Label(self.frame, text=f"{self.humidity}%",
                                          font=("Arial", 16, "normal"), fg="black",
                                          bg="#e6e6e6", borderwidth=0, width=4)
    self.humidity_percentage_label.place(x=App.WIDTH-416, y=App.HEIGHT/1.11)
    #self.humidity_percentage_label.place(x=App.WIDTH/3 + 60, y=App.HEIGHT/1.11)

    #*pressure label
    self.pressure_label = Label(self.frame, text="Pressure", font=("Arial", 18, "normal"),
                                fg="black", bg="#e6e6e6", borderwidth=0, width=8)
    self.pressure_label.place(x=App.WIDTH-168, y=App.HEIGHT/1.32)

    #*pressure image
    self.pressure_img = PhotoImage(file=r"images\pressure.png")
    self.canvas.create_image(App.WIDTH-112, App.HEIGHT/1.17, image=self.pressure_img)

    #*pressure level label
    self.pressure_level_label = Label(self.frame, text=f"{self.pressure} hPa",
                                      font=("Arial", 16, "normal"), fg="black", 
                                      bg="#e6e6e6", borderwidth=0, width=8)
    self.pressure_level_label.place(x=App.WIDTH-163, y=App.HEIGHT/1.11)

    #*local time label
    self.local_time_label = Label(self.frame, text=f"Local time: {self.local_time}",
                                  font=("Arial", 11, "normal"), fg="black", bg="#e6e6e6",
                                  borderwidth=0, width=20, height=1, anchor="center")
    self.local_time_label.place(x=App.WIDTH/2-87, y=App.HEIGHT/1.03)

    #*menu bar
    self.menu_bar = Menu(self)
    self.config(menu=self.menu_bar)

    #*app menu
    self.app_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="App", menu=self.app_menu)
    self.app_menu.add_command(label="Credits", command=self.credits)
    self.app_menu.add_command(label="Exit", command=self.destroy)

    #*save menu
    self.save_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label="Save", menu=self.save_menu)
    self.save_menu.add_command(label="Save to txt", command=self.save_to_txt)



  #!methods-----------------------
  #*saves json data to txt file
  def save_to_txt(self):
    displayed_time = self.local_time.replace(":", "_")
    file_name = f"saved\{self.city}_{displayed_time}.txt"

    with open(f"{file_name}", "w") as file:
      file.write(f"City: {self.city}\n")
      file.write(f"Weather: {self.weather}\n")
      file.write(f"Temperature: {self.temp} °C\n")
      file.write(f"Wind speed: {self.wind_speed_kph} km/h\n")
      file.write(f"Humidity: {self.humidity}%\n")
      file.write(f"Pressure: {self.pressure} hPa\n")
      file.write(f"Local time: {self.local_time}\n")
      
  #*prints credits for images
  def credits(self):
    messagebox.showinfo("Credits", "Icons from Icons8: https://icons8.com/icons/set/weather")
    #print("Icons from Icons8: https://icons8.com/icons/set/weather")

  #*gets city from search entry   
  def get_city(self):
    city = self.search_entry.get()
    
    if city == "":
      messagebox.showerror("Error", "Please enter a city!")
    
    elif city == "Enter a city:":
      messagebox.showerror("Error", "Please enter a city!")

    elif city == self.city:
      pass 

    else:
      self.city = city
      #self.display_city()
      self.get_weather()
      return city

  #*display city name
  def display_city(self):
    self.city_label.configure(text=self.city)

  #*choose wind image based on wind speed
  def set_wind_image(self):
    if self.wind_speed < 7:
      self.wind = "Wind_low"
    elif self.wind_speed < 16:
      self.wind = "Wind_medium"
    elif self.wind_speed < 28:
      self.wind = "Wind_strong"
    else:
      self.wind = "Wind_extreme"

  #*gets weather data from api
  def get_weather(self):
    api_key = "" #!IMPORTANT: paste your API key (get it from openweather)
    api = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}"

    try:
      json_data = requests.get(api).json()
      #print(json_data.keys())
      condition = json_data["weather"][0]["main"]

      #*set local time
      local_time_offset = json_data["timezone"]
      self.grinich_time = datetime.now(timezone.utc)
      self.local_time = self.grinich_time + timedelta(seconds=local_time_offset)
      self.local_time = self.local_time.strftime("%H:%M")
      #print(self.local_time)

      #*set weather condition
      self.temp = int(json_data["main"]["temp"] - 273.15)
      self.pressure = json_data["main"]["pressure"]
      self.humidity = json_data["main"]["humidity"]
      self.wind_speed = json_data["wind"]["speed"]
      self.wind_speed_kph = self.wind_speed*3.6
      self.wind_speed_kph = round(self.wind_speed_kph, 0)
      self.weather = condition
      self.city = json_data["name"]

      #*set weather condition
      if condition == "Clear":
        self.weather = "Clear_day"
        if (self.local_time < "06:00" or self.local_time > "18:00"):
          self.weather = "Clear_night"
        if(self.wind_speed_kph > 50):
          self.weather = "Windy"
      elif condition == "Clouds" or condition == "Mist" or condition == "Fog" or condition == "Haze":
        self.weather = "Cloudy"
        if (json_data["clouds"]["all"] < 65):
          self.weather = "Partly_cloudy"
      elif condition == "Rain":
        self.weather = "Rain"
        if (json_data["rain"]["1h"] < 3 and json_data["rain"]["1h"] > 0):
          self.weather = "Light_rain"
        elif (json_data["rain"]["1h"] < 9 and json_data["rain"]["1h"] > 3):
          self.weather = "Rain"
        elif (json_data["rain"]["1h"] > 9):
          self.weather = "Heavy_rain"
      elif condition == "Snow":
        self.weather = "Snow"
      elif condition == "Thunderstorm":
        self.weather = "Thunderstorm"
      else:
        print(self.weather)
        pass  

      #for wind
      self.set_wind_image()


      #*update labels
      self.temp_label.configure(text=f"{self.temp}°C")
      self.wind_speed_label.configure(text=f"{self.wind_speed_kph} km/h")
      self.humidity_percentage_label.configure(text=f"{self.humidity}%")
      self.pressure_level_label.configure(text=f"{self.pressure} hPa")
      self.weather_display = self.weather.replace("_", " ")
      self.weather_display = self.weather_display.title()
      self.weather_label.configure(text=self.weather_display)
      self.city_label.configure(text=self.city)
      self.local_time_label.configure(text=f"Local time: {self.local_time}")


      #*update canvas images
      self.canvas.itemconfig(self.weather_canv, image=self.weather_images[self.weather])
      self.canvas.itemconfig(self.wind_canv, image=self.wind_images[self.wind])

    except Exception as e:
      messagebox.showerror("The Weather App", "Please enter a valid city or check your internet connection!")


  

if __name__ == "__main__":
  app = App()
  app.get_weather()
  app.mainloop()

