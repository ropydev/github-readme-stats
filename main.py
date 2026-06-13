# Author: Ronald Bello(ropydev)

from fastapi import FastAPI, Response
import requests
import textwrap
import html
import pygal
from pygal.style import LightStyle

app = FastAPI()


@app.get("/")
async def root():
    return False


@app.get("/repos/pin")
async def pinRepository(
    repo: str,
    username: str,
    bgColor="FFFFFF",
    color="0381e8",
    borderColor="606060",
    borderWidth="3",
    borderHide=False,
):
    try:
        headers = {"Accept": "application/vnd.github+json"}
        response = requests.get(
            f"https://api.github.com/repos/{username}/{repo}", headers=headers
        )
        data = response.json()
        description = html.escape(data["description"] or "")
        descriptionWrap = textwrap.wrap(description, 55)
        descriptionsvg = ""
        y = 0
        for l in descriptionWrap:
            descriptionsvg += f'<tspan x="30" dy="{20 if y>0 else 0}">{l}</tspan>'
            y += 1
        repoName = html.escape(data["name"] or "")
        if response.status_code == 404:
            return "Repo not Found"
        elif response.status_code == 200:
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
<text x="15" y="30" fill="#0381e8" font-family="Inter, sans-serif" font-size="18" font-weight="bold">
{repoName}
</text>
<text x="15" y="55" fill="#{color}" font-family="Inter, sans-serif" font-size="11">
{descriptionsvg}
</text>
<text x="15" y="140" fill="#{color}" font-family="Inter, sans-serif" font-size="11" font-weight="bold">
{data["language"]}
</text>
<text x="120" y="140" fill="#{color}" font-family="Inter, sans-serif" font-size="11" font-weight="bold">
☆ {data["stargazers_count"]}
</text>
<text x="225" y="140" fill="#{color}" font-family="Inter, sans-serif" font-size="11" font-weight="bold">
forks:{data["forks"]}
</text>
</g>
</svg>"""
            return Response(content=svg, media_type="image/svg+xml")
        else:
            return response.status_code
    except requests.ConnectionError:
        return "Connection Error"

@app.get("/stats/commits-activity")
async def activity(
    username
):
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = response.json()
    reposNames = [repo["name"] for repo in repos]
    days = list(range(1, 29))
    commits = [0] * 28
    for repo in reposNames:
        data = requests.get(f"https://api.github.com/repos/{username}/{repo}/stats/commit_activity").json()
        last4Weeks = data[-4:]
        i = 0
        for l in last4Weeks:
            for d in l["days"]:
                commits[i] += int(d)
                i+=1
    custom_style = LightStyle(
        background='#000000',   # fondo transparente
        plot_background='#606060',
        foreground='#ffffff',       # texto blanco
        foreground_strong='#ffffff',
        foreground_subtle='#aaaaaa',
        colors=('#FFFFFF',)         # color verde azulado (como tu paleta)
    )

    line_chart = pygal.Line(
        style=custom_style,
        show_legend=False,
        show_y_guides=False,
        show_x_guides=False,
        dots_size=2,
        stroke_style={'width': 2},
        width=600,   # más ancho
        height=150   # más bajo
    )

    line_chart.title = username+"'s Github Activity"
    line_chart.x_labels = days
    line_chart.add("", commits)

    svg_data = line_chart.render()
    return Response(content=svg_data, media_type="image/svg+xml")