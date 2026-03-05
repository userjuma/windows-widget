# Desktop Widget for Windows

Windows has never had a proper always-on-top desktop widget. There are third-party apps that try to fill that gap, but most of them are bloated, require constant internet connections, or are simply abandoned. So this was built from scratch to do the job cleanly.

It sits on your desktop, shows you the current weather for your location, and lets you track the time in any city around the world. Nothing more, nothing less.


## What it does

- Shows live weather for your city, auto-detected on first launch
- Lets you search for any city to use as your weather location
- Displays clocks for multiple world cities, all updating in real time
- Works offline without issue, weather falls back to the last cached data
- Saves your settings between sessions
- Draggable, so you can put it exactly where you want on the screen
- Stays on top of other windows without getting in the way


## Requirements

- Windows 10 or 11
- Python 3.8 or newer, available at python.org
- An internet connection for the first weather load (not required afterwards)


## Setup

Run `install.bat` once. That installs the two Python dependencies the launcher needs:

```
pywebview
requests
```

After that, double-click `run.bat` any time you want to start the widget. No console window will appear.


## Files

| File | What it does |
|---|---|
| `widget.html` | The entire widget interface, HTML, CSS, and JavaScript in one file |
| `launcher.py` | Opens the widget in a frameless, always-on-top window using pywebview |
| `config.json` | Created automatically, stores your city list and weather location |
| `weather_cache.json` | Created automatically, stores the last weather data fetched |
| `run.bat` | Starts the widget silently |
| `install.bat` | Installs Python dependencies |


## Usage

On first launch, the widget will ask you to set a weather location. Click "Detect my location" to use your current IP location, or type a city name to search.

To add a world clock, click the `+` button on the right of the clock row. Search for a city and click it to add it. Hover over any clock card to reveal the remove button.

To change the weather city, click on the city name shown in the weather section.

Drag the widget by clicking and holding anywhere on the dark background and moving it to your preferred spot on the screen.


## Weather data

Weather is fetched from Open-Meteo, which is free and requires no API key. Location detection uses the browser geolocation API first, then falls back to IP-based detection via ipapi.co. City search for weather uses the Open-Meteo geocoding API.

When offline, the widget displays the last successfully fetched weather with a timestamp. The clocks continue working without any internet connection.


## Auto-start with Windows

To have the widget start when you log in:

1. Press `Win + R`, type `shell:startup`, and press Enter
2. Right-click in the folder that opens and choose "New > Shortcut"
3. Point the shortcut to `run.bat` in this folder


## License

MIT. Use it, modify it, share it.
