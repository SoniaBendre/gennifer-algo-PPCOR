import os
import pandas as pd

import ppcor

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data')

def generateInputs(dataset_uri):
    inputExpr = pd.read_csv(os.path.join(DATASET_PATH, dataset_uri), header=0, index_col=0)
    geneNames = inputExpr.index.values
    inputExpr.index = geneNames

def run(inputExpre):
    network = pcor(x = np.transpose(inputExpr.values), method = "spearman")
    return network

def parseOutput(network):
    return network.to_json(orient='records')
