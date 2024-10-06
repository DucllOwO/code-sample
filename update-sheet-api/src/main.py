from fastapi.middleware.cors import CORSMiddleware
from src.constants import Environment
from src.config import app_configs, settings
from src.config import app_configs
from fastapi import FastAPI
from src.on import on_start, on_shutdown
from src.checkout_ipn.routers import router as root_router
from src.spreadsheet.routers import router as spreadsheet_router

__import__("os").environ["TZ"] = "UTC"


app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def lifespan():
    # Startup
    await on_start()


@app.on_event("shutdown")
async def shutdown():
    await on_shutdown()


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

app.include_router(root_router, prefix='', tags=['Root'])
app.include_router(spreadsheet_router, prefix='/sheets', tags=["Sheets"])
