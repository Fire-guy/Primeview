
import pandas as pd
import pickle
from lightfm import LightFM
from scipy.sparse import coo_matrix
import os

DATA_PATH = "data/interactions.csv"
MODEL_PATH = "models/lightfm_model.pkl"

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found!")
    df = pd.read_csv(DATA_PATH)
    if not {'user_id', 'item_id', 'event_type'}.issubset(df.columns):
        raise ValueError("CSV must have columns: user_id, item_id, event_type")
    return df

def build_interaction_matrix(df):
    # Map IDs to sequential indices
    user_mapping = {u: i for i, u in enumerate(df['user_id'].unique())}
    item_mapping = {i: j for j, i in enumerate(df['item_id'].unique())}

    df['user_index'] = df['user_id'].map(user_mapping)
    df['item_index'] = df['item_id'].map(item_mapping)

    # Simple implicit feedback: view/click → 1
    df['interaction'] = 1  

    return coo_matrix(
        (df['interaction'], (df['user_index'], df['item_index'])),
        shape=(len(user_mapping), len(item_mapping))
    ), user_mapping, item_mapping

def train_model(interactions):
    model = LightFM(loss='warp')
    model.fit(interactions, epochs=10, num_threads=2)
    return model

if __name__ == "__main__":
    df = load_data()
    interactions, user_mapping, item_mapping = build_interaction_matrix(df)
    model = train_model(interactions)

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({
            "model": model,
            "user_mapping": user_mapping,
            "item_mapping": item_mapping
        }, f)

    print(f"✅ Model saved to {MODEL_PATH}")
