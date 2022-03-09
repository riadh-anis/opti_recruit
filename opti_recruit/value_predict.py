import pandas as pd
import numpy as np
from opti_recruit.pipeline import Trainer
import opti_recruit.feature_engineering as fe
from opti_recruit.data import get_data,clean_data,features_to_drop,features_need_value,clean_df_value
from sklearn.model_selection import train_test_split

dfs=get_data()

def pre_process():
    #value here for combine with df21 to train
    value_22=dfs[22][['sofifa_id','value_eur']]

    dfs_c=clean_df_value(dfs)
    #df22 is for predict,df21 is for train
    df22=dfs_c[22]
    #df22_d=df22.drop(columns='sofifa_id')
    df21=dfs_c[21]

    df_train=df21.merge(value_22,on='sofifa_id',how='inner')
    df_train=df_train.fillna(df_train.mean())

    X=df_train.drop(columns=['value_eur','sofifa_id'])
    y=df_train[['value_eur']]

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size=0.2,
                                                    random_state=10)
    trainer=Trainer(X_train,y_train)
    trainer.run()
    ans=trainer.predict(df22)


    return ans

def prediction():
    id22=dfs[22][['sofifa_id']]
    predt=pre_process()
    predt=pd.DataFrame(predt)
    result=id22.join(predt).rename(columns={0: "predict_value"}).set_index('sofifa_id')
    return result

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
