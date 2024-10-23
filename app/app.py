import pickle
import aiohttp
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from tensorflow.keras import models # type: ignore
from utils.layers import TransformerEncoder, PositionalEmbedding
from spektral.layers import GCNConv, GlobalSumPool
from utils.data_collecting import fetch_url_data
from utils.data_preprocessing import transform_url, parse_html, create_graph
from utils.data_preprocessing import create_graph_adjacency, create_graph_feature

app = FastAPI()

model = models.load_model(
    'models/best_model.h5',
    custom_objects={'TransformerEncoder': TransformerEncoder,
                    'PositionalEmbedding': PositionalEmbedding,
                    'GCNConv': GCNConv,
                    'GlobalSumPool': GlobalSumPool})

class PredictionInput(BaseModel):
    url: str

@app.get('/')
async def welcome():
    return {'message': 'Welcome!'}

@app.post('/predict')
async def predict(input_data: PredictionInput):
    try:
        async with aiohttp.ClientSession() as session:
            result = await fetch_url_data(session, input_data.url, timeout=5)
            
            if result is None:
                return {
                    'phishing_probability': -1,
                    'message': "The URL cannot be accessed."
                }
            
        max_word = 50
        max_node = 400
        feature_dim = 3

        with open('models/dictionary.pkl', 'rb') as f:
            dictionary = pickle.load(f, encoding='utf-8')
        url_input = transform_url(result['url'], dictionary=dictionary, max_word=max_word)
        html_dom = parse_html(result['html'])
        html_graph = create_graph(html_dom)
        adjacency_input = create_graph_adjacency(html_graph, max_node=max_node)
        feature_input = create_graph_feature(html_graph, max_node=max_node)

        url_input = np.array(url_input).reshape(1, max_word)
        adjacency_input = np.array(adjacency_input).reshape(1, max_node, max_node)
        feature_input = np.array(feature_input).reshape(1, max_node, feature_dim)

        y_pred_prob = model.predict([url_input, adjacency_input, feature_input])
        probability = round(float(y_pred_prob[0]), 2)
    except Exception as e:
        return {
            'phishing_probability': -2,
            'message': str(e),
        }

    return {
        'phishing_probability': probability,
        'message': 'Successfully.'
        }