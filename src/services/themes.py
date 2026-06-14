import json

def loadTheme(theme):
    with open("themes/themes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        theme = data[theme]
        return {
            "bg": theme["bg_color"],
            "title": theme["title_color"],
            "text": theme["text_color"],
            "border": theme["border_color"]
        }

def loadLangColor(lang):
    with open("themes/languages_colors.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        colorNormalize = {k.lower(): v for k, v in data.items()}
        color = colorNormalize[lang]
        return color