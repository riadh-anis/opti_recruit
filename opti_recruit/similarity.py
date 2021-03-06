import opti_recruit.feature_engineering as fe
import opti_recruit.get_team_features as gtf
import pandas as pd
import numpy as np
import pickle
from sklearn.pipeline import Pipeline,make_pipeline,make_union
from sklearn.compose import make_column_transformer,make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from opti_recruit.data import get_data, clean_data, get_api_data
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors




def get_index(df,player_id):
    print(player_id)
    return df[df['sofifa_id']==int(player_id)].index.tolist()[0]

def normalize(array):
    return np.array([round(num, 2) for num in (array - min(array))*100/(max(array)-min(array))])

def numeric_pipeline(df):
    num_transformer = make_pipeline(SimpleImputer(), StandardScaler())
    num_col = make_column_selector(dtype_include=['float64','int64'])

    cat_transformer = OneHotEncoder()
    cat_col = make_column_selector(dtype_include=['object','category'])

    preproc_basic = make_column_transformer(
        (num_transformer, num_col),
        (cat_transformer, cat_col),
        remainder='passthrough')

    SimpleImputer.get_feature_names_out = (lambda self, names=None: self.feature_names_in_)

    num_trans_df = preproc_basic.fit_transform(df)

    sim_df = pd.DataFrame(num_trans_df,
                columns=preproc_basic.get_feature_names_out()
            )
    return sim_df

def get_similarity_dataframe(df):
    """Extract and transform the original dataframe to have only numerical feature"""
    to_drop = ['sofifa_id','short_name','player_positions','height_cm','weight_kg','club_team_id'
               ,'club_name' ,'league_name','club_position','club_joined',
               'club_contract_valid_until','nationality_name','nation_team_id',
               'preferred_foot','weak_foot','work_rate','body_type',
               'player_tags','player_traits','is_bench','potential_diff',
               'age_bin','player_pos','new_nationality','value_eur','wage_eur','release_clause_eur']

    num_df = df.drop(to_drop, axis = 1)

    similarity_df = numeric_pipeline(num_df)

    # Cosine Similarity matrix
    similarities = cosine_similarity(similarity_df)
    # KNN matrix
    # reco = NearestNeighbors(n_neighbors=11, algorithm='ball_tree').fit(similiraty_df)

    return similarities


def get_similarity_matrix():
    input_df = get_data()[22]
    df = fe.add_features(input_df)
    similarities = get_similarity_dataframe(df)
    with open(r'similarity_matrix_v3.pickle', 'wb') as file:
        pickle.dump(similarities, file)

def get_reco(index,sim_mat):
    index_search = index
    list_res=[]
    length = len(sim_mat.reco_player_index[index_search])
    for i in range(0,length):
        d = {
            'index_search' : index_search,
            'index' : sim_mat.reco_player_index[index_search][i],
            'score': sim_mat.scores[index_search][i]
            }
        list_res.append(d)
    reco_df = pd.DataFrame(list_res).set_index('index')
    return reco_df

def get_list_dict(df):
    list_res = []
    for i in range(0,len(df)):
        d = {
            'sofifa_id': int(df.iloc[i]['sofifa_id']),
            'score': df.iloc[i]['score'],
            'index' : i
            }
        list_res.append(d)
    return list_res

def filter_params(df, age_min, age_max, value_min, value_max, position):
    df = df[(df['age'] >= age_min) & (df['age'] <= age_max)]
    df = df[(df['value_eur'] >= value_min) & (df['value_eur'] <= value_max)]
    if position != None and position != 'All':
        df = df[df['player_positions'].str.contains(f'(^|,) {position}(,|$)')]
    return list(df.sofifa_id)

def cosine_recommendation(player_id, sim_mat, df):
    index = get_index(df, player_id)
    reco_df = get_reco(index, sim_mat)
    reco_df['sofifa_id'] = df.iloc[reco_df.index]['sofifa_id']
    # res = get_list_dict(reco_df)
    res = reco_df
    return res
