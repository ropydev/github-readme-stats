from fastapi import FastAPI
from src.routes import pinrepos, commitsgraph, toplangs

app = FastAPI()

app.include_router(pinrepos.router, prefix="/repos", tags=["Repos"])
app.include_router(commitsgraph.router, prefix="/stats", tags=["Commits Activity"])
app.include_router(toplangs.router, prefix="/top", tags=["Top Langs"])

@app.get("/")
async def root():
    return {
        "Author": "Ronald Bello (ropydev)", 
        "author_github": "https://github.com/ropydev"
    }