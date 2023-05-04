from urllib.request import Request

from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

import auth
import my_err
from api import router
from database import db_session
from service.model import ClassifierModule
from settings import settings


tags_metadata = [
    {
        "name": "user",
        "description": "Операции с пользователями",
    }
]

db_session.global_init()
model = ClassifierModule(
    path_to_model="model_data/pulse_model",
    path_to_tokenizer="model_data/keras_tokenizer.pickle",
    # init_stopwords=False
)

print(model.predict_one("Модуль, используемый для создания виртуальных сред и управления ими, называется ven. обычно ven устанавливает самую последнюю версию Python, которая у вас есть в наличии. Если в вашей системе установлено несколько версий Python, вы можете выбрать конкретную версию Python, запустив python 3 или любую другую версию, которую вы хотите.", 5).get_human_readable_separates())

app = FastAPI(
    title="TinkScreen",
    description="API для бота TinkScreen",
    openapi_tags=tags_metadata,
    dependencies=[Depends(auth.get_api_key)],
    debug=settings().API_DEBUG,
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "ErrorID": my_err.VALIDATION_ERROR}),
    )


@app.exception_handler(my_err.APIError)
async def api_error_handler(request: Request, exc: my_err.APIError):
    # print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{"msg": exc.msg}], "ErrorID": exc.err_id},
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": [{"msg": "Internal server error"}], "ErrorID": my_err.INTERNAL_SERVER_ERROR},
    )


@app.get("/")
async def root():
    return {"message": "Hello Tinkoff!"}
