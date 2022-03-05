import pytz
import pandas as pd
import joblib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opti_recruit.similarity import cosine_recommendation
from opti_recruit.pipeline import Trainer
from opti_recruit.data import get_data

PATH_TO_LOCAL_MODEL = 'model.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

dfs = get_data()



@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/similarities")
def compute_player_similarity(player_name):
    df = cosine_recommendation(player_name)
    return df.reset_index().to_dict()

# @app.get("/predict/marketvalue")
# def predict_marketvalue(player_id):
#     trainer = Trainer()
#     trainer.load_model()
#     trainer.predict(df.loc[player_id])
#     return
