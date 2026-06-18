from fastapi import APIRouter, Response
import requests, io, json
import matplotlib.pyplot as plt
from src.services import themes

router = APIRouter()

@router.get("/commits-activity")
async def activity(
    username: str,
    title = "Commits Activity",
    titleColor="0381e8",
    bgColor="FFFFFF",
    color="0381e8",
    theme=""
):
    if theme:
        theme = themes.loadTheme(theme)
        if theme["error"]:
            return theme["message"]
        bgColor = theme["bg"]
        titleColor = theme["title"]
        color = theme["text"]
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = response.json()
    reposNames = [repo["name"] for repo in repos]
    days = list(range(1, 29))
    commits = [0] * 28
    for repo in reposNames:
        data = requests.get(f"https://api.github.com/repos/{username}/{repo}/stats/commit_activity").json()
        if not data:
            return {"Error": "No commit activity data"}
        last4Weeks = data[-4:]
        i = 0
        for l in last4Weeks:
            for d in l["days"]:
                commits[i] += int(d)
                i+=1
    plt.style.use("seaborn-v0_8-dark")
    fig, ax = plt.subplots(figsize=(8, 3), dpi=120)
    fig.patch.set_facecolor(f"#{bgColor}")
    ax.set_facecolor(f"#{bgColor}")
    ax.plot(days, commits, color=f"#{titleColor}", linewidth=2.5)
    ax.scatter(days, commits, color=f"#{titleColor}", s=20, zorder=3)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.grid(False)
    ax.set_xlabel("Days", fontsize=10, color=f"#{color}", labelpad=5)
    ax.set_ylabel("Commits", fontsize=10, color=f"#{color}", labelpad=5)
    ax.set_title(title, fontsize=12, color=f"#{titleColor}", pad=10)
    svg_buffer = io.StringIO()
    plt.savefig(svg_buffer, format="svg", bbox_inches="tight")
    plt.close()
    svg_code = svg_buffer.getvalue()
    svg_buffer.close()
    return Response(content=svg_code, media_type="image/svg+xml")