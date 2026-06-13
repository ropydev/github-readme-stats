# Author: Ronald Bello(ropydev)

from fastapi import FastAPI, Response
import requests
import textwrap
import html

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
