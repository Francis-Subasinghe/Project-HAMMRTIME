# predictor.py – Model loading and prediction
import xgboost as xgb
import pandas as pd
from config import driver_to_id, team_to_id, tire_to_id

# Load pre-trained model
model = xgb.XGBRegressor()
model.load_model("models/laptime_predictor_v2.json")

def predict_lap_time(driver_name, team, tire, stint_norm, lap_trend,
                     time_sec, pace_dev, delta_to_best, rolling_avg):
    input_data = pd.DataFrame({
        'DriverID': [driver_to_id[driver_name]],
        'TeamID': [team_to_id[team]],
        'TyreCode': [tire_to_id[tire]],
        'StintNorm': [stint_norm],
        'LapTrend': [lap_trend],
        'TimeSeconds': [time_sec],
        'PaceDeviation': [pace_dev],
        'DeltaToBest': [delta_to_best],
        'RollingAvgDriver': [rolling_avg]
    })

    prediction = model.predict(input_data)[0]
    return prediction, input_data, model
