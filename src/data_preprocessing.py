from src.utils import logger
from src.utils import load_config
import pandas as pd
import numpy as np

config = load_config()
cols_to_keep = config["columns"]["cols_to_keep"]
delay_cols = config["columns"]["delay_cols"]

def load_data(path):
    df = pd.read_csv(path)
    return df

def drop_unnamed(df):
    return df.loc[:, ~df.columns.str.startswith("Unnamed")]

def drop_unwanted_cols(df, cols_to_keep):
    existing_cols_to_keep = [col for col in cols_to_keep if col in df.columns]
    df = df[existing_cols_to_keep].copy()
    return df

def process_date(df):
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"]) 
    df["MONTH"] = df["FL_DATE"].dt.month
    df["DAY_OF_WEEK"] = df["FL_DATE"].dt.dayofweek
    df = df.drop(columns = ["FL_DATE"])
    return df

def process_time(df):
    df["DEP_HOUR"] = df["CRS_DEP_TIME"]//100
    df = df.drop(columns = ["CRS_DEP_TIME"])
    return df

def handle_missing_values(df, delay_cols):
    if "DEP_DELAY" in df.columns:
        df = df.dropna(subset = ["DEP_DELAY"])
    existing_delay_cols = [col for col in delay_cols if col in df.columns]
    
    if existing_delay_cols:
        df[existing_delay_cols] = df[existing_delay_cols].fillna(0)

    return df

def clean_dataset(df, cols_to_keep, delay_cols):
    df = drop_unnamed(df)
    df = drop_unwanted_cols(df, cols_to_keep)
    df = process_date(df)
    df = process_time(df)
    df = handle_missing_values(df, delay_cols)
    return df

def preprocessing_pipeline(path, cols_to_keep, delay_cols):
    logger.info("Starting Preprocessing")
    df = load_data(path)
    logger.info(f"Dataset loaded, Shape: {df.shape}")
    df = clean_dataset(df, cols_to_keep, delay_cols)
    logger.info(f"Dataset cleaned, Shape: {df.shape}")
    logger.info("Preprocessing Completed")
    return df
