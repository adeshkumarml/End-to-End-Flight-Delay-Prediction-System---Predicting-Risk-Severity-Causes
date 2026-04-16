import joblib
import pandas as pd
from src.utils import logger, load_config
from src.data_preprocessing import preprocessing_pipeline, clean_dataset

config = load_config()
freq_cols = config["columns"]["freq_cols"]
ohe_cols = config["columns"]["ohe_cols"]

risk_model = joblib.load("models/final/risk_model_v1.pkl")
severity_model = joblib.load("models/final/severity_model.pkl")
cause_model = joblib.load("models/final/cause_model.pkl")
risk_threshold = joblib.load("models/final/risk_threshold.pkl")
freq_maps = joblib.load("models/final/freq_maps.pkl")
ohe = joblib.load("models/final/ohe.pkl")
le = joblib.load("models/final/le.pkl")
feature_space = joblib.load("models/final/feature_space.pkl")
logger.info("All artifacts loaded")

def predict_from_df(df):
    logger.info("Prediction pipeline starting")
    for col in freq_cols:
        df[f"{col}_FREQ"] = df[col].map(freq_maps[col]).fillna(0)
    
    ohe_transformed = ohe.transform(df[ohe_cols])
    ohe_df = pd.DataFrame(ohe_transformed, columns = ohe.get_feature_names_out(ohe_cols), index = df.index)
    df = df.drop(columns = ohe_cols)
    df = pd.concat([df, ohe_df], axis = 1)
    logger.info("Encoding done")
    
    df = df.drop(config["columns"]["delay_cols"], axis = 1, errors = "ignore")
    df = df.drop(["DEP_DELAY"], axis = 1, errors = "ignore")
    df = df.reindex(columns = feature_space, fill_value = 0)

    risk_probs = risk_model.predict_proba(df)[:,1]
    risk_preds = (risk_probs >= risk_threshold).astype(int)
    logger.info("Risk predicted")

    severity_preds = severity_model.predict(df)
    logger.info("Severity predicted")

    cause_probs = cause_model.predict_proba(df)
    top_three_idx = cause_probs.argsort(axis = 1)[:,-3:][:,::-1]
    top_three_causes = []
    for i, row in enumerate(top_three_idx):
        labels = le.inverse_transform(row.flatten())
        probs = cause_probs[i][row]
        result = list(zip(labels, probs))
        top_three_causes.append(result)
    logger.info("Cause predicted")

    risk_map = config["mappings"]["risk"]
    severity_map = config["mappings"]["severity"]
    results = []

    for i in range(len(df)):
        risk = risk_preds[i]
        if risk == 0:
            result = {"risk": risk_map[risk], 
                      "severity": "No Delay", 
                      "top_causes": []}
        else:
            severity = severity_map[severity_preds[i]]
            causes = [(label, round(prob, 2)) for label, prob in top_three_causes[i]]
            result =  {"risk" : risk_map[risk],
                       "severity" : severity,
                       "top_causes" : causes}
        results.append(result)
    logger.info("Returning consoliated predictions")
    return results

def predict_batch(data_path):
    logger.info("Prediction pipeline starting")
    df = preprocessing_pipeline(data_path, config["columns"]["cols_to_keep"], config["columns"]["delay_cols"])
    logger.info("Data loaded and preprocessing done")
    return predict_from_df(df)

def predict_api(input_dict):
    df = pd.DataFrame([input_dict])
    df = clean_dataset(df, config["columns"]["cols_to_keep"], config["columns"]["delay_cols"])
    results = predict_from_df(df)
    return results[0]

if __name__ == "__main__":
    path = "data/inference/APICheck.csv"
    df_in = pd.read_csv(path)
    results = predict_batch(path)
    df_results = pd.DataFrame(results)
    df_out = pd.concat([df_in, df_results], axis = 1)
    df_out.to_csv("outputs/APIOut.csv", index = False)
    print("Predictions saved at outputs/APIOut.csv")

