import pickle
import asyncio
import aiohttp
import traceback
import logging
import numpy as np
from fastapi import FastAPI, Response
from pydantic import BaseModel
from tensorflow.keras import models # type: ignore
from utils.layers import TransformerEncoder, PositionalEmbedding
from spektral.layers import GCNConv, GlobalSumPool
from utils.data_preprocessing import transform_url, parse_html, create_graph
from utils.data_preprocessing import create_graph_adjacency, create_graph_feature

# Config logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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

async def is_pdf_website(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            return 'application/pdf' in content_type.lower()

async def fetch_url(url, timeout=5):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            html = await response.text()

            return {'url': str(response.url), 'html': html}

@app.post('/predict')
async def predict(input_data: PredictionInput, response: Response):
    try:
        is_pdf = await is_pdf_website(input_data.url)
        if is_pdf:
            return {
                'phishing_probability': 0,
                'message': 'Successfully.'
            }
        
        result = await fetch_url(input_data.url, timeout=10)
                    
        max_word = 50
        max_node = 400
        feature_dim = 3

        with open('models/dictionary.pkl', 'rb') as f:
            dictionary = pickle.load(f)
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

        return {
            'phishing_probability': probability,
            'message': 'Successfully.'
        }
    except asyncio.TimeoutError as e:
        response.status_code = 408
        return {
            'phishing_probability': -1,
            'message': 'Timeout error when fetch url.'
        }
    except aiohttp.ClientError as e:
        response.status_code = 400
        return {
            'phishing_probability': -1,
            'message': f'HTTP error occurred: {str(e)}'
        }
    except Exception as e:
        response.status_code = 500
        error_trace = traceback.format_exc()
        print(error_trace)
        logging.error(f"Unexpected error: {error_trace}")
        return {
            'phishing_probability': -1,
            'message': 'An unexpected error occurred.'
        }