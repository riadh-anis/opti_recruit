import pandas as pd

def get_data(years = [17, 18, 19, 20, 21, 22]):
    """method to get the training data from the raw data"""
    dfs = {}
    for year in years:
        dfs[year] = pd.read_csv(f'../raw_data/fifa22/players_{year}.csv', low_memory=False)
        # dfs[year] = pd.read_csv(f'raw_data/fifa22/players_{year}.csv', low_memory=False)
    return dfs

def get_api_data(years = [17, 18, 19, 20, 21, 22]):
    """method to get the training data from the raw data"""
    dfs = {}
    for year in years:
        dfs[year] = pd.read_csv(f'raw_data/fifa22/players_{year}.csv', low_memory=False)
    return dfs

def clean_data(dfs):
    """method to clean the data"""
    for year, df in dfs.items():
        dfs[year] = df.drop(features_to_drop(), axis = 1)
    return dfs

def features_to_drop():
    """method to get the features to drop from the raw data"""
    return ['club_logo_url','nation_flag_url','club_flag_url','nation_logo_url','player_face_url','dob','player_url','real_face','nation_jersey_number','nation_position','club_loaned_from','long_name','player_url','ls','st','rs','lw','lf','cf','rf','rw','lam','cam','ram','lm','lcm','cm','rcm','rm','lwb','ldm', 'cdm','rdm','rwb','lb','lcb','cb','rcb','rb','gk','club_jersey_number','nationality_id','club_jersey_number','goalkeeping_diving','goalkeeping_handling','goalkeeping_kicking' ,'goalkeeping_positioning' ,'goalkeeping_reflexes', 'goalkeeping_speed']

# please don't remove below
def features_need_value():
    return ['sofifa_id','physic','defending','dribbling','passing',
            'shooting','pace','release_clause_eur','international_reputation',
            'skill_moves','weak_foot','club_contract_valid_until',
            'league_level','club_team_id','weight_kg','height_cm','age','wage_eur',
            'potential','overall']

def clean_df_value(dfs):
    for year, df in dfs.items():
        dfs[year] = df[features_need_value()]
    return dfs


if __name__ == '__main__':
    dfs = get_data()
