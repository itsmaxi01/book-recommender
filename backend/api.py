from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.books import router as books_router
from routes.auth import router as auth_router


from routes.recommendations import router as recommendations_router
from routes.ratings import router as ratings_router
from routes.users import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(auth_router)
app.include_router(recommendations_router)
app.include_router(ratings_router)
app.include_router(users_router)

@app.get("/")
def home():

    return {
        "mensaje": "API funcionando"
    }