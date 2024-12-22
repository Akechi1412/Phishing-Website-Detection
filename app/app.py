import socket
import pickle
import asyncio
import aiohttp
import traceback
import logging
import numpy as np
from fastapi import FastAPI, Response
from pydantic import BaseModel
from tensorflow.keras import models # type: ignore
from utils.layers import TransformerEncoder, PositionalEmbedding, GCN
from spektral.layers import GCNConv, GlobalSumPool
from utils.data_preprocessing import vectorize_url, parse_html, create_graph
from utils.data_preprocessing import create_graph_adjacency, create_graph_feature
from logging.handlers import RotatingFileHandler
from fastapi.middleware.cors import CORSMiddleware

handler = RotatingFileHandler(
    'app.log', maxBytes=5*1024*1024, backupCount=5
)
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)

app = FastAPI()

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

if local_ip.startswith('127.') \
   or local_ip.startswith('192.168.') \
   or hostname == 'localhost':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

model = models.load_model(
    'models/best_model.h5',
    custom_objects={'TransformerEncoder': TransformerEncoder,
                    'PositionalEmbedding': PositionalEmbedding,
                    'GCNConv': GCNConv,
                    'GlobalSumPool': GlobalSumPool,
                    'GCN': GCN})

class PredictionInput(BaseModel):
    url: str

@app.get('/')
async def welcome():
    return {'message': 'Welcome!'}

async def fetch_url(url, timeout=5):
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            html = None
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' in content_type.lower():
                html = await response.text()
            print(response.url)

            return {'url': str(response.url), 'html': html}

@app.post('/predict')
async def predict(input_data: PredictionInput, response: Response):
    try:      
        result = await fetch_url(input_data.url, timeout=5)
        if not result['html']:
            return {
                'phishing_probability': -1,
                'message': 'Successfully.'
            } 
                    
        max_words = 50
        max_nodes = 600
        feature_dim = 3

        with open('models/dictionary.pkl', 'rb') as f:
            dictionary = pickle.load(f)
        url_input = vectorize_url(result['url'].strip().rstrip('/'), 
                                  dictionary=dictionary, 
                                  max_words=max_words)
        html_dom = parse_html(result['html'])
        html_graph = create_graph(html_dom)
        adjacency_input = create_graph_adjacency(html_graph, max_nodes=max_nodes)
        feature_input = create_graph_feature(html_graph, max_nodes=max_nodes)

        url_input = np.array(url_input).reshape(1, max_words)
        adjacency_input = np.array(adjacency_input).reshape(1, max_nodes, max_nodes)
        feature_input = np.array(feature_input).reshape(1, max_nodes, feature_dim)

        y_pred_prob = model.predict([url_input, adjacency_input, feature_input])
        probability = round(float(y_pred_prob[0]), 2)

        return {
            'phishing_probability': probability,
            'message': 'Successfully.'
        }
    except asyncio.TimeoutError as e:
        response.status_code = 408
        error_message = 'Timeout error when fetching URL.'
        logging.error(f'{error_message} URL: {input_data.url} - Error: {e}')
        return {
            'phishing_probability': -1,
            'message': error_message
        }
    except aiohttp.ClientError as e:
        response.status_code = 400
        error_message = f'HTTP error occurred: {str(e)}'
        logging.error(f'{error_message} URL: {input_data.url} - Error: {e}')
        return {
            'phishing_probability': -1,
            'message': error_message
        }
    except Exception as e:
        response.status_code = 500
        error_trace = traceback.format_exc()
        logging.error(f'Unexpected error: {error_trace}')
        return {
            'phishing_probability': -1,
            'message': 'An unexpected error occurred.'
        }