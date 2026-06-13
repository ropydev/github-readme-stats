# Author: Ronald Bello(ropydev)

from fastapi import FastAPI, Response
import requests
import textwrap
import html
import matplotlib.pyplot as plt
import io

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
    username,
    title = "Commits Activity"
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
    plt.style.use("seaborn-v0_8-dark")
    fig, ax = plt.subplots(figsize=(8, 3), dpi=120)
    fig.patch.set_facecolor("#0B0C10")
    ax.set_facecolor("#0B0C10")
    ax.plot(days, commits, color="#FFFFFF", linewidth=2.5)
    ax.scatter(days, commits, color="#FFFFFF", s=20, zorder=3)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.grid(False)
    ax.set_xlabel("Days", fontsize=10, color="#E0E0E0", labelpad=5)
    ax.set_ylabel("Commits", fontsize=10, color="#E0E0E0", labelpad=5)
    ax.set_title(title, fontsize=12, color="#FFFFFF", pad=10)
    svg_buffer = io.StringIO()
    plt.savefig(svg_buffer, format="svg", bbox_inches="tight")
    plt.close()
    svg_code = svg_buffer.getvalue()
    svg_buffer.close()
    return Response(content=svg_code, media_type="image/svg+xml")