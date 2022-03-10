import pandas as pd
import numpy as np
from opti_recruit.pipeline import Trainer
import opti_recruit.feature_engineering as fe
from opti_recruit.data import get_data,clean_data,features_to_drop,features_need_value,clean_df_value
from sklearn.model_selection import train_test_split
from opti_recruit.feature_engineering import add_features

dfs=get_data()

# def age_bin(a):
#     if a <= 19:
#         return "a"
#     if 20 <= a <= 24:
#         return "b"
#     if 25 <= a <= 29:
#         return "c"
#     if 30 <= a <= 34:
#         return 0.1
#     if a >= 35:
#         return 0.01


def pre_process():
    #value here for combine with df21 to train
    value_22=dfs[22][['sofifa_id','value_eur']]

    dfs_c=clean_df_value(dfs)
    #df22 is for predict,df21 is for train
    df22=dfs_c[22]
    #df22_d=df22.drop(columns='sofifa_id')
    df21=dfs_c[21]
    df20=dfs_c[20]
    frame=[df21,df20]
    dfdf=pd.concat(frame,join='outer')
    #dfdf['age']=dfdf['age'].apply(age_bin)

    # df22=dfs[22]
    # df22=add_features(df22)
    # df21=dfs[21]
    # df21=add_features(df21)
    # df20=dfs[20]
    # df20=add_features(df20)
    # frame=[df21,df20]
    # dfdf=pd.concat(frame,join='outer')
    # dfdf=dfdf.drop(columns='value_eur')


    df_train=dfdf.merge(value_22,on='sofifa_id',how='inner')
    #df_train=df_train.dropna(how='any')
    df_train=df_train.fillna(df_train.std()) # was .mean()

    X=df_train.drop(columns=['value_eur','sofifa_id'])
    y=df_train[['value_eur']]

    # X_train, X_test, y_train, y_test = train_test_split(X, y,
    #                                                 test_size=0.3,
    #                                                 random_state=10)
    trainer=Trainer(X,y)
    trainer.run()
    ans=trainer.predict(df22)


    return ans

def prediction():
    id22=dfs[22][['sofifa_id']]
    predt=pre_process()
    predt=pd.DataFrame(predt)
    result=id22.join(predt).rename(columns={0: "predict_value"}).set_index('sofifa_id')
    return result

# def get_index(df,player_id):
#     print(player_id)
#     return df[df['sofifa_id']==int(player_id)].index.tolist()[0]

def value_show(player_id):
    predict_value=prediction()
    res_value=predict_value.loc[player_id]
    return res_value

# def id_22():
#     #id22=dfs[22][['sofifa_id']]
#     predt=pre_process()
#     predt=pd.DataFrame(predt)
#     # result=id22.join(predt)
#     return predt


# def get_fianlresult():
#     id=id_22()
#     ans=pre_process()
#     c1=pd.DataFrame(id)
#     c2=pd.DataFrame(ans)
#     res=c1.join(c2)
#     return res
