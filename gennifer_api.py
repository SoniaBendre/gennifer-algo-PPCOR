import os
import pandas as pd
import uuid
import json
from pathlib import Path

DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data/GSD')

def generateInputs(dataset_uri):
    if not os.path.join(DATASET_PATH, dataset_uri).exists():
        print("Input folder for PPCOR does not exist, creating input folder...")
        os.path.join(DATASET_PATH, dataset_uri).mkdir(exist_ok = False)

    if not os.path.join(DATASET_PATH, dataset_uri, "ExpressionData.csv").exists():
        print(f"{dataset_uri} does not exist at path")    

    ExpressionData = pd.read_csv(os.path.join(DATASET_PATH, dataset_uri, "ExpressionData.csv"), header=0, index_col=0)
        
    newExpressionData = ExpressionData.copy()
    newExpressionDataPath = os.path.join("/tmp", "newExpressionData.csv")
    newExpressionData.to_csv(newExpressionDataPath, sep = ',', header  = True, index = True)

    return newExpressionDataPath

def run(newExpressionDataPath):
    '''
    Function to run PPCOR algorithm
    '''
    inputPath = newExpressionDataPath
    # make output dirs if they do not exist:
    outDir =  os.path.join("/tmp") + str(uuid.uuid4())
    os.makedirs(outDir, exist_ok = True)
    
    outPath = str(outDir) + 'outFile.txt'

    cmdToRun = ' '.join(['Rscript runPPCOR.R', inputPath, outPath])
    print(cmdToRun)
    os.system(cmdToRun)
    return outPath


def parseOutput(outPath, pVal=0.05):
    '''
    Function to parse outputs from PPCOR.
    '''
    # Read output
    OutDF = pd.read_csv(outPath, sep = '\t', header = 0)
    # edges with significant p-value
    part1 = OutDF.loc[OutDF['pValue'] <= float(pVal)]
    part1 = part1.assign(absCorVal = part1['corVal'].abs())
    # edges without significant p-value
    part2 = OutDF.loc[OutDF['pValue'] > float(pVal)]
    
    # outFile = open(outDir + 'rankedEdges.csv','w')
    # outFile.write('Gene1'+'\t'+'Gene2'+'\t'+'EdgeWeight'+'\n')

    results = {'Gene1': [], 
               'Gene2': [],
               'EdgeWeight': []}

    for idx, row in part1.sort_values('absCorVal', ascending = False).iterrows():
        results['Gene1'].append(row['Gene1'])
        results['Gene1'].append(row['Gene2'])
        results['Gene1'].append(str(row['corVal']))

    
    for idx, row in part2.iterrows():
        results['Gene2'].append(row['Gene1'])
        results['Gene2'].append(row['Gene2'])
        results['EdgeWeight'].append(str(0))

    return json.dumps(results)
    