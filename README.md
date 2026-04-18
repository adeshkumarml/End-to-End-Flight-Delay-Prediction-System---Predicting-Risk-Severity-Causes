# Flight-Delay-Prediction-System---Predicting-Risk-Severity-Causes
Predict flight delay risk and severity using pre-departure data.

## Demo
Access the system *(v1)* from here: https://aksflightdelayrisksevcausespred.streamlit.app/<br>
Acess the API docs from here: https://flight-delay-risk-severity-and-cause-api.onrender.com/docs<br>

[Demo Video](https://drive.google.com/file/d/1nLu3uoZ0IDv9W7_PU5YtK6HnIDEhmhJo/view?usp=sharing)  


## Overview
An end-to-end machine learning system to predict possible flight delays from pre-departure data. The system predicts the following:
- Risk of delay (High risk/ Low risk)
- Severity if there is a high risk of delay (Major delay/ Minor delay)<br>
The system is deployed with a real-time inference API and a simple and minimal interactive UI.

## Features
- Pre-departure delay risk prediction
- Severity classification when the delay is high risk
- Real-time inference via API
- Interactive Streamlit UI

## Tech-Stack
The following have been used:
- ML Models: XGBoost and Scikit-learn
- Backend: FastAPI
- Frontend: Streamlit
- Deployment: Render, Streamlit Cloud

## General Architecture
User input ➡️ Streamlit UI ➡️ FastAPI ➡️ Models ➡️ Output

## Project Structure
*app.py*: FastAPI backend code<br>
*ui.py* : Streamlit UI code<br>
*src* : Prediction pipeline<br>
*config* : Configuration files<br>
*setup.sh* : Script to download model artifacts<br>
*requirements.txt* : Required libraries

## Deployment Note
The system is originally designed to perform three tasks:
- Risks prediction, 
- Severity classification, and
- Cause classification.<br>
However, the cause classification task model (Random Forests) has been excluded from this currently deployed version of this system due to memory constraints on the free tier of Render.<br> 
The complete development repository containing all models, complete training and prediction pipelines, and experiments can be found here: https://github.com/adeshkumarml/End-to-End-Flight-Delay-Prediction-System---Development-Repo. 