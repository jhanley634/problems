#! /usr/bin/env python
# Copyright 2022 John Hanley. MIT licensed.
from pathlib import Path

import gpxpy
import mlmodel
import numpy as np
import pandas as pd
import typer
import xgboost as xgb


def directions(in_file="/tmp/10-Jul-2022-1714.gpx"):
    in_file = Path(in_file).expanduser()
    with open(in_file) as fin:
        _show(gpxpy.parse(fin))


def _show(gpx):
    dtrain = xgb.DMatrix(X)

    # mlmodel.E_train is the boolean event indicator
    # mlmodel.T_train is the time elapsed when event is either observed or censored
    y_lower_bound = np.where(mlmodel.E_train == 1, mlmodel.T_train, 0)
    y_upper_bound = np.where(mlmodel.E_train == 1, mlmodel.T_train, np.inf)

    dtrain.set_float_info("label_lower_bound", y_lower_bound)
    dtrain.set_float_info("label_upper_bound", y_upper_bound)

    params = {
        "objective": "survival:aft",
        "eval_metric": "aft-nloglik",
        "aft_loss_distribution": "normal",
        "aft_loss_distribution_scale": 1.20,
        "tree_method": "hist",
        "learning_rate": 0.05,
        "max_depth": 2,
    }

    bst = xgb.train(params, dtrain, num_boost_round=5, evals=[(dtrain, "train")])

    mlmodel.model = bst

    dtest = xgb.DMatrix(self.X_test)
    mlmodel.y_pred_hazard = pd.DataFrame(mlmodel.model.predict(dtest))


if __name__ == "__main__":
    typer.run(directions)
