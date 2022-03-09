import pytz
import pandas as pd
import joblib,pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opti_recruit.similarity import cosine_recommendation
from opti_recruit.pipeline import Trainer
from opti_recruit.data import get_data
from opti_recruit.value_predict import prediction

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
df22 = dfs[22]

with open("similarity_matrix.pickle", 'rb') as file:
    sim_matrix = pickle.load(file)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/similarities")
def compute_player_similarity(player_name):
    my_reco_list = cosine_recommendation(player_name,sim_matrix,df22)
    return my_reco_list

@app.get("/value")
def get_2023_value(sofifaid):
    value_lst=prediction()
    return value_lst

# @app.get("/predict/marketvalue")
# def predict_marketvalue(player_id):
#     trainer = Trainer()
#     trainer.load_model()
#     trainer.predict(df.loc[player_id])
#     return
