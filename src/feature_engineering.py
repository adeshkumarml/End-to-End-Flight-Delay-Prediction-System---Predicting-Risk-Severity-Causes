from src.utils import logger
from src.utils import load_config
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

config = load_config()
delay_cols = config["columns"]["delay_cols"]
freq_cols = config["columns"]["freq_cols"]
ohe_cols = config["columns"]["ohe_cols"]

def create_targets(df):
    logger.info("Creating targets for Delay Risk and Severity")
    df["DELAY_RISK"] = (df["DEP_DELAY"] > 15).astype(int)
    def classify_severity(delay):
        if(delay <= 15):
            return 0
        elif(delay <= 60):
            return 1
        else:
            return 2
    df["SEVERITY"] = df["DEP_DELAY"].apply(classify_severity)
    return df

def create_cause_column(df):
    logger.info("Creating cause column")
    df_cause = df[df[delay_cols].sum(axis = 1) > 0].copy()
    df_cause["CAUSE"] = df_cause[delay_cols].idxmax(axis = 1)
    return df_cause

def encode_cause(df_cause):
    logger.info("Label encoding causes")
    le = LabelEncoder()
    df_cause["CAUSE"] = le.fit_transform(df_cause["CAUSE"])
    return df_cause, le

def apply_frequency_encode(df, col):
    logger.info(f"Frequency encoding {col}")
    freq_map = df[col].value_counts(normalize = True)
    df[f"{col}_FREQ"] = df[col].map(freq_map).fillna(0)
    return df, freq_map

def encode_features(df, freq_cols):
    freq_maps = {}
    for col in freq_cols:
        df, freq_map = apply_frequency_encode(df, col)
        freq_maps[col] = freq_map
    logger.info("Feature encoding completed")
    return df, freq_maps

def apply_ohe(df, ohe_cols):
    logger.info(f"One-hot encoding {ohe_cols}")
    ohe = OneHotEncoder(handle_unknown = "ignore", sparse_output = False)
    encoded = ohe.fit_transform(df[ohe_cols])
    encoded_df = pd.DataFrame(encoded, 
                              columns = ohe.get_feature_names_out(ohe_cols),
                              index = df.index)
    df = pd.concat([df, encoded_df], axis = 1)
    df = df.drop(ohe_cols, axis = 1)
    return df, ohe

def prep_risk_dataset(df):
    logger.info("Preparing risk dataset")
    X = df.drop(["DEP_DELAY", "DELAY_RISK", "SEVERITY"] + freq_cols + delay_cols, axis = 1, errors = "ignore")
    y = df["DELAY_RISK"]
    return X, y

def prep_severity_dataset(df):
    logger.info("Preparing severity dataset")
    X = df.drop(["DEP_DELAY", "DELAY_RISK", "SEVERITY"] + freq_cols + delay_cols, axis = 1, errors = "ignore")
    y = df["SEVERITY"]
    return X, y

def prep_cause_dataset(df):
    logger.info("Preparing cause dataset")
    df_cause = create_cause_column(df)
    df_cause, cause_map = encode_cause(df_cause)
    X = df_cause.drop(["DEP_DELAY", "DELAY_RISK", "SEVERITY", "CAUSE"] + delay_cols + freq_cols, axis = 1, errors = "ignore")
    y = df_cause["CAUSE"]
    return X, y, cause_map

def split_data(X, y, test_size = 0.2, stratify = None, random_state = 42):
    logger.info("Performing train and test split")
    return train_test_split(X, y, test_size = test_size, stratify = stratify, random_state = random_state)



