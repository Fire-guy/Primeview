from fastapi import FastAPI
import pickle

app=FastAPI()

@app.get("/recommend/{user_id}")
def recommend(user_id:int):
    with open("models/lightfm_model.pkl","rb") as f:
        model=pickle.load(f)
    return {"user_id":user_id,"recommendations":["ItemA","ItemB"]}
