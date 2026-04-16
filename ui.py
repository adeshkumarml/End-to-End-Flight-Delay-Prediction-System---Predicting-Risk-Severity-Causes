import streamlit as st
import requests
from src.utils import load_config

config = load_config("config/ui_config.yaml")
airlines = config["ui"]["airlines"]

st.set_page_config(page_title = "Flight Delay Predictor", layout = "centered")

st.title("PRE-DEPARTURE FLIGHT DELAY PREDICTION")
st.markdown("Predict risk of flight delays and its severity and possible causes.")
st.subheader("Enter Your Flight Details")

col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("AIRLINE", airlines)
    date = st.date_input("FLIGHT DATE")
    formatted_date = date.strftime("%y/%m/%d")

with col2:
    colA, colB = st.columns(2)
    with colA:
        origin = st.text_input("ORIGIN", help = "Enter Departure Airport IATA Code.")
    with colB:
        dest = st.text_input("DESTINATION", help = "Enter Arrival Airport IATA Code.")
    
    dep_time = st.number_input("DEPARTURE TIME (HHMM)", min_value = 0, max_value = 2359, step = 100)

if st.button("PREDICT"):
    input_data = {
        "AIRLINE": airline,
        "ORIGIN": origin,
        "DEST": dest,
        "FL_DATE": formatted_date,
        "CRS_DEP_TIME": dep_time
    }
    
    with st.spinner("Predicting..."):
        try:
            response = requests.post("https://flight-delay-risk-severity-and-cause-api.onrender.com/predict", json = input_data)
            if response.status_code == 200:
                result = response.json()

                st.subheader("Prediction Results")
                if "Low delay risk" in result["risk"]:
                    st.success("LOW DELAY RISK")
                    st.success("No significant delay is predicted!")

                else:
                    st.error("HIGH DELAY RISK")
                    st.error(f"Delay Severity: {result['severity']}")

        #           st.subheader("Possible Causes")
        #           cause_map = config["ui"]["cause_map"]

        #           for cause, prob in result["top_causes"]:
        #                ui_cause = cause_map.get(cause)
        #                percent = int(prob * 100)

        #                st.write(f"{ui_cause} ({percent}%)")
        #                st.progress(percent)
            else:
                st.error("API Error!")
        
        except Exception as e:
            st.error(e)
