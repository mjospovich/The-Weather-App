![](https://img.shields.io/github/license/mjospovich/The-Weather-App)
![](https://img.shields.io/github/languages/code-size/mjospovich/The-Weather-App?color=blue)
![](https://img.shields.io/badge/language%20-Python-yellow.svg)
![](https://img.shields.io/badge/api%20-OpenWeatherMap-red.svg)

# The Weather App
### **Description:**
 - Python weather app project for OOP.
 - The app uses the OpenWeatherMap API to get the weather data.
 - The app uses the Tkinter library to create the GUI.
 - The app can save the weather data in a text file.
 - Icons are from: https://icons8.com/icons/set/weather
----------------------------------------------

## Preview (GUI and save format):
<p allign = "center">
<img src="preview\gui.PNG" alt="gui" width="350" />
<img src="preview\save_format.PNG" alt="gui" width="210" height="400"/>
</p>

----------------------------------------------

## Notes:
- Project supports [Better Comments](https://marketplace.visualstudio.com/items?itemName=aaron-bond.better-comments) extension for VS Code.
- Needs an API key from OpenWeatherMap to work.
- Get your API key from: https://openweathermap.org/api
- After getting the API paste it into the api_key variable in the app.py file.
```python
def get_weather(self):
    api_key = "" #!IMPORTANT: paste your API key (get it from openweather)
    api = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}"

```

----------------------------------------------

### Future updates (maybe):
- [ ] Better night/day icons and a better system to change them.
- [ ] GUI improvements.
- [ ] Better save format and type.

----------------------------------------------

### License:
- This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
