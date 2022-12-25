import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split


def catboost(df: pd.DataFrame):
    X = df.drop(['dislikes'], axis=1)
    y = df['dislikes']
    folds = 5
    cat_regressor = CatBoostRegressor(silent=True)
    pipeline = Pipeline([('estimator', cat_regressor)])
    cv = KFold(n_splits=folds)
    #scores = cross_val_score(pipeline, X, y, cv=cv, scoring='neg_mean_absolute_error')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    cat_regressor.fit(X_train, y_train)
    return cat_regressor


def bag_of_words(df: pd.DataFrame):
    X = df.drop(['dislikes'], axis=1)
    categorical_features = X.columns[np.where(X.dtypes != float)[0]].values.tolist()
    X[categorical_features] = X[categorical_features].astype(str)
    y = df['dislikes']
    folds = 5
    regressor = CatBoostRegressor(silent=True)
    pipeline = Pipeline([('estimator', regressor)])
    cv = KFold(n_splits=folds)
    #scores = cross_val_score(pipeline, X, y, cv=cv, scoring='neg_mean_absolute_error')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    regressor.fit(X_train, y_train, cat_features = categorical_features)
    return regressor