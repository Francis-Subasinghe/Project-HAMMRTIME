# main.py – Streamlit UI
import streamlit as st
from predictor import predict_lap_time
from config import driver_names, driver_team_map, tire_types, driver_to_id, team_to_id, tire_to_id
from utils import load_lap_data, show_feature_importance
import pandas as pd

lap_data = load_lap_data()

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
        prediction, input_data, model = predict_lap_time(
            driver_name, team, tire, stint_norm, lap_trend, time_sec,
            pace_dev, delta_to_best, rolling_avg
        )

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
        show_feature_importance(model, input_data)

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
