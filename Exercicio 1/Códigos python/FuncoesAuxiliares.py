#neste arquivo estão descritas todas as funções que serão utilizadas para auxiliar na produção do notebook para analise dos dados
import pandas as pd 
import sklearn 
import functools
import xlrd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
def getDataframeInSpecificFormat(datasetPath):
    availabelFormats = ['csv','xslx','txt']
    datasetDataFrame = None
    if (availabelFormats[0] in datasetPath):
        datasetDataFrame = pd.read_csv(datasetPath)

    elif (availabelFormats[1] in datasetPath):
        datasetDataFrame = pd.read_excel(datasetPath)
    
    elif (availabelFormats[2] in datasetPath):
        datasetDataFrame = pd.read_csv(datasetPath)
    
    else:
        print('Formato: ' + format + ' desconhedio, formatos disponiveis:')
        stringOfFormats = functools.reduce(lambda element1,element2: element1 + ' ' + element2,availabelFormats)
        print(stringOfFormats)
    return datasetDataFrame

def saveDescriptionOfEachColumn(datasetPath,pathToSaveTable,tableName):
    datasetDataFrame = getDataframeInSpecificFormat(datasetPath)
    datasetColumns = datasetDataFrame.columns
    describedDataFrame = pd.DataFrame(columns = None)
    for column in datasetColumns:
        describedDataFrame[column] = datasetDataFrame[column].describe()
    describedDataFrame.to_excel(pathToSaveTable+tableName)

def getOccurencesOfMissingValuesByColumns(datasetDataFrame):
    dicOfMissingValues = {}
    sizeOfData = len(datasetDataFrame.index)
    for column in datasetDataFrame.columns:
        dicOfMissingValues[column] = list(datasetDataFrame[column]).count("?")*100/sizeOfData
    return(dicOfMissingValues)

def removeColumnsWithMissingValues(datasetDataFrame):
    dicOfMissingValues = getOccurencesOfMissingValuesByColumns(datasetDataFrame)
    columnsToRemove = [key for key,val  in dicOfMissingValues.items() if val > 0 ]
    datasetDataFrameWithoutColumnsWithMissingValues = datasetDataFrame.drop(columns = columnsToRemove)
    return datasetDataFrameWithoutColumnsWithMissingValues

def printOccurencesAndPercentagesOfMissingValuesByColumns(datasetPath):    
    datasetDataFrame = getDataframeInSpecificFormat(datasetPath)
    dicOfMissingValues = getOccurencesOfMissingValuesByColumns(datasetDataFrame)
    print("Porcentagem de '?' em cada coluna ")
    for key,val in  dicOfMissingValues.items(): 
        print('{key} - {val:.2f}'.format(key = key, val = val))

def removeLinesWithMissingValues(datasetDataFrame):
    linesToBeRemoved = []
    for index, row in datasetDataFrame.iterrows():
        if '?' in list(row):
            linesToBeRemoved.append(index)
    datasetDataFrameWithMissingLines = datasetDataFrame.drop(linesToBeRemoved)
    return datasetDataFrameWithMissingLines

def getCorrelationInDataframe(datasetDataFrame,outputName):
    dummiesDataFrame = pd.get_dummies(datasetDataFrame)
    cor = dummiesDataFrame.corr()
    cor_target = abs(cor[outputName]).sort_values(ascending=False)
    return cor_target[1:]

def getMostCorrelatedColumns(datasetDataFrame,outputName,numberOfVariables):
    cor_target =  getCorrelationInDataframe(datasetDataFrame,outputName)
    columnsNames = list(cor_target.keys()[:numberOfVariables])
    print (columnsNames)
    return columnsNames

def getCorrelatedDataFrame(datasetDataFrame,outputName,numberOfVariables):
    cor_target =  getCorrelationInDataframe(datasetDataFrame,outputName)
    columnsNames = list(cor_target.keys()[numberOfVariables:])
    return datasetDataFrame.drop(columns = columnsNames)

def saveCorrelationImage(datasetDataFrame,folderPath,imageName,outputName,numberOfVariables):
    dummiesDataFrame = pd.get_dummies(datasetDataFrame)
    cor_target =  getCorrelationInDataframe(datasetDataFrame,outputName)
    columnsNamesToBeRemoved = list(cor_target.keys()[numberOfVariables:])
    correlatedDataFrame = dummiesDataFrame.drop(columns = columnsNamesToBeRemoved)

    plt.figure(figsize=(20,20))
    cor = correlatedDataFrame.corr()
    sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
    # sns.heatmap(cor, annot=True, cmap=plt.cm.Reds,xticklabels=columns, yticklabels=columns)
    plt.savefig(folderPath+imageName)

def prepareDatasetforTraining(datasetDataFrame):
    dummiesDataFrame = pd.get_dummies(datasetDataFrame)
    for col in dummiesDataFrame.columns: 
        print(col)