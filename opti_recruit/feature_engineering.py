import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from opti_recruit.data import get_data

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


def add_features(df):
    to_drop = [
        'club_logo_url','nation_flag_url','club_flag_url','nation_logo_url','player_face_url','dob','player_url',
        'real_face','nation_jersey_number','nation_position','club_loaned_from','long_name','player_url',
        'ls','st','rs','lw','lf','cf','rf','rw','lam','cam','ram','lm','lcm','cm','rcm',
        'rm','lwb','ldm', 'cdm','rdm','rwb','lb','lcb','cb','rcb','rb','gk','club_jersey_number','nationality_id',
        'club_jersey_number','goalkeeping_diving','goalkeeping_handling','goalkeeping_kicking' ,
        'goalkeeping_positioning' ,'goalkeeping_reflexes', 'goalkeeping_speed'
        ]

    df = df.drop(to_drop,axis = 1)

    df['is_bench'] = df['club_position'].apply(is_bench)
    df['potential_diff'] = df['potential'] - df['overall']
    df[['att_rate', 'def_rate']] = df['work_rate'].str.split('/', 1, expand=True)
    df['age_bin'] = df['age'].apply(age_bins)
    df['prefered_pos'] = df['player_positions'].apply(prefered_position)
    df['player_pos'] = df['prefered_pos'].apply(play_pos)
    df['new_nationality'] = df['nationality_name'].apply(top_nationality)
    df['prefered_pos'] = df['prefered_pos'].astype('category')
    df['is_bench'] = df['is_bench'].astype('category')
    df['player_pos'] = df['player_pos'].astype('category')
    df['new_nationality'] = df['new_nationality'].astype('category')

    return df
