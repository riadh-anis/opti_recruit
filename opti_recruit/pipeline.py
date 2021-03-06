
import numpy as np
import joblib
from sklearn.metrics import mean_squared_error
from sklearn.compose import ColumnTransformer,make_column_selector,make_column_transformer,TransformedTargetRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline,make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

PATH_TO_LOCAL_MODEL = 'model.joblib'

class Trainer(object):
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y/100000000

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        SimpleImputer.get_feature_names_out = (lambda self,
                                                names=None:
                                                    self.feature_names_in_)

        num_transformer = make_pipeline(SimpleImputer(strategy='mean'),
                                        StandardScaler())
        num_col = make_column_selector(dtype_include=['int64','float64'])

        cat_transformer = make_pipeline(SimpleImputer(strategy = 'most_frequent')
                                ,OneHotEncoder(handle_unknown='ignore', sparse=True))

        cat_col = make_column_selector(dtype_include=['object','bool','category'])

        regressor=LinearRegression()

        preproc = make_column_transformer(
            (num_transformer, num_col),
            (cat_transformer, cat_col),
            remainder='passthrough')

        self.pipeline = make_pipeline(preproc, regressor)
        return self.pipeline

    def run(self):
        self.set_pipeline()
        self.pipeline.fit(self.X, self.y)

    def predict(self, X_test):
        y_pred = self.pipeline.predict(X_test)
        return y_pred*100000000

    def evaluate(self, y_pred, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        rmse = np.sqrt(mean_squared_error(y_pred, y_test))
        return round(rmse, 2)

    def save_model_locally(self):
        """Save the model into a .joblib format"""
        joblib.dump(self.pipeline, PATH_TO_LOCAL_MODEL)
        # self.predict(X) ## dump the final predicted values into json
        print(colored("model.joblib saved locally", "green"))

    def load_model(self):
        pipeline = joblib.load(PATH_TO_LOCAL_MODEL)
        return pipeline

# class Trainer(object):
#     def __init__(self, X, y):
#         """
#             X: pandas DataFrame
#             y: pandas Series
#         """
#         self.pipeline = None
#         self.X = X
#         self.y = y
#         # for MLFlow
#         #self.experiment_name = EXPERIMENT_NAME

#     def set_experiment_name(self, experiment_name):
#         '''defines the experiment name for MLFlow'''
#         self.experiment_name = experiment_name
# def run(self):
#     self.set_pipeline()
#     self.mlflow_log_param("model", "Linear")
#     self.pipeline.fit(self.X, self.y)

# def evaluate(self, X_test, y_test):
#     """evaluates the pipeline on df_test and return the RMSE"""
#     y_pred = self.pipeline.predict(X_test)
#     rmse = np.sqrt(mean_squared_error(y_pred, y_test))
#     self.mlflow_log_metric("rmse", rmse)
#     return round(rmse, 2)



# MLFlow methods
    # @memoized_property
    # def mlflow_client(self):
    #     mlflow.set_tracking_uri(MLFLOW_URI)
    #     return MlflowClient()

    # @memoized_property
    # def mlflow_experiment_id(self):
    #     try:
    #         return self.mlflow_client.create_experiment(self.experiment_name)
    #     except BaseException:
    #         return self.mlflow_client.get_experiment_by_name(
    #             self.experiment_name).experiment_id

    # @memoized_property
    # def mlflow_run(self):
    #     return self.mlflow_client.create_run(self.mlflow_experiment_id)

    # def mlflow_log_param(self, key, value):
    #     self.mlflow_client.log_param(self.mlflow_run.info.run_id, key, value)

    # def mlflow_log_metric(self, key, value):
    #     self.mlflow_client.log_metric(self.mlflow_run.info.run_id, key, value)
