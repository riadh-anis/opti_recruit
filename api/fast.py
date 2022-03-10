import pytz
import pandas as pd
import joblib,pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opti_recruit.similarity import cosine_recommendation, filter_params,get_list_dict
from opti_recruit.pipeline import Trainer
from opti_recruit.value_predict import prediction,value_show
from opti_recruit.data import get_api_data, get_data

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

with open("similarity_matrix_v3.pickle", 'rb') as file:
    sim_matrix = pickle.load(file)

@app.get("/")
def index():
    return {"greeting": "Hello world"}


@app.get("/similarities")
def compute_player_similarity(player_id, age_min=1, age_max=99, value_min=0, value_max=999999999, position=None):

    my_reco_df = cosine_recommendation(player_id, sim_matrix, df22)

    #transform reco_list into dataframe
    df_22_filtered = filter_params(df22, int(age_min), int(age_max), int(value_min), int(value_max), position)

    #filter my_reco_df with df_filtered
    boolean_series = my_reco_df.sofifa_id.isin(df_22_filtered)
    my_reco_filt = my_reco_df[boolean_series]
    # my_reco_list = cosine_recommendation(player_id, sim_matrix, df_22_filtered)

    return get_list_dict(my_reco_filt)


# @app.get("/value")
# def value_show(player_id):
#     predict_value=prediction()
#     res_value=predict_value.loc[int(player_id)]
#     return res_value


# @app.get("/predict/marketvalue")
# def predict_marketvalue(player_id):
#     trainer = Trainer()
#     trainer.load_model()
#     trainer.predict(df.loc[player_id])
#     return
