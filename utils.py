# utils.py – Helper functions
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load processed lap data
def load_lap_data():
    return pd.read_csv("data/processed_lap_data.csv")

# Plot feature importance
def show_feature_importance(model, input_data):
    fig, ax = plt.subplots()
    importance = model.feature_importances_
    sorted_idx = importance.argsort()
    ax.barh(input_data.columns[sorted_idx], importance[sorted_idx])
    ax.set_xlabel("Feature Importance")
    st.pyplot(fig)
