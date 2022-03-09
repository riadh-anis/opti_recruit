import pytz
import pandas as pd
import joblib,pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opti_recruit.similarity import cosine_recommendation, filter_params
from opti_recruit.pipeline import Trainer
from opti_recruit.data import get_api_data

PATH_TO_LOCAL_MODEL = 'model.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

dfs = get_api_data()
df22 = dfs[22]

with open("similarity_matrix.pickle", 'rb') as file:
    sim_matrix = pickle.load(file)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/similarities")
def compute_player_similarity(player_id, age_min=1, age_max=99, value_min=0, value_max=999999999, position=None):
    df_22_filtered = filter_params(df22, age_min, age_max, value_min, value_max, position)
    my_reco_list = cosine_recommendation(player_id, sim_matrix, df_22_filtered)
    return my_reco_list

# @app.get("/predict/marketvalue")
# def predict_marketvalue(player_id):
#     trainer = Trainer()
#     trainer.load_model()
#     trainer.predict(df.loc[player_id])
#     return
