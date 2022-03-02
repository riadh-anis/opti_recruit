import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import opti_recruit.feature_engineering as fe
from opti_recruit.data import get_data
from functools import reduce



def get_team_metrics():
    """
    Method to create dataframes by season/by team/ by positions
    where values, overall and potentials are averaged
    """
    ## Import Data
    dfs = get_data()

    ## Extract yearly df
    df22 = fe.add_features(dfs[22])
    df21 = fe.add_features(dfs[21])
    df20 = fe.add_features(dfs[20])
    df19 = fe.add_features(dfs[19])

    ## dataframes names :
    frames = [df22,df21,df20,df19]
    teams_avg = ['df22_team','df21_team','df20_team','df19_team']
    team_pos = ['df22_team_pos','df21_team_pos','df20_team_pos','df19_team_pos']
    team_start = ['df22_team_start','df21_team_start','df20_team_start','df19_team_start']

    ## Dictionaries
    d_avg = {teams_avg[i]: frames[i] for i in range(0,4)}
    d_avg_pos = {team_pos[i]: frames[i] for i in range(0,4)}
    d_avg_start = {team_start[i]: frames[i] for i in range(0,4)}

    team_avg = {}
    team_avg_pos = {}
    team_avg_pos_start = {}
    ## Team Average
    for df in d_avg.keys():
        vars()[df]  = d_avg[df].groupby(['club_name'])[['value_eur','overall','potential']] \
            .mean() \
            .reset_index() \
            .add_suffix('_mean') \
            .rename(columns={"club_name_mean": "club_name"})
        team_avg[df] = vars()[df]

    ## Team Average by positions
    for df in d_avg_pos.keys():
        vars()[df]  = d_avg_pos[df].groupby(['club_name','player_pos'])[['value_eur','overall','potential']] \
            .mean() \
            .reset_index() \
            .pivot(index='club_name',columns='player_pos',values=['value_eur','overall','potential'])
        vars()[df].columns = list(map("_".join, vars()[df].columns))
        vars()[df] = vars()[df].rename(columns={"club_name_": "club_name"}).reset_index()
        team_avg_pos[df] = vars()[df]

    ## Team Average by positions for starting player
    for df in d_avg_start.keys():
        vars()[df]  = d_avg_start[df][d_avg_start[df]['is_bench']==False] \
            .groupby(['club_name','player_pos'])[['value_eur','overall','potential']] \
            .mean() \
            .reset_index() \
            .pivot(index='club_name',columns='player_pos',values=['value_eur','overall','potential'])
        vars()[df].columns = list(map("_".join, vars()[df].columns))
        vars()[df] = vars()[df].rename(columns={"club_name_": "club_name"}) \
            .add_suffix('_start').reset_index()
        team_avg_pos_start[df] = vars()[df]

    return team_avg,team_avg_pos,team_avg_pos_start


def join_team_df():
    """
    Method to join previous dataframes to original dataframes.
    Joined by club_name
    """
    ## Import Data
    dfs = get_data()
    team_avg,team_avg_pos,avg_pos_start = get_team_metrics()

    ## Create lists to iterate over for multiple join
    df_2022_list = [dfs[22],team_avg['df22_team'],team_avg_pos['df22_team_pos'],avg_pos_start['df22_team_start']]
    df_2021_list = [dfs[21],team_avg['df21_team'],team_avg_pos['df21_team_pos'],avg_pos_start['df21_team_start']]
    df_2020_list = [dfs[20],team_avg['df20_team'],team_avg_pos['df20_team_pos'],avg_pos_start['df20_team_start']]
    df_2019_list = [dfs[19],team_avg['df19_team'],team_avg_pos['df19_team_pos'],avg_pos_start['df19_team_start']]

    ## Join all dataframes together
    df_2022 = reduce(lambda  left,right: pd.merge(left,right,on=['club_name'],how='outer'), df_2022_list)
    df_2021 = reduce(lambda  left,right: pd.merge(left,right,on=['club_name'],how='outer'), df_2021_list)
    df_2020 = reduce(lambda  left,right: pd.merge(left,right,on=['club_name'],how='outer'), df_2020_list)
    df_2019 = reduce(lambda  left,right: pd.merge(left,right,on=['club_name'],how='outer'), df_2019_list)


    return df_2022,df_2021,df_2020,df_2019
# data_frames_22 = [df22, df22_team,df22_team_pos, df22_team_start]
# df_2022 = reduce(lambda  left,right: pd.merge(left,right,on=['club_name'],how='outer'), data_frames)
