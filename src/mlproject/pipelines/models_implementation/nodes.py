import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import pickle


def catboost(df: pd.DataFrame):
    X = df.drop(['dislikes'], axis=1)
    y = df['dislikes']
    folds = 5
    cat_regressor = CatBoostRegressor(silent=True)
    pipeline = Pipeline([ ('estimator', cat_regressor)])
    cv = KFold(n_splits=folds)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring='neg_mean_absolute_error')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    cat_regressor.fit(X_train, y_train)
    return cat_regressor
