from fastapi import APIRouter, Response
import requests
from src.services import themes
import requests
import json

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    return response.json()

def get_languages(username):
    repos = get_repos(username)
    lang_stats = {}
    for repo in repos:
        url = repo["languages_url"]
        data = requests.get(url).json()
        for lang, size in data.items():
            lang_stats[lang.lower()] = lang_stats.get(lang.lower(), 0) + size

    return lang_stats

router = APIRouter()

@router.get("/langs")
async def topLangs(
    username: str,
    titleColor="0381e8",
    bgColor="FFFFFF",
    color="0381e8",
    borderColor="606060",
    borderWidth="3",
    borderHide=False,
    theme=""
):
    if theme:
        theme = themes.loadTheme(theme)
        bgColor = theme["bg"]
        titleColor = theme["title"]
        color = theme["text"]
        borderColor = theme["border"]
    lang_stats = get_languages(username)
    total = sum(lang_stats.values())
    percentages = {
        lang: f"{round((size / total) * 100, 2)}%"
        for lang, size in lang_stats.items()
    }
    sortPercentages = sorted(percentages.items(), key=lambda x: float(x[1].strip('%')), reverse=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="150">
<style>
    .fadeIn {
      opacity: 0;
      transform: translateY(10px);
      animation: fadeInMove 1s ease-out forwards;
    }
    @keyframes fadeInMove {
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }"""
    svg += f"""</style>
<g class="fadeIn">
<rect x="0" y="0" width="400" height="150" rx="20" ry="20" fill="#{bgColor}" stroke="#{borderColor}" stroke-width="{borderWidth if not bool(borderHide) else "0"}"/>
<text x="15" y="30" fill="#{titleColor}" font-family="Inter, sans-serif" font-size="18" font-weight="bold">
{username}'s Top Langs
</text>"""
    y = 80
    x = 40
    i = 0
    total_width = 350
    height = 10
    x_offset = 25
    for lang, percent in sortPercentages:
        langColor = themes.loadLangColor(lang.lower())
        svg += f"""<circle cx="{x-10}" cy="{y-4}" r="5" fill="#{langColor}" />
        <text x="{x}" y="{y}" fill="#{color}" font-family="Inter, sans-serif" font-size="14" font-weight="bold">
{lang} {percent}
</text>"""
        i+=1
        x = 200 if i%2 != 0 else 40
        y = y+20 if i%2 == 0 else y
        value = float(percent.strip('%')) / 100
        width = total_width * value
        svg += f'<rect x="{x_offset}" y="40" width="{width}" height="{height}" fill="#{langColor}"/>'
        x_offset += width

    svg+="""</g>
</svg>"""
    return Response(content=svg, media_type="image/svg+xml")