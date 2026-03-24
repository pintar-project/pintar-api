import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


from routes.auth import router as auth_router
from routes.siswa import router as siswa_router
from routes.admin import router as admin_router
from routes.kelas import router as kelas_router
from routes.modul import router as modul_router
from routes.tahun_ajaran import router as tahun_ajaran_router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "If-None-Match"],
    expose_headers=["ETag"],
)


@app.middleware("http")
async def add_timestamp_middleware(request: Request, call_next):
    request.state.timestamp = datetime.datetime.now(datetime.timezone.utc)
    response = await call_next(request)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "message": exc.detail,
                "data": None,
            }
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "message": "validation error",
                "data": exc.errors(),
            }
        ),
    )


app.include_router(auth_router)
app.include_router(siswa_router)
app.include_router(admin_router)
app.include_router(kelas_router)
app.include_router(modul_router)
app.include_router(tahun_ajaran_router)
