import webview
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')
CACHE_FILE  = os.path.join(BASE_DIR, 'weather_cache.json')
HTML_FILE   = os.path.join(BASE_DIR, 'widget.html')

DEFAULT_CONFIG = {
    "cities": [
        {"name": "New York",  "timezone": "America/New_York",  "country": "USA"},
        {"name": "London",    "timezone": "Europe/London",     "country": "UK"},
        {"name": "Tokyo",     "timezone": "Asia/Tokyo",        "country": "Japan"}
    ],
    "weather": {"city": "", "lat": None, "lon": None},
    "window":  {"x": 80, "y": 80}
}

app_window = None


class Api:

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return DEFAULT_CONFIG

    def save_config(self, config):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return str(e)

    def load_weather_cache(self):
        try:
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def save_weather_cache(self, data):
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            return str(e)

    def get_window_position(self):
        global app_window
        if app_window:
            return {"x": app_window.x, "y": app_window.y}
        return {"x": 80, "y": 80}

    def move_window(self, x, y):
        global app_window
        if app_window:
            app_window.move(int(x), int(y))
        return True

    def save_window_position(self, x, y):
        try:
            cfg = self.load_config()
            cfg["window"] = {"x": int(x), "y": int(y)}
            self.save_config(cfg)
        except Exception:
            pass
        return True

    def quit_app(self):
        global app_window
        if app_window:
            app_window.destroy()


def main():
    global app_window
    api = Api()
    config = api.load_config()
    wx = config.get("window", {}).get("x", 80)
    wy = config.get("window", {}).get("y", 80)

    html_url = 'file:///' + HTML_FILE.replace('\\', '/')

    app_window = webview.create_window(
        title='Widget',
        url=html_url,
        js_api=api,
        width=700,
        height=380,
        x=wx,
        y=wy,
        frameless=True,
        on_top=True,
        background_color='#141416',
        transparent=False,
        min_size=(420, 260)
    )

    webview.start(debug=False)


if __name__ == '__main__':
    main()
