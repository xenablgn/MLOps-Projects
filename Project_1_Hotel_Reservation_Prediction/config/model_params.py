from scipy.stats import randint, uniform

XGBOOST_PARAMS = {
    "learning_rate": uniform(0.001, 0.01),
    "max_depth": randint(5, 15),
    "n_estimators": randint(100, 200),
}

RANDOM_SEARCH_PARAMS = {
    "n_iter": 10,
    "cv": 3,
    "verbose": 2,
    "n_jobs": -1,
    "random_state": 42,
    "scoring": "accuracy"
}