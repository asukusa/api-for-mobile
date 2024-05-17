from fastapi import FastAPI

from .users.router import router as router_users
from .profiles.router import router as router_profiles
from .reactions.router import router as router_reactions
from .database import Base


app = FastAPI(title="FindMe")

app.include_router(router_users, prefix="/users")
app.include_router(router_profiles, prefix="/profiles")
app.include_router(router_reactions, prefix="/reactions")
