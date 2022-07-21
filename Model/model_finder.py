import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics  import roc_auc_score,accuracy_score
from File_Ops.file_ops import File_Ops
from sklearn.preprocessing import LabelEncoder


class Model_Finder:
    def __init__(self,clustered_data,list_of_clusters):
        self.clustered_data = clustered_data
        self.list_of_clusters = list_of_clusters
        self.file_ops = File_Ops()

    def get_model(self):
        for i in self.list_of_clusters:
            data = self.clustered_data[self.clustered_data['cluster'] == i]
            X = data.drop(['cluster','label'],axis=1)
            y = data['label']

            X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)
            self.model , self.model_name = self.find_Model(X_train,X_test,y_train,y_test)
            self.file_ops.save_model(self.model,self.model_name+str(i))






    def find_Model(self,X_train, X_test, y_train, y_test):

        le = LabelEncoder()
        new_y_train = le.fit_transform(y_train)
        new_y_test = le.fit_transform(y_test)

        self.xgb = self.find_best_xgboost(X_train,new_y_train)
        self.xgb_score = accuracy_score(new_y_test,self.xgb.predict(X_test))

        self.rfc = self.find_best_random_forest(X_train,y_train)
        self.rfc_score = accuracy_score(y_test,self.rfc.predict(X_test))

        if self.rfc_score > self.xgb_score:
            return self.rfc , "Random Forest"
        else:
            return self.xgb , "XGBoost"


    def find_best_xgboost(self,X_train,y_train):

        self.param_grid_xgboost = {

            'learning_rate': [0.5, 0.1, 0.01, 0.001],
            'max_depth': [3, 5, 10, 20],
            'n_estimators': [10, 50, 100, 200]

        }
        self.grid = GridSearchCV(XGBClassifier(objective='binary:logistic'),param_grid=self.param_grid_xgboost)
        self.grid.fit(X_train,y_train)

        self.learning_rate = self.grid.best_params_['learning_rate']
        self.max_depth = self.grid.best_params_['max_depth']
        self.n_estimators = self.grid.best_params_['n_estimators']

        self.xgb = XGBClassifier(learning_rate = self.learning_rate, max_depth = self.max_depth, n_estimators = self.n_estimators)
        self.xgb.fit(X_train,y_train)
        return self.xgb



    def find_best_random_forest(self,X_train,y_train):

        self.param_grid = {
            "n_estimators": [10, 50, 100, 130],
            "criterion": ['gini', 'entropy'],
            "max_depth": range(2, 4, 1),
            "max_features": ['auto', 'log2']
        }

        self.grid = GridSearchCV(RandomForestClassifier(),param_grid=self.param_grid)
        self.grid.fit(X_train,y_train)

        self.n_estimators = self.grid.best_params_["n_estimators"]
        self.criterion = self.grid.best_params_['criterion']
        self.max_depth = self.grid.best_params_['max_depth']
        self.max_features = self.grid.best_params_['max_features']

        self.rfc = RandomForestClassifier(n_estimators=self.n_estimators,criterion=self.criterion,
                                          max_depth=self.max_depth,max_features=self.max_features)

        self.rfc.fit(X_train,y_train)

        return self.rfc





