import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from opti_recruit.data import load_data

def is_bench(d):
    if d in ("SUB", "RES", ""):
        return True
    return False

def age_bins(a):
    if a <= 19:
        return 'Below 20'
    if 20 <= a <= 24:
        return '20-24'
    if 25 <= a <= 29:
        return '25-29'
    if 30 <= a <= 34:
        return '30-34'
    if a >= 35:
        return 'Over 34'

# add get data
dfs = get_data()
top_nat = list(dfs[22].nationality_name.value_counts().iloc[:20].index)

def top_nationality(val):
    if val not in top_nat:
        return 'Others'
    return val

def play_pos(a):
    if a in ('ST','CF','RF','LF','RW','LW'):
        return 'ATT'
    if a in ('RM','LM','CAM','CDM','CM','LWB','RWB'):
        return 'MID'
    if a in ('CB','CF','LB','RB'):
        return 'DEF'
    return a

def prefered_position(positions):
    a = positions.split(',')
    return a[0]


def feature_engineering(df):
    to_drop = [
        'club_logo_url','nation_flag_url','club_flag_url','nation_logo_url','player_face_url','dob','player_url',
        'real_face','nation_jersey_number','nation_position','club_loaned_from','long_name','player_url',
        'ls','st','rs','lw','lf','cf','rf','rw','lam','cam','ram','lm','lcm','cm','rcm',
        'rm','lwb','ldm', 'cdm','rdm','rwb','lb','lcb','cb','rcb','rb','gk','club_jersey_number','nationality_id',
        'club_jersey_number','goalkeeping_diving','goalkeeping_handling','goalkeeping_kicking' ,
        'goalkeeping_positioning' ,'goalkeeping_reflexes', 'goalkeeping_speed'
        ]

    clean_df = df.drop(to_drop,axis = 1)

    for frame in dfs:
        frame['is_bench'] = frame['club_position'].apply(is_bench)
        frame['potential_diff'] = frame['potential'] - frame['overall']
        frame[['att_rate', 'def_rate']] = frame['work_rate'].str.split('/', 1, expand=True)
        frame['age_bin'] = frame['age'].apply(age_bins)
        frame['prefered_pos'] = frame['player_positions'].apply(prefered_position)
        frame['player_pos'] = frame['prefered_pos'].apply(play_pos)
        frame['new_nationality'] = frame['nationality_name'].apply(top_nationality)
        frame['prefered_pos'] = frame['prefered_pos'].astype('category')
        frame['is_bench'] = frame['is_bench'].astype('category')
        frame['player_pos'] = frame['player_pos'].astype('category')
        frame['new_nationality'] = frame['new_nationality'].astype('category')
