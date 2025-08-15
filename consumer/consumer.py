import asyncio
import json
import pickle
import os
from aiokafka import AIOKafkaConsumer
import pandas as pd
from lightfm import LightFM
from scipy.sparse import coo_matrix


MODEL_PATH="models/lightfm_model.pkl"

BATCH_SIZE=5

interactions=[]

async def consume():
    consumer = AIOKafkaConsumer(
        'user_events',
        bootstrap_servers='localhost:9092',
        group_id="recommendation_group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    print("Kafka consumer started. Listening for events...")

    try:
        while True:
            msg = await consumer.getone()
            event = json.loads(msg.value.decode())
            print(f"Received event: {event}",event)
            interactions.append(event)
            
            if len(interactions)>=BATCH_SIZE:
                print(f"Training model on {len(interactions)} events...")
                train_ans_save_model(interactions)
                interactions.clear()
    finally:
        await consumer.stop()

def train_and_save_model(events):
    df=pd.DataFrame(events)
    if df.empty():
        print("No data found")
        return
    
    df['user_idx']=df['user_id'].astype('category').cat.codes
    df['item_idx']=df['item_id'].astype('category').cat.codes

    mat=coo_matrix(
        (1,(df['user_idx'],df['item_idx']))
    )

    model=LightFM(loss='warp')
    model.fit(mat,epochs=10,num_threads=2)

    os.makedirs(os.path.dirname(MODEL_PATH),exist_ok=True)
    with open(MODEL_PATH,"wb") as f:
        pickle.dump({
            "model":model,
            "user_mappings":dict(enumerate(df['user_id'].astype("category").cat.categories)),
            "item_mappings":dict(enumerate(df['item_id'].astype('category').cat.categories))
        },f)
    print(f"Model trained and saved in {MODEL_PATH}")

if __name__ == "__main__":
    asyncio.run(consume())
