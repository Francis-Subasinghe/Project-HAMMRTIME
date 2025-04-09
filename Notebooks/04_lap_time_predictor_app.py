import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import os

# Load pre-trained model
model = xgb.XGBRegressor()
model.load_model("models/laptime_predictor_v2.json")

# Driver and team data (2024 season)
driver_names = [
    "Max Verstappen", "Sergio Perez", "Lewis Hamilton", "George Russell",
    "Charles Leclerc", "Carlos Sainz", "Lando Norris", "Oscar Piastri",
    "Fernando Alonso", "Lance Stroll", "Pierre Gasly", "Esteban Ocon",
    "Yuki Tsunoda", "Daniel Ricciardo", "Kevin Magnussen", "Nico Hülkenberg",
    "Valtteri Bottas", "Zhou Guanyu", "Alex Albon", "Logan Sargeant"
]

# Map drivers to their real 2024 teams
driver_team_map = {
    "Max Verstappen": "Red Bull",
    "Sergio Perez": "Red Bull",
    "Lewis Hamilton": "Mercedes",
    "George Russell": "Mercedes",
    "Charles Leclerc": "Ferrari",
    "Carlos Sainz": "Ferrari",
    "Lando Norris": "McLaren",
    "Oscar Piastri": "McLaren",
    "Fernando Alonso": "Aston Martin",
    "Lance Stroll": "Aston Martin",
    "Pierre Gasly": "Alpine",
    "Esteban Ocon": "Alpine",
    "Yuki Tsunoda": "AlphaTauri",
    "Daniel Ricciardo": "AlphaTauri",
    "Kevin Magnussen": "Haas",
    "Nico Hülkenberg": "Haas",
    "Valtteri Bottas": "Alfa Romeo",
    "Zhou Guanyu": "Alfa Romeo",
    "Alex Albon": "Williams",
    "Logan Sargeant": "Williams"
}

driver_to_id = {name: idx for idx, name in enumerate(driver_names)}
teams = sorted(set(driver_team_map.values()))
team_to_id = {team: idx for idx, team in enumerate(teams)}
tire_types = ['SOFT', 'MEDIUM', 'HARD']
tire_to_id = {tire: idx for idx, tire in enumerate(tire_types)}

# Load lap data for historical metrics
lap_data = pd.read_csv("data/processed_lap_data.csv")

def main():
    st.set_page_config(page_title="Lap Time Predictor", layout="centered")
    st.title("🏁 Project HAMMRTIME")
    tabs = st.tabs(["🔮 Lap Time Predictor", "⚖️ Compare Drivers"])

    # TAB 1: Lap Time Predictor
    with tabs[0]:
        st.markdown("Predict an F1 driver's lap time based on car, tire, and session inputs.")

        driver_name = st.selectbox("Driver", driver_names)
        team = driver_team_map[driver_name]
        st.markdown(f"**Team:** {team}")

        with st.form("lap_input_form"):
            tire = st.selectbox("Tyre Compound", tire_types)
            stint_norm = st.slider("Normalized Stint", 0.0, 1.0, 0.5)
            lap_trend = st.slider("Lap Trend (Progress %)", 0.0, 1.0, 0.5)
            time_sec = st.slider("Time into Session (s)", 0, 3000, 1000)
            pace_dev = st.slider("Pace Deviation from Driver's Best (s)", 0.0, 10.0, 2.0)
            delta_to_best = st.slider("Delta to Session Best Lap (s)", 0.0, 10.0, 2.0)
            rolling_avg = st.slider("Rolling Lap Average (s)", 80.0, 150.0, 90.0)

            submit = st.form_submit_button("Predict Lap Time")

        if submit:
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
            st.success(f"🏎️ Predicted Lap Time: **{prediction:.3f} seconds**")

            # Historical stats
            st.subheader("📊 Historical Lap Summary")
            driver_id = driver_to_id[driver_name]
            driver_laps = lap_data[lap_data["DriverID"] == driver_id]
            st.metric("Best Lap", f"{driver_laps['LapTimeSeconds'].min():.3f} sec")
            st.metric("Avg Lap", f"{driver_laps['LapTimeSeconds'].mean():.3f} sec")
            st.metric("Consistency (Std Dev)", f"{driver_laps['LapTimeSeconds'].std():.3f} sec")
            st.metric("Stint Count", f"{driver_laps['StintNorm'].nunique()}")

            # Feature importance chart
            st.subheader("Feature Importance")
            fig, ax = plt.subplots()
            importance = model.feature_importances_
            sorted_idx = np.argsort(importance)
            ax.barh(input_data.columns[sorted_idx], importance[sorted_idx])
            st.pyplot(fig)

    # TAB 2: Compare Drivers
    with tabs[1]:
        st.markdown("Compare two drivers side by side using average and best lap time.")

        col1, col2 = st.columns(2)
        with col1:
            driver_1 = st.selectbox("Driver 1", driver_names, key="d1")
        with col2:
            driver_2 = st.selectbox("Driver 2", driver_names, key="d2")

        if driver_1 == driver_2:
            st.warning("Please select two different drivers to compare.")
        else:
            d1_id = driver_to_id[driver_1]
            d2_id = driver_to_id[driver_2]

            d1_data = lap_data[lap_data["DriverID"] == d1_id]
            d2_data = lap_data[lap_data["DriverID"] == d2_id]

            st.subheader("📊 Lap Time Comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{driver_1}**")
                st.metric("Best Lap", f"{d1_data['LapTimeSeconds'].min():.3f} sec")
                st.metric("Avg Lap", f"{d1_data['LapTimeSeconds'].mean():.3f} sec")
            with col2:
                st.markdown(f"**{driver_2}**")
                st.metric("Best Lap", f"{d2_data['LapTimeSeconds'].min():.3f} sec")
                st.metric("Avg Lap", f"{d2_data['LapTimeSeconds'].mean():.3f} sec")

            st.subheader("📉 Visual Comparison")
            comp_df = pd.DataFrame({
                "Driver": [driver_1, driver_2],
                "Best Lap (s)": [d1_data["LapTimeSeconds"].min(), d2_data["LapTimeSeconds"].min()],
                "Avg Lap (s)": [d1_data["LapTimeSeconds"].mean(), d2_data["LapTimeSeconds"].mean()],
            })
            chart_data = comp_df.set_index("Driver")
            st.bar_chart(chart_data)

if __name__ == "__main__":
    main()
