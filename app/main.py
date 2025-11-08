from fastapi import FastAPI
from app.api.v1 import routes_user
from app.api.v1 import routes_protected
app = FastAPI(title="MyFastAPI")

app.include_router(routes_user.router, prefix="/api/v1", tags=["users"])
app.include_router(routes_protected.router, prefix="/api/v1", tags=["auth"])