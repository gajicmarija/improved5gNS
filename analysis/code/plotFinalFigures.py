import sys
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import sklearn
import pandas as pd
import matplotlib
import glob
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import seaborn as sns
import math
from collections import OrderedDict
import statistics
from scipy import stats
from sklearn.model_selection import train_test_split
from matplotlib.colors import LogNorm, Normalize
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from matplotlib.transforms import Affine2D
from matplotlib.patches import Rectangle
import scipy.stats
import matplotlib.colors as mcolors
from matplotlib.ticker import MultipleLocator


import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
print(parentdir)
sys.path.insert(0,parentdir) 
from algorithm import algorithm as algo

font = {'weight' : 'normal',
        'size'   : 40}

matplotlib.rc('font', **font)
matplotlib.rc('lines', linewidth=2.0)
matplotlib.rc('lines', markersize=8)

downlink = ['Downlink', 'rxPkOk:vector(packetBytes)']
uplink = ['Uplink', 'txPk:vector(packetBytes)']
maxSimTime = 400

globalCounter = 0

def partialCDFBegin(numSubplots):
    fig, ax = plt.subplots(numSubplots, figsize=(16,12*numSubplots))
    return fig, ax

def partialCDFPlotData(fig, ax, data, label, lineType, lineColor):
    sorted_data = np.sort(data)
    linspaced = np.linspace(0, 1, len(data), endpoint=True)
    ax.plot(sorted_data, linspaced, lineType, label=label, color=lineColor)

def partialCDFPlotDataNoColor(fig, ax, data, label, lineType):
    sorted_data = np.sort(data)
    linspaced = np.linspace(0, 1, len(data), endpoint=True)
    ax.plot(sorted_data, linspaced, lineType, label=label)

def partialCDFEnd(fig, ax, title, xLabel, outPath):
    try:
        iterator = iter(ax)
    except TypeError:
        ax.set_ylim(0,1.1)
        ax.grid(True)
    else:
        for axs in ax:
            axs.set_ylim(0,1.1)
            axs.grid(True)
    plt.legend()
    if title != '':
        plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel("CDF")
    fig.savefig(outPath, dpi=100, bbox_inches='tight')
    plt.close('all')

def partialCDFEndPNG(fig, ax, title, xLabel, outPath):
    try:
        iterator = iter(ax)
    except TypeError:
        ax.set_ylim(0,1.1)
        ax.grid(True)
    else:
        for axs in ax:
            axs.set_ylim(0,1.1)
            axs.grid(True)
    plt.legend()
    if title != '':
        plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel("CDF")
    fig.savefig(outPath, dpi=100, bbox_inches='tight', format='png')
    plt.close('all')

def makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit):
    scenName = str(testName) + '_' + str(numCLI)
    for nodeType,numNodesType in zip(nodeTypes, nodeSplit):
        scenName += '_' + nodeType.replace('host','') + str(numNodesType)
    return scenName
  

def makeNodeIdentifier(nodeType, nodeNum):
    if nodeNum < 0:
        return nodeType
    else:
        return nodeType + str(nodeNum)

def importDF(testName, numCLI, nodeTypes, nodeSplit, dataType):
    # File that will be read
    fullScenarioName = makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)
    file_to_read = '../exports/extracted/' + str(dataType) + '/' + fullScenarioName + '.csv'
    print("Results from run: " + file_to_read)
    # Read the CSV
    return pd.read_csv(file_to_read)

def importDFextended(testName, numCLI, nodeTypes, nodeSplit, dataType, extension):
    # File that will be read
    fullScenarioName = makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)
    print(fullScenarioName)
    file_to_read = '../exports/extracted/' + str(dataType) + '/' + fullScenarioName + extension + '.csv'
    #print("Results from run: " + file_to_read)
    # Read the CSV
    return pd.read_csv(file_to_read)

def filterDFType(df, filterType):
    return df.filter(like=filterType)

def chooseName(dataName):
    if dataName == 'hostVID':
        return 'VoD'
    elif dataName == 'hostFDO':
        return 'Download'
    elif dataName == 'hostSSH':
        return 'SSH'
    elif dataName == 'hostVIP':
        return 'VoIP'
    elif dataName == 'hostHVIP':
        return 'Crit VoIP'
    elif dataName == 'hostLVD':
        return 'Live Video'
    elif dataName == '2link0':
        return 'Bandwidth Slice'
    elif dataName == '2link1':
        return 'Delay Slice'
    elif dataName == '1link0':
        return 'Link'
    elif dataName == '3link0':
        return 'Bandwidth Slice'
    elif dataName == '3link1':
        return 'Delay Slice'
    elif dataName == '3link2':
        return 'Return Link'

colormap = plt.get_cmap('Set1').colors
print(colormap)
colorMapping = {
    'VID' : colormap[0],
    'LVD' : colormap[1], 
    'FDO' : colormap[2], 
    'SSH' : colormap[3], 
    'VIP' : colormap[4],
    'HVIP' : colormap[5],
    'all' : colormap[6]
}
def chooseColor(dataName):
    # if dataName == 'hostVID':
    #     return 'y'
    # elif dataName == 'hostFDO':
    #     return 'g'
    # elif dataName == 'hostSSH':
    #     return 'r'
    # elif dataName == 'hostVIP':
    #     return 'b'
    # if dataName == 'hostLVD':
    #     return 'm'
    if dataName == 'hostVID':
        return colorMapping['VID']
    elif dataName == 'hostFDO':
        return colorMapping['FDO']
    elif dataName == 'hostSSH':
        return colorMapping['SSH']
    elif dataName == 'hostVIP':
        return colorMapping['VIP']
    elif dataName == 'hostHVIP':
        return colorMapping['HVIP']
    if dataName == 'hostLVD':
        return colorMapping['LVD']
    elif dataName == '2link0':
        return 'c'
    elif dataName == '2link1':
        return 'm'
    elif dataName == '1link0':
        return 'k'
    elif dataName == '3link0':
        return 'c'
    elif dataName == '3link1':
        return 'm'
    elif dataName == '3link2':
        return 'k'

niceDataTypeName = {
    'DABL' : 'Buffer Length [s]',
    'DAMS' : 'MOS',
    'DAVB' : 'Requested Video Bitrate [kbps]',
    'DAVR' : 'Requested Video Resolution [p]',
    'DLVD' : 'Delay To Live Video Edge [s]',
    'Mos' : 'MOS',
    'RTT' : 'Round Trip Time [s]',
    'DAEB' : 'Estimated Bitrate [kbps]',
    'E2ED' : 'End to End Delay [s]',
    'PkLR' : 'Packet Loss Rate',
    'PlDel' : 'Playout Delay [s]',
    'PlLR' : 'Playout Loss Rate',
    'TDLR' : 'Taildrop Loss Rate',
    'rtt' : 'Round Trip Time [s]'
}

def plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                data = df[colName].dropna().tolist()
                if len(data) > 0:
                    tempValue.append(statistics.mean(data))
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                partialCDFPlotData(fig, ax1, tempValue, chooseName(nodeType), '-o', chooseColor(nodeType))
    if dataIdent == 'Mos':
        ax1.set_xlim(0.95,5.05)
    # else:
    #     ax1.set_xlim(0,1.01*maxValue)
    partialCDFEnd(fig,ax1,'', 'Mean Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_meanCdf' + dataIdent + str(nodeTypesToPlot) + '.pdf')
    partialCDFEndPNG(fig,ax1,'', 'Mean Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_meanCdf' + dataIdent + str(nodeTypesToPlot) + '.png')

minMaxQoE = {'hostFDO' : {'minMOS' : 1.0,
                            'maxMOS' : 5.0},
                'hostSSH' : {'minMOS' : 1.0,
                            'maxMOS' : 4.292851753999999},
                'hostVID' : {'minMOS' : 1.0,
                            'maxMOS' : 4.394885531954699},
                'hostVIP' : {'minMOS' : 1.0,
                            'maxMOS' : 4.5},
                'hostHVIP' : {'minMOS' : 1.0,
                            'maxMOS' : 4.5},
                'hostLVD' : {'minMOS' : 1.0,
                            'maxMOS' : 4.585703050898499}}

def normalizeQoE(cliType, mos):
    retMos = (mos - minMaxQoE[cliType]['minMOS'])*((5.0 - 1.0)/(minMaxQoE[cliType]['maxMOS'] - minMaxQoE[cliType]['minMOS'])) + 1.0
    return max(1.0, min(retMos, 5.0))

def getMeanDataTypeAppClass(testName, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot, sliceConfig):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, folderName)
    dfRtt = importDF(testName, numCLI, nodeTypes, nodeSplit, 'rtt')
    dfE2ed = importDF(testName, numCLI, nodeTypes, nodeSplit, 'endToEndDelay')
    meanMosFromExperiment = {}
    mosFairnessFromExperiment = {}
    minMosValFromExperiment = {}
    maxMosValFromExperiment = {}
    allData = []
    allDataRtt = []
    allDataE2ed = []

    initBandAss = {}
    for sli in list(sliceConfig):
        initBandAss[sli] = 100/len(list(sliceConfig))
    algoRes = algo.algorithm(sliceConfig, initBandAss, 1000, 0.33, 0.33, 1000, 50, False)
    # print(algoRes)

    algoMeanMos = {}
    algoMeanDelay = {}
    for sli in list(algoRes[8]):
        for cli in list(algoRes[8][sli]):
            # print(sli, cli,algoRes[8][sli][cli])
            algoMeanMos[cli] = algoRes[8][sli][cli]
            algoMeanDelay[cli] = algoRes[7][sli][cli]

    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            tempValueRtt = []
            tempValueE2ed = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                data = df[colName].dropna().tolist()
                if len(data) > 0:
                    # normalizedQoEdata = [normalizeQoE(nodeType, x) for x in data]
                    tempValue.append(normalizeQoE(nodeType,statistics.mean(data)))
                    allData.append(normalizeQoE(nodeType,statistics.mean(data)))
                if nodeType != 'hostVIP':
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " rtt Val"
                    data = dfRtt[colName].dropna().tolist()
                    if len(data) > 0:
                        tempValueRtt.append(statistics.mean(data))
                        allDataRtt.append(statistics.mean(data))
                else:
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " E2ED Val"
                    data = dfE2ed[colName].dropna().tolist()
                    if len(data) > 0:
                        tempValueE2ed.append(statistics.mean(data))
                        allDataE2ed.append(statistics.mean(data))

            # print(tempValue)
            print(nodeType + ':')
            meanMosFromExperiment[nodeType] = statistics.mean(tempValue)
            print('\tMean ' + dataIdent + ' of clients: ' + str(statistics.mean(tempValue)) + '; vs. predicted mean: ' + str(algoMeanMos[nodeType]))
            minMosValFromExperiment[nodeType] = min(tempValue)
            print('\tMin ' + dataIdent + ' of clients: ' + str(min(tempValue)))
            maxMosValFromExperiment[nodeType] = max(tempValue)
            print('\tMax ' + dataIdent + ' of clients: ' + str(max(tempValue)))
            mosFairnessFromExperiment[nodeType] = 1 - (2*statistics.stdev(tempValue))/(5.0-1.0)
            print('\tFairness ' + dataIdent + ' of clients: ' + str(1 - (2*statistics.stdev(tempValue))/(5.0-1.0)))
            if nodeType != 'hostVIP':
                print('\tMean delay of clients: ' + str(statistics.mean([x*1000/2 for x in tempValueRtt])) + '; vs. predicted mean: ' + str(algoMeanDelay[nodeType]))
                print('\tMin delay of clients: ' + str(min(tempValueRtt)*1000/2))
                print('\tMax delay of clients: ' + str(max(tempValueRtt)*1000/2))
            else:
                print('\tMean delay of clients: ' + str(statistics.mean([x*1000 for x in tempValueE2ed])) + '; vs. predicted mean: ' + str(algoMeanDelay[nodeType]))
                print('\tMin delay of clients: ' + str(min(tempValueE2ed)*1000))
                print('\tMax delay of clients: ' + str(max(tempValueE2ed)*1000))
            # allData.extend(tempValue)
    print(len(allData))
    print('Mean ' + dataIdent + ' of all clients: ' + str(statistics.mean(allData)) + '; vs. predicted mean: ' + str(algoRes[4]))
    print('Min ' + dataIdent + ' of all clients: ' + str(min(allData)) + '; vs. predicted min: ' + str(algoRes[2][2]))
    print('Max ' + dataIdent + ' of all clients: ' + str(max(allData)) + '; vs. predicted max: ' + str(algoRes[3][2]))
    print('Fairness ' + dataIdent + ' of all clients: ' + str(1 - (2*statistics.stdev(allData))/(5.0-1.0)) + '; vs. predicted fairness: ' + str(algoRes[5]))


def plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                tempValue.extend(df[colName].dropna().tolist())
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                partialCDFPlotData(fig, ax1, tempValue, chooseName(nodeType), '-o', chooseColor(nodeType))
    if dataIdent == 'Mos':
        ax1.set_xlim(0.95,5.05)
    else:
        ax1.set_xlim(0,1.01*maxValue)
    partialCDFEnd(fig,ax1,'', 'Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + '.pdf')
    partialCDFEndPNG(fig,ax1,'', 'Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + '.png')

def plotUtilityCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, nodeTypesToPlot):
    folderName = 'mos'
    dataIdent = 'Mos'
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                tempValue.extend([normalizeQoE(nodeType, x) for x in df[colName].dropna().tolist()])
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                partialCDFPlotData(fig, ax1, tempValue, chooseName(nodeType), '-o', chooseColor(nodeType))
    if dataIdent == 'Mos':
        ax1.set_xlim(0.95,5.05)
    # else:
    #     ax1.set_xlim(0,1.01*maxValue)
    prePath = '../exports/plots/baseSlicingComps/'
    if not os.path.exists(prePath):
        os.makedirs(prePath)
    plt.legend(loc='upper left')
    partialCDFEnd(fig,ax1,'', 'Utility', prePath+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'_'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + '.pdf')
    partialCDFEndPNG(fig,ax1,'', 'Utility', prePath+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'_'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + '.png')


niceTestName = {
    'baselineTest' : 'Baseline',
    'baselineTestTemp' : 'Temporary Baseline',
    'baselineTestNS_2sli_LVD-DES' : '2 Slices, Live in Delay, No Algorithm',
    'baselineTestNS_2sli_LVD-BWS' : '2 Slices, Live in Bandwidth, No Algorithm',
    'baselineTestNS_2sliSingle_LVD-DES' : '2 Slices + Single Link, Live Video in Delay Slice',
    'baselineTestNS_2sliSingle_LVD-BWS' : '2 Slices + Single Link, Live Video in Bandwidth Slice',
    'baselineTestNS_2sliSingle2sli_LVD-DES' : '2 Slices + Single Link + 2 Slices, Live Video in Delay Slice',
    'baselineTestNS_2sliSingle2sli_LVD-BWS' : '2 Slices + Single Link + 2 Slices, Live Video in Bandwidth Slice',
    'baselineTestNS_2sliDouble_LVD-DES' : 'Directional 2 Slices + Single Link, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliNBS_LVD-DES' : '2 Same Prio Queues: 2 + Single + 2 Links, Live Vid in Delay Slice',
    'baselineTestNSPrioQueueAF_2sliSingle2sliNBS_LVD-DES' : '2 Different Prio Queues: 2 + Single + 2 Links, Live Vid in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliNBS_LVD-BWS' : '2 Same Prio Queues: 2 + Single + 2 Links, Live Vid in Bandwidth Slice',
    'baselineTestNSPrioQueueAF_2sliSingle2sliNBS_LVD-BWS' : '2 Different Prio Queues: 2 + Single + 2 Links, Live Vid in Bandwidth Slice',
    'baselineTestNS_2sliDouble_LVD-BWS' : 'Directional 2 Slices + Single Link, Live Video in Bandwidth Slice',
    'baselineTestNS_5sli' : '5 Slices',
    'baselineTestNS_5sliSingle' : '5 Slices + Single Link',
    'baselineTestNS_5sliSingle5sli' : '5 Slices + Single Link + 5 Slices',
    'baselineTestNS_5sliDouble' : 'Directional 5 Slices + Single Link',
    'baselineTestNSPrioQueueAF_Single_LVD-DES' : 'Single Link with priority queue for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueAF_SingleLBS_LVD-DES' : 'Single Link with priority queue for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueAF_Single50_LVD-DES' : 'Single Link with priority queue for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueAF_SingleNBS_LVD-DES' : 'Single Link with priority queue for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_SingleDW_LVD-BWS' : 'Single Link with WRR sheduler, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_SingleDWR_LVD-DES' : 'Single Link with WRR sheduler, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_SingleDWR_LVD-BWS' : 'Single Link with WRR sheduler, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_SingleDWRLQ_LVD-DES' : 'One Link + WRR sheduler LQ, Live Vid in Delay Sli',
    'baselineTestNSPrioQueue_SingleDWRLQ_LVD-BWS' : 'One Link + WRR sheduler LQ, Live Vid in Bandwidth Sli',
    'baselineTestNSPrioQueueDES_2sliSingle2sli_LVD-DES' : '1 + 1 + 1 Links with Priority for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueDES_2sliSingle2sli_LVD-BWS' : '1 + 1 + 1 Links with Priority for Delay Slice, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWR_LVD-DES' : '1 + 1 + 1 Links with Weighted Queues, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWR_LVD-BWS' : '1 + 1 + 1 Links with Weighted Queues, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueueDES2_2sliSingle2sli_LVD-DES' : '2 + 1 + 2 Links with Priority for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueDES2_2sliSingle2sli_LVD-BWS' : '2 + 1 + 2 Links with Priority for Delay Slice, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueueDES4_2sliSingle2sli_LVD-DES' : '2 + 1 + 2 Links with 4x Priority for Delay Slice, Live Video in Delay Slice',
    'baselineTestNSPrioQueueDES4_2sliSingle2sli_LVD-BWS' : '2 + 1 + 2 Links with 4x Priority for Delay Slice, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWR2_LVD-DES' : '2 + 1 + 2 Links with Weighted Queues, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWR2_LVD-BWS' : '2 + 1 + 2 Links with Weighted Queues, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWRLQ_LVD-DES' : '2 + 1 + 2 Links with WRR, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWRLQ_LVD-BWS' : '2 + 1 + 2 Links with WRR, Live Video in Bandwidth Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWRLQPD_LVD-DES' : '2 + 1 + 2 Links WRR Delay Prio, Live Video in Delay Slice',
    'baselineTestNSPrioQueue_2sliSingle2sliDWRLQPD_LVD-BWS' : '2 + 1 + 2 Links WRR Delay Prio, Live Video in Bandwidth Slice',
    'baselineTestNS_5sli_AlgoTest1' : '5 Slices, Algorithm v0.1',
    'baselineTestNS_5sli_AlgoTest2' : '5 Slices, Algorithm v0.11',
    'baselineTestNS_5sli_AlgoTest3' : '5 Slices, Algorithm v0.12',
    'baselineTestNS_2sli_LVD-DES_AlgoTest1' : '2 Slices, Live in Delay, Algorithm v0.11',
    'baselineTestNS_2sli_LVD-BWS_AlgoTest1' : '2 Slices, Live in Bandwidth, Algorithm v0.11',
    'baselineTestNS_2sli_LVD-DES_AlgoTest3' : '2 Slices, Live in Delay, Algorithm v0.12',
    'baselineTestNS_2sli_LVD-BWS_AlgoTest3' : '2 Slices, Live in Bandwidth, Algorithm v0.12'
}



def plotMeanDataTypeCdfAllAppsComp(testNameMain, testNameSecondary, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    df = importDF(testNameMain, numCLI, nodeTypes, nodeSplit, folderName)
    df2 = importDF(testNameSecondary, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax = partialCDFBegin(2)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            tempValue2 = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                data = df[colName].dropna().tolist()
                data2 = df2[colName].dropna().tolist()
                if len(data) > 0:
                    tempValue.append(statistics.mean(data))
                if len(data2) > 0:
                    tempValue2.append(statistics.mean(data2))
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                if len(tempValue2) > 0:
                    if maxValue < max(tempValue2):
                        maxValue = max(tempValue2)
                partialCDFPlotData(fig, ax[0], tempValue, chooseName(nodeType), '-o', chooseColor(nodeType))
                partialCDFPlotData(fig, ax[1], tempValue2, chooseName(nodeType), '-o', chooseColor(nodeType))
    for axs in ax:
        if dataIdent == 'Mos':
            axs.set_xlim(0.95,5.05)
        else:
            axs.set_xlim(0,1.01*maxValue)
    ax[0].title.set_text(niceTestName[testNameMain])
    ax[1].title.set_text(niceTestName[testNameSecondary])
    partialCDFEnd(fig,ax,'', 'Mean Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_meanCdf' + dataIdent + str(nodeTypesToPlot) + 'compWith' + str(testNameSecondary) + '.pdf')
    partialCDFEndPNG(fig,ax,'', 'Mean Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_meanCdf' + dataIdent + str(nodeTypesToPlot) + 'compWith' + str(testNameSecondary) + '.png')


def plotDataTypeCdfAllAppsComp(testNameMain, testNameSecondary, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    df = importDF(testNameMain, numCLI, nodeTypes, nodeSplit, folderName)
    df2 = importDF(testNameSecondary, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax = partialCDFBegin(2)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            tempValue2 = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                tempValue.extend(df[colName].dropna().tolist())
                tempValue2.extend(df2[colName].dropna().tolist())
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                if len(tempValue2) > 0:
                    if maxValue < max(tempValue2):
                        maxValue = max(tempValue2)
                partialCDFPlotData(fig, ax[0], tempValue, chooseName(nodeType), '-o', chooseColor(nodeType))
                partialCDFPlotData(fig, ax[1], tempValue2, chooseName(nodeType), '-o', chooseColor(nodeType))
    if dataIdent == 'Mos':
        for axs in ax:
            axs.set_xlim(0.95,5.05)
    else:
        ax[0].set_xlim(0,1.01*maxValue)
        ax[1].set_xlim(0,1.01*maxValue)
    ax[0].title.set_text(niceTestName[testNameMain])
    ax[1].title.set_text(niceTestName[testNameSecondary])
    partialCDFEnd(fig,ax,'', 'Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + 'compWith' + str(testNameSecondary) + '.pdf')
    partialCDFEndPNG(fig,ax,'', 'Client ' + niceDataTypeName[dataIdent], '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf' + dataIdent + str(nodeTypesToPlot) + 'compWith' + str(testNameSecondary) + '.png')

def plotEstimatedChosenBitrateLVD(testName, numCLI, nodeTypes, nodeSplit, nodeTypesToPlot):
    df = importDF(testName, numCLI, nodeTypes, nodeSplit, 'daeb')
    df2 = importDF(testName, numCLI, nodeTypes, nodeSplit, 'davb')
    fig, ax = partialCDFBegin(1)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType in nodeTypesToPlot:
            tempValue = []
            tempValue2 = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " DAEB Val"
                colName2 = makeNodeIdentifier(nodeType, nodeNum) + " DAVB Val"
                tempValue.extend(df[colName].dropna().tolist())
                tempValue2.extend(df2[colName2].dropna().tolist())
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                if maxValue < max(tempValue2):
                    maxValue = max(tempValue2)
                partialCDFPlotData(fig, ax, tempValue, 'Estimated Bitrate', '-o', 'g')
                partialCDFPlotData(fig, ax, tempValue2, 'Chosen Video Bitrate', '-o', 'b')
    ax.set_xlim(0,1.01*maxValue)
    partialCDFEnd(fig,ax,'', 'Bitrate [kbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfDAEBDAVB'  + str(nodeTypesToPlot) + '.pdf')
    partialCDFEndPNG(fig,ax,'', 'Bitrate [kbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfDAEBDAVB'  + str(nodeTypesToPlot) + '.png')


def plotTPdirection(testName, numCLI, nodeTypes, nodeSplit, numSlices, direction):
    df = importDFextended(testName, numCLI, nodeTypes, nodeSplit, 'throughputs', '_' + direction[0])
    filtered_df = df.filter(like='FDO')
    print(filtered_df)
    print(filtered_df["Downlink Throughput hostFDO0"].to_string())
    print(statistics.mean(filtered_df["Downlink Throughput hostFDO0"]))
    print(statistics.stdev(filtered_df["Downlink Throughput hostFDO0"]))
    fig, ax1 = plt.subplots(1, figsize=(16,12))
    times = range(1,maxSimTime+1,1)
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        tempDF = pd.DataFrame() #keeps data for only one application type
        for nodeNum in range(numNodes):
            colName = direction[0] + " Throughput " + makeNodeIdentifier(nodeType, nodeNum)
            tempDF = pd.concat([tempDF,df[colName]],axis=1,ignore_index=False)
            print(tempDF.sum(axis=1).tolist())
        ax1.plot(times, [x/1000 for x in tempDF.sum(axis=1).tolist()], label=chooseName(nodeType), marker='o', ls='-', color=chooseColor(nodeType))
    #for sliceNum in range(numSlices):
    #    linkDF = filterDFType(df, direction[0] + ' Throughput resAllocLink' + str(sliceNum))
    #    ax1.plot(times, [x/1000 for x in linkDF.sum(axis=1).tolist()], label=chooseName(str(numSlices)+'link'+str(sliceNum)), marker='o', ls='-', color=chooseColor(str(numSlices)+'link'+str(sliceNum)))
        # print(linkDF)
    ax1.set_ylabel(direction[0]+' Throughput [mbps]')
    ax1.set_xlabel('Simulation Time [s]')
    ax1.set_xlim(0,1.01*times[-1])
    # ax1.set_ylim(0,105)
    plt.legend()
    plt.grid(True)
    fig.savefig('../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_'+direction[0]+'Throughputs' + str(nodeTypes) + '.pdf', dpi=100, bbox_inches='tight')

def plotTPScdfDirection(testName, numCLI, nodeTypes, nodeSplit, numSlices, direction, cutoff):
    df = importDFextended(testName, numCLI, nodeTypes, nodeSplit, 'throughputs', '_' + direction[0])
    fig, ax1 = partialCDFBegin(1)
    maxTPS = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        tempTPSall = []
        for nodeNum in range(numNodes):
            colName = direction[0] + " Throughput " + makeNodeIdentifier(nodeType, nodeNum)
            tempTPSall.extend([x/1000 for x in df[colName].tolist()[:int(cutoff)+1]])
        if maxTPS < max(tempTPSall):
            maxTPS = max(tempTPSall)
        partialCDFPlotData(fig, ax1, tempTPSall, chooseName(nodeType), '-o', chooseColor(nodeType))


    ax1.set_xlim(0,1.01*maxTPS)
    partialCDFEndPNG(fig,ax1,'', 'Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + '.png')
    partialCDFEnd(fig,ax1,'', 'Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdf'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + '.pdf')

def plotMeanTPScdfDirection(testName, numCLI, nodeTypes, nodeSplit, direction, cutoff):
    df = importDFextended(testName, numCLI, nodeTypes, nodeSplit, 'throughputs', '_' + direction[0])
    fig, ax1 = partialCDFBegin(1)
    maxTPS = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        tempTPSall = []
        for nodeNum in range(numNodes):
            colName = direction[0] + " Throughput " + makeNodeIdentifier(nodeType, nodeNum)
            tempTPSall.append(statistics.mean([x/1000 for x in df[colName].tolist()[:int(cutoff)+1]]))
        if maxTPS < max(tempTPSall):
            maxTPS = max(tempTPSall)
        partialCDFPlotData(fig, ax1, tempTPSall, chooseName(nodeType), '-o', chooseColor(nodeType))

    ax1.set_xlim(0,1.01*maxTPS)
    partialCDFEnd(fig,ax1,'', 'Mean Client Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfMean'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + '.pdf')
    partialCDFEndPNG(fig,ax1,'', 'Mean Client Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfMean'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + '.png')

def plotMeanTPScdfDirectionComp(testNameMain, testNameSecondary, numCLI, nodeTypes, nodeSplit, direction, cutoff):
    df = importDFextended(testNameMain, numCLI, nodeTypes, nodeSplit, 'throughputs', '_' + direction[0])
    df2 = importDFextended(testNameSecondary, numCLI, nodeTypes, nodeSplit, 'throughputs', '_' + direction[0])
    fig, ax = partialCDFBegin(2)
    maxTPS = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        tempTPSall = []
        tempTPSall2 = []
        for nodeNum in range(numNodes):
            colName = direction[0] + " Throughput " + makeNodeIdentifier(nodeType, nodeNum)
            tempTPSall.append(statistics.mean([x/1000 for x in df[colName].tolist()[:int(cutoff)+1]]))
            tempTPSall2.append(statistics.mean([x/1000 for x in df2[colName].tolist()[:int(cutoff)+1]]))
        if maxTPS < max(tempTPSall):
            maxTPS = max(tempTPSall)
        if maxTPS < max(tempTPSall2):
            maxTPS = max(tempTPSall2)
        partialCDFPlotData(fig, ax[0], tempTPSall, chooseName(nodeType), '-o', chooseColor(nodeType))
        partialCDFPlotData(fig, ax[1], tempTPSall2, chooseName(nodeType), '-o', chooseColor(nodeType))
    for axs in ax:
        axs.set_xlim(0,1.01*maxTPS)
    ax[0].title.set_text(niceTestName[testNameMain])
    ax[1].title.set_text(niceTestName[testNameSecondary])
    partialCDFEnd(fig,ax,'', 'Mean Client Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfMean'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + 'compWith' + str(testNameSecondary) + '.pdf')
    partialCDFEndPNG(fig,ax,'', 'Mean Client Throughput [mbps]', '../exports/plots/'+makeFullScenarioName(testNameMain, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfMean'+direction[0]+'ThroughputsCutoff'+ str(cutoff) + str(nodeTypes) + 'compWith' + str(testNameSecondary) + '.png')


def plotRTOcdf(testName, numCLI, nodeTypes, nodeSplit):
    rtos = []
    numSession = 0
    numSessionWithRTO = 0
    fullScenarioName = makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)
    file_to_read = '../exports/extracted/rto/' + fullScenarioName + '.csv'
    with open(file_to_read, mode='r') as readFile:
        csv_reader = csv.reader(readFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                rtos = row
            elif line_count == 1:
                numSession = row[0]
            elif line_count == 2:
                numSessionWithRTO = row[0]
            line_count += 1
    # print(rtos)
    print('Total Number of sessions at the SSH server: ' + str(numSession))
    print('Number of sessions at the SSH server where at least one retransmission timeout occured: ' + str(numSessionWithRTO))
    print('Percentage of sessions with a timeout: ' + str(numSessionWithRTO*100/numSession) + '%')
    fig, ax1 = partialCDFBegin(1)
    partialCDFPlotData(fig, ax1, rtos, 'SSH Server', '-o', chooseColor('hostSSH'))
    ax1.text(0.25,0.12, 'SSH server sessions - total: ' + str(int(numSession)), horizontalalignment='left', transform=ax1.transAxes)
    ax1.text(0.25,0.07, 'SSH server sessions - with timeout: ' + str(int(numSessionWithRTO)), horizontalalignment='left', transform=ax1.transAxes)
    ax1.text(0.25,0.02, 'Sessions with timeout: ' + str(round(numSessionWithRTO*100/numSession, 2)) + '%', horizontalalignment='left', transform=ax1.transAxes)
    partialCDFEnd(fig,ax1,'', 'RTO Value [s]', '../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)+'/'+str(globalCounter)+'_cdfRTO[\'serverSSH\'].pdf')

def plotSSHRTOcdfMultiTest(testNames, numCLIs, lineColors):
    fig, ax1 = partialCDFBegin(1)
    iterator = 0
    for testName in testNames:
        rtos = []
        numSession = 0
        numSessionWithRTO = 0
        fullScenarioName = str(testName) + '_' + str(numCLIs[iterator])
        file_to_read = '../exports/extracted/rto/' + fullScenarioName + '.csv'
        with open(file_to_read, mode='r') as readFile:
            csv_reader = csv.reader(readFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    rtos = row
                elif line_count == 1:
                    numSession = row[0]
                elif line_count == 2:
                    numSessionWithRTO = row[0]
                line_count += 1
        # print(rtos)
        print('Total Number of sessions at the SSH server: ' + str(numSession))
        print('Number of sessions at the SSH server where at least one retransmission timeout occured: ' + str(numSessionWithRTO))
        print('Percentage of sessions with a timeout: ' + str(numSessionWithRTO*100/numSession) + '%')
        
        partialCDFPlotData(fig, ax1, rtos, testName, '-o', lineColors[iterator])
        ax1.text(0.25,0.02+iterator*0.05, testName + ' # Sessions: ' + str(int(numSession)) + '; With Timeout: ' + str(round(numSessionWithRTO*100/numSession, 2)) + '%', horizontalalignment='left', transform=ax1.transAxes, fontsize=20)
        iterator += 1
    partialCDFEndPNG(fig,ax1,'', 'RTO Value [s]', '../exports/plots/'+str(testNames)+'_sshRtoCDF.png')

def chooseColorNS(nodeSplit):
    if nodeSplit == [10,10,10,10]:
        return 'c'
    elif nodeSplit == [20,20,20,20]:
        return 'm'
    elif nodeSplit == [30,30,30,30]:
        return 'y'
    elif nodeSplit == [40,40,40,40]:
        return 'b'
    elif nodeSplit == [50,50,50,50]:
        return 'g'

def chooseNameNS(nodeSplit):
    if nodeSplit == [10,10,10,10]:
        return '10 clients per app'
    elif nodeSplit == [20,20,20,20]:
        return '20 clients per app'
    elif nodeSplit == [30,30,30,30]:
        return '30 clients per app'
    elif nodeSplit == [40,40,40,40]:
        return '40 clients per app'
    elif nodeSplit == [50,50,50,50]:
        return '50 clients per app'

def plotMeanDataTypeCdfMultiRun(testName, nodeTypes, nodeSplits, dataIdent, folderName, nodeTypesToPlot):
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    for nodeSplit in nodeSplits:
        numCLI = sum(nodeSplit)
        df = importDF(testName, numCLI, nodeTypes, nodeSplit, folderName)
        for nodeType,numNodes in zip(nodeTypes,nodeSplit):
            if nodeType in nodeTypesToPlot:
                tempValue = []
                for nodeNum in range(numNodes):
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                    data = df[colName].dropna().tolist()
                    if len(data) > 0: 
                        tempValue.append(statistics.mean(data))
                # print(tempValue)
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                partialCDFPlotDataNoColor(fig, ax1, tempValue, nodeSplit, '-o')
    if dataIdent == 'Mos':
        ax1.set_xlim(0.95,5.05)
    else:
        ax1.set_xlim(0,1.01*maxValue)
    if not os.path.exists('../exports/plots/'+makeFullScenarioName(testName, 0, nodeTypes, [0,0,0,0])):
        os.makedirs('../exports/plots/'+makeFullScenarioName(testName, 0, nodeTypes, [0,0,0,0]))
    partialCDFEnd(fig,ax1,'', 'Mean Client ' + dataIdent + ' Value', '../exports/plots/'+makeFullScenarioName(testName, 0, nodeTypes, [0,0,0,0])+'/'+str(globalCounter)+'_meanCdf' + dataIdent + str(nodeTypesToPlot) + '.pdf')

def plotMultiTest(testName, nodeTypes, nodeSplits):
    for nodeType in nodeTypes:
        plotMeanDataTypeCdfMultiRun(testName, nodeTypes, nodeSplits, 'Mos', 'mos', [nodeType])
    plotMeanDataTypeCdfMultiRun(testName, nodeTypes, nodeSplits, 'RTT', 'rtt', ['hostSSH'])
    plotMeanDataTypeCdfMultiRun(testName, nodeTypes, nodeSplits, 'E2ED', 'e2ed', ['hostVIP'])
    plotMeanDataTypeCdfMultiRun(testName, nodeTypes, nodeSplits, 'PkLR', 'pklr', ['hostVIP'])


def plotMosBaseSliComp(testNameBaseline, testName2sli, testName5sli, numCLI, nodeTypes, nodeSplit, cliType):
    matplotlib.rc('lines', linewidth=3.0)
    matplotlib.rc('lines', markersize=8)
    folderName = 'mos'
    dataIdent = 'Mos'
    df = importDF(testNameBaseline, numCLI, nodeTypes, nodeSplit, folderName)
    df2 = importDF(testName2sli, numCLI, nodeTypes, nodeSplit, folderName)
    df5 = importDF(testName5sli, numCLI, nodeTypes, nodeSplit, folderName)
    fig, ax = partialCDFBegin(1)
    maxValue = 0
    for nodeType,numNodes in zip(nodeTypes,nodeSplit):
        if nodeType == cliType:
            tempValue = []
            tempValue2 = []
            tempValue5 = []
            for nodeNum in range(numNodes):
                colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                tempValue.extend([normalizeQoE(nodeType, x) for x in df[colName].dropna().tolist()])
                tempValue2.extend([normalizeQoE(nodeType, x) for x in df2[colName].dropna().tolist()])
                tempValue5.extend([normalizeQoE(nodeType, x) for x in df5[colName].dropna().tolist()])
            # print(tempValue)
            if len(tempValue) > 0:
                if maxValue < max(tempValue):
                    maxValue = max(tempValue)
                if len(tempValue2) > 0:
                    if maxValue < max(tempValue2):
                        maxValue = max(tempValue2)
                partialCDFPlotData(fig, ax, tempValue, 'Baseline', '-', 'red')
                print(np.sort(tempValue)[(np.abs(np.linspace(0, 1, len(tempValue), endpoint=True) - 0.4)).argmin()])
                partialCDFPlotData(fig, ax, tempValue2, '2 Slices', '-', 'blue')
                ax.arrow(np.sort(tempValue)[(np.abs(np.linspace(0, 1, len(tempValue), endpoint=True) - 0.4)).argmin()], 0.4, np.sort(tempValue2)[(np.abs(np.linspace(0, 1, len(tempValue2), endpoint=True) - 0.4)).argmin()] - np.sort(tempValue)[(np.abs(np.linspace(0, 1, len(tempValue), endpoint=True) - 0.4)).argmin()], 0, width=0.008, head_width=0.04, head_length=0.08, color='blue', length_includes_head=True, overhang=0.2)
                partialCDFPlotData(fig, ax, tempValue5, '5 Slices', '--', 'green')
                ax.arrow(np.sort(tempValue)[(np.abs(np.linspace(0, 1, len(tempValue), endpoint=True) - 0.6)).argmin()], 0.6, np.sort(tempValue5)[(np.abs(np.linspace(0, 1, len(tempValue5), endpoint=True) - 0.6)).argmin()] - np.sort(tempValue)[(np.abs(np.linspace(0, 1, len(tempValue), endpoint=True) - 0.6)).argmin()], 0, width=0.008, head_width=0.04, head_length=0.08, color='green', length_includes_head=True, overhang=0.2)
    if dataIdent == 'Mos':
        ax.set_xlim(0.95,5.05)
    else:
        ax[0].set_xlim(0,1.01*maxValue)
    prePath = '../exports/plots/baseSlicingComps/'
    if not os.path.exists(prePath):
        os.makedirs(prePath)
    partialCDFEnd(fig,ax,'', 'Utility', prePath+str(globalCounter)+'_cdf_' + testNameBaseline + '_' + dataIdent + '_' + str(cliType) + '_compWith' + str(testName2sli) + '_and_' + testName5sli + '.pdf')
    partialCDFEndPNG(fig,ax,chooseName(cliType), 'Utility', prePath+str(globalCounter)+'_cdf_' + testNameBaseline + '_' + dataIdent + '_' + str(cliType) + '_compWith' + str(testName2sli) + '_and_' + testName5sli + '.png')


def plotTPS(testName, numCLI, nodeTypes, nodeSplit, numSlices, direction, cutoff):
    global globalCounter
    print(testName + ': Plotting ' + direction[0] + ' Throughput over time...')
    plotTPdirection(testName, numCLI, nodeTypes, nodeSplit, numSlices, direction)
    globalCounter += 1
    print(testName + ': Plotting ' + direction[0] + ' Throughput CDF...')
    plotTPScdfDirection(testName, numCLI, nodeTypes, nodeSplit, numSlices, direction, cutoff)
    globalCounter += 1
    print(testName + ': Plotting ' + direction[0] + ' Mean Throughput CDF...')
    plotMeanTPScdfDirection(testName, numCLI, nodeTypes, nodeSplit, direction, cutoff)

def plotAll(testName, compTestName, nodeTypes, nodeSplit, numSlices, cutoff):
    global globalCounter
    globalCounter = 0
    numCLI = sum(nodeSplit)
    if not os.path.exists('../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit)):
        os.makedirs('../exports/plots/'+makeFullScenarioName(testName, numCLI, nodeTypes, nodeSplit))
    plotTPS(testName, numCLI, nodeTypes, nodeSplit, numSlices, downlink, cutoff)
    globalCounter += 1
    #plotTPS(testName, numCLI, nodeTypes, nodeSplit, numSlices, uplink, cutoff)
    globalCounter += 1
    print(testName + ': Plotting Mean MOS CDF...')
    #plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', nodeTypes)
    #plotMeanMosHeatmapTable(testName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', ["hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD","hostLVD"]) #"hostLVD","hostVIP","hostSSH","hostFDO"
    #plotMeanMosHeatmapTable(testName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', ["hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO","hostFDO"]) #"hostLVD","hostVIP","hostSSH","hostFDO"
    #plotMeanMosHeatmapTableSlice(testName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', ["hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID","hostVID"]) 
    globalCounter += 1
    print(testName + ': Plotting MOS CDF...')
    #plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', nodeTypes)
    globalCounter += 1
    if compTestName != '':
        plotMeanDataTypeCdfAllAppsComp(testName, compTestName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', nodeTypes)
        globalCounter += 1
        plotDataTypeCdfAllAppsComp(testName, compTestName, numCLI, nodeTypes, nodeSplit, 'Mos', 'mos2', nodeTypes)
        globalCounter += 1
        plotMeanDataTypeCdfAllAppsComp(testName, compTestName, numCLI, nodeTypes, nodeSplit, 'E2ED', 'endToEndDelay', nodeTypes)
        globalCounter += 1
    else:
        globalCounter += 3
    plotTPS(testName, numCLI, nodeTypes, nodeSplit, numSlices, downlink, cutoff)
    globalCounter += 1
    plotTPS(testName, numCLI, nodeTypes, nodeSplit, numSlices, uplink, cutoff)
    globalCounter += 1

    # if 'hostSSH' in nodeTypes: 
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'RTT', 'rtt', ['hostSSH'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'RTT', 'rtt', ['hostSSH'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'RTT', 'rtt', ['hostSSH'])
    #     globalCounter += 1
    # else:
    #     globalCounter += 3
    globalCounter += 3
    # if 'hostVIP' in nodeTypes: 
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'E2ED', 'e2ed', ['hostVIP'])
    #     globalCounter += 1
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PkLR', 'pklr', ['hostVIP'])
    #     globalCounter += 1
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PlDel', 'pldel', ['hostVIP'])
    #     globalCounter += 1
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PlLR', 'pllr', ['hostVIP'])
    #     globalCounter += 1
    #     plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'TDLR', 'tdlr', ['hostVIP'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'E2ED', 'e2ed', ['hostVIP'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PkLR', 'pklr', ['hostVIP'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PlDel', 'pldel', ['hostVIP'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'PlLR', 'pllr', ['hostVIP'])
    #     globalCounter += 1
    #     plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'TDLR', 'tdlr', ['hostVIP'])
    #     globalCounter += 1
    # else:
    #     globalCounter += 10
    globalCounter += 10
    if 'hostLVD' in nodeTypes:
        print(testName + ': Plotting Live Video Delay To Live CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DLVD', 'dlvd', ['hostLVD'])
        globalCounter += 1
        if compTestName != '':
            plotDataTypeCdfAllAppsComp(testName, compTestName, numCLI, nodeTypes, nodeSplit, 'DLVD', 'dlvd', ['hostLVD'])
        globalCounter += 1
        print(testName + ': Plotting Live Video Delay To Live CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DAEB', 'daeb', ['hostLVD'])
        globalCounter += 1
        print(testName + ': Plotting Live Video Estimated Bitrate CDF...')
        plotEstimatedChosenBitrateLVD(testName, numCLI, nodeTypes, nodeSplit, ['hostLVD'])
        globalCounter += 1
    if 'hostVID' in nodeTypes and 'hostLVD' in nodeTypes:
        print(testName + ': Plotting Video Buffer Length CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DABL', 'dabl', ['hostVID', 'hostLVD'])
        globalCounter += 1
        print(testName + ': Plotting Chosen Video Bitrate CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DAVB', 'davb', ['hostVID', 'hostLVD'])
        globalCounter += 1
        print(testName + ': Plotting Chosen Video Resolution CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DAVR', 'davr', ['hostVID', 'hostLVD'])
        globalCounter += 1
        print(testName + ': Plotting Video MOS CDF...')
        plotDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'DAMS', 'dams', ['hostVID', 'hostLVD'])
        globalCounter += 1
    if compTestName != '':
        plotMeanTPScdfDirectionComp(testName, compTestName, numCLI, nodeTypes, nodeSplit, downlink, cutoff)
    globalCounter += 1
    # print(testName + ': Plotting Mean End-To-End Delay CDF...')
    # plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'E2ED', 'endToEndDelay', nodeTypes)
    # globalCounter += 1
    # print(testName + ': Plotting Mean RTT CDF...')
    # plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'rtt', 'rtt', ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH'])
    # globalCounter += 1
    # print(testName + ': Plotting VoIP Mean End-To-End Delay CDF...')
    # plotMeanDataTypeCdfAllApps(testName, numCLI, nodeTypes, nodeSplit, 'E2ED', 'endToEndDelay', ['hostVIP'])
    # globalCounter += 1


# plotAll('baselineTest', '', ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [50 for x in range(5)], 1, 400)
# plotAll('newHmsQoeAdm4-3xDelNo3_5sli_R100_Q35_M100_C200_PFalse', '', ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [20,19,19,41,40], 1, 400)
# plotAll('newHmsQoeAdmNo3_5sli_R100_Q35_M100_C200_PFalse', '', ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP'], [20,19,19,31,30], 1, 400)

def plotMeanMosHeatmapTable(testName, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    #fig, axs = plt.subplots(len(testPrefixes), figsize=(10+sum([x for x in range(len(gbrs))])*1/5,(len(mbrs)-1)*len(testPrefixes)), sharex=True, sharey=True)
    #for testName in testNames: #for each run 
    print(testName)
    nodeTypesToPlot=["hostLVD"]
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    #testName = "bufferStudiesNoFlowsLVD"
    testName = "bufferStudiesNoFlowsFDO"
    testName = "bufferStudiesNoFlowsV2VoD"
    testName = "bufferStudiesQoSFlowsVoD"
    testName = "QoSFlowsLVD"
    # gbr = testName.split("GBR")[1]
    gbr = [100,85,80,50]
    numberOfClients = 28 #28 #50
    #queueSizes = [int(1120*20/math.sqrt(numberOfClients)), 1120*10,1120*20,65535*4,65535*8 ] #1120*20 VOD
    #queueSizes = [int(1820*20/math.sqrt(numberOfClients)),1820*10, 1820*20,65535*4,65535*8] #LVD
    queueSizes = [int(2240*20/math.sqrt(numberOfClients)), 2240*10, 2240*20,65535*4,65535*8] #FDO
  
    #for QoS Flows
    queueSizes = [2240*20,65535*4,65535*8] #FDO
    queueSizes = [1120*20,65535*4,65535*8] #VoD 
    queueSizes = [1820*20,65535*4,65535*8] #LVD
    queueSizesQuantization = []


    #queueSizesText = [ "\n BDP/sqrt(n)","\n BDP/2", "\n BDP", "\n rcvWnd * n /2", "\n rcvWnd * n"] #VoD
    #queueSizesText = [ "\n BDP/2", "\n BDP/tiny", "\n rcvWnd * n /2", "\n rcvWnd * n"] #VoD
    queueSizesText = [ "\n BDP/tiny", "\n rcvWnd * n /2", "\n rcvWnd * n"] #VoD

    print(queueSizes)
    testNames = []
    totalCli =[28,50,5]
    numCliArray = [133,153,165,266] 
    numCliArray = [133,157,165,266]
    

    for gbrMultiplier in gbr:
        print(gbrMultiplier)
        for queueSize in queueSizes:
            if (queueSize % 65535 != 0):
                queueSize = round(queueSize * gbrMultiplier/100)
            if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    queueSizesQuantization.append(queueSize)
            
        #     else:     
        #         queueSize = queueSize * numberOfClients
        #     print(testName + str(queueSize) +  "b_GBR" + str(gbrMultiplier))
            testNames.append(testName + str(queueSize) +  "b_GBR" + str(gbrMultiplier)) 
    print(testNames)
    print(queueSizes)
    meanMosAllCli = pd.DataFrame(columns=[x for x in queueSizes]) #create df with all apps as columns , index = [x for x in gbr]
    meanMosAllCli = pd.DataFrame() 
    print(meanMosAllCli)
    for scenario in testNames:    
        print(scenario)
        fullScenarioExportName = makeFullScenarioName(scenario, numCLI, nodeTypes, nodeSplit)
        print(fullScenarioExportName)
        #from here on is for getting average queue fullness
        # allData = pd.DataFrame()
        # fileToRead = '../' + str(scenario) + '/' + str(fullScenarioExportName) + '/vectors/' + str(fullScenarioExportName) + '_resAllocLink0' + '_vec.csv'
        # print("Importing: " + fileToRead)
        # df = pd.read_csv(fileToRead)
        #print("before if")
        #print(df.columns)

        # if not df.filter(like='queueBitLength').dropna().empty:
        #     print("*******in if now******")
        #     cols = [col for col in df.columns if 'queueBitLength' in col]
        #     for column in cols:
        #         print(df.columns.get_loc(column))
        #         print(column)
                

        #     #print(df.iloc[:, [166,167]])
        #     #print(df.columns.get_loc(df.filter(like='queueBitLength')))
        #     #print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
        #     print(df.iloc[:, [176]])
        #     df = df.iloc[:, [177]]
            
        #     df.columns = df.iloc[0,:].values
        #     df = df.tail(-1)
        #     queue = scenario.split("b_")[0].split("bufferStudiesNoFlowsLVD")[1]
        #     print(queue)
        #     print(df.dropna().head(50))
        #     df = ((df.dropna()/int(queue))*100)
           
        #     allData=pd.concat([allData, pd.DataFrame(df.values.tolist(), columns=[str(scenario)])], axis=1)
        #     print("------->Mean queue fullness is: ")
        #     print(statistics.mean(allData[str(scenario)].apply(float)))

        # for column in allData.columns:
        #     print(statistics.mean(allData[column].apply(float)))

        print(scenario)
        queueSize = int(scenario.split(testName)[1].split("b")[0])
        gbrMultiplier = int(scenario.split("_GBR")[1])
        print("***********************************************")
        print(queueSize)
        print(gbrMultiplier)
        #df = importDF(scenario, numCliArray[gbr.index(int(gbrMultiplier))], nodeTypes, [round(x*100/gbrMultiplier) for x in nodeSplit], folderName) #round/int
        nodeSplit=[numberOfClients,0,0,0,0,0] #vid

        nodeSplit= [0,0,numberOfClients, 0, 0, 0] #fdo
        nodeSplit=[0,numberOfClients,0,0,0,0] #lvd

        df = importDF(scenario, round(numberOfClients*100/gbrMultiplier), nodeTypes, [round(x*100/gbrMultiplier) for x in nodeSplit], folderName) #round/int

        
        print(df)
        for nodeType,numNodes in zip(nodeTypes,nodeSplit):
            if nodeType in nodeTypesToPlot:
                tempValue = []
                for nodeNum in range(numNodes):
                    print(makeNodeIdentifier(nodeType, nodeNum))
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                    data = df[colName].dropna().tolist()
                    print(data)
                    print("Data is: -----------------------")
                    if len(data) > 0:
                        tempValue.append(statistics.mean(data.dropna())) #tempValue will contain mean for all clients of specific types 
                    else:
                        print("no data")
                        print(makeNodeIdentifier(nodeType, nodeNum))

                print(scenario)
                print("QueueSize is ")
                print(queueSize)
                print(int(100*40/gbrMultiplier))
                #comment out when we do QoSFlows and uncomment for when we do slicing 
                # if (queueSize % 65535 == 0):
                #     queueSizeOriginal = queueSize/int(100*numberOfClients/gbrMultiplier)
                # else:     
                #     queueSizeOriginal = queueSize/numberOfClients
                
                
                #queuSizeOriginal= int(queueSize)/int(100*40/gbrMultiplier)
                print("QueuSize Original is")
                #print(queueSizeOriginal)
                #this is for Slicing 
                #meanMosAllCli.loc[str(gbrMultiplier), str(queueSizeOriginal) + queueSizesText[queueSizes.index(queueSizeOriginal)] ] = float(statistics.mean(tempValue))
                #this is for QoS Flows
                print("Queue Sizes Text")
                print(queueSizesText)
                print(queueSizesQuantization)
                if len(tempValue) > 0:
                    meanMosAllCli.loc[str(gbrMultiplier), queueSizesText[queueSizesQuantization.index(queueSize)%len(queueSizes)]] = float(statistics.mean(tempValue))
                else:
                    meanMosAllCli.loc[str(gbrMultiplier), queueSizesText[queueSizesQuantization.index(queueSize)%len(queueSizes)]] = 1.0
                print("MOS data is")
                print(meanMosAllCli)
    # meanMosAllCli.loc["200", "hostVID"] = float(statistics.mean(tempValue))
    # meanMosAllCli.loc["300", "hostVID"] = float(4.0)
    # meanMosAllCli.loc["400", "hostVID"] = float(4.0)
    
    print(type(meanMosAllCli))        
    print(meanMosAllCli)
    meanMosAllCli = meanMosAllCli.astype(float)
    fig, ax = plt.subplots(figsize=(40,30))
    sn.set(font_scale=5)
    sn.heatmap(meanMosAllCli, annot=True,  fmt='.3g', cmap='viridis', vmin=0, vmax=5, cbar_kws={'label': 'MOS','orientation': 'vertical' })
    ax.set_ylabel("GBR (percentage of the original GBR)")
    ax.set_xlabel("Queue size [bits]")
    ax.set_ylabel("GBR (percentage of the original GBR)")
    
    ax.collections[0].colorbar.set_label("MOS",rotation=270,  labelpad=40)

    #figure = heatmap.get_figure().set_figwidth(20)

    fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsVoD896000b_GBR100_133_VID50_LVD28_FDO5_SSH10_VIP40_HVIP0"+'/heatmap' + scenario, dpi=400, format="pdf") 
    #fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsLVD7339920b_GBR100_133_VID50_LVD28_FDO5_SSH10_VIP40_HVIP0"+'/heatmap' + scenario + '.pdf', dpi=400) 
    #/mnt/data/improved5gNS/analysis/exports/plots/bufferStudiesNoFlowsFDO112000b_GBR85_153_VID58_LVD32_FDO5_SSH11_VIP47_HVIP0 fig.savefig('../exports/plots/' + '/heatmapFDO' + '.pdf', dpi=400) 
    #fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsFDO112000b_GBR85_153_VID58_LVD32_FDO5_SSH11_VIP47_HVIP0"+'/heatmap' + scenario +  '.pdf', dpi=400) 


def plotMeanMosHeatmapTableSlice(testName, numCLI, nodeTypes, nodeSplit, dataIdent, folderName, nodeTypesToPlot):
    #fig, axs = plt.subplots(len(testPrefixes), figsize=(10+sum([x for x in range(len(gbrs))])*1/5,(len(mbrs)-1)*len(testPrefixes)), sharex=True, sharey=True)
    #for testName in testNames: #for each run 
    print(testName)
    nodeTypesToPlot=["hostLVD"]
    fig, ax1 = partialCDFBegin(1)
    maxValue = 0
    #testName = "bufferStudiesNoFlowsLVD"
    testName = "bufferStudiesNoFlowsFDO"
    testName = "bufferStudiesNoFlowsV2VoD"
    testName = "bufferStudiesQoSFlowsVoD"
    testName = "QoSFlowsLVD"
    testName = "SliceNoFlowsLVD"
    # gbr = testName.split("GBR")[1]
    gbr = [100, 85,80,50]
    numberOfClients = 28 #28 #50
    #queueSizes = [int(1120*20/math.sqrt(numberOfClients)), 1120*10,1120*20,65535*4,65535*8] #1120*20 VOD  int(1120*20/math.sqrt(numberOfClients)), 1120*10,1120*20,
    queueSizes = [int(1820*20/math.sqrt(numberOfClients)), 1820*10,1820*20,65535*4,65535*8] #LVD int(1820*20/math.sqrt(numberOfClients)) 1820*10, 1820*20,
    #queueSizes = [int(2240*20/math.sqrt(numberOfClients)), 2240*10, 2240*20,65535*4,65535*8] #FDO
  
    #for QoS Flows
    # queueSizes = [2240*20,65535*4,65535*8] #FDO
    # queueSizes = [1120*20,65535*4,65535*8] #VoD 
    # queueSizes = [1820*20,65535*4,65535*8] #LVD

    queueSizesQuantization = []


    queueSizesText = [ "\n Tiny Buffer", "\n BDP/2", "\n BDP",  "\n rcvWnd * n /2", "\n rcvWnd * n", ] #VoD
    #queueSizesText = [ "\n BDP/2", "\n BDP/tiny", "\n rcvWnd * n /2", "\n rcvWnd * n"] #VoD
    #queueSizesText = [ "\n BDP/tiny", "\n rcvWnd * n /2", "\n rcvWnd * n"] #VoD

    print(queueSizes)
    testNames = []
    totalCli =[28,50,5]
    numCliArray = [133,153,165,266] 
    numCliArray = [133,157,165,266]
    

    for gbrMultiplier in gbr:
        print(gbrMultiplier)
        for queueSize in queueSizes:
            if queueSize % 65535 == 0:
                queueSize = queueSize * int(numberOfClients * 100 / gbrMultiplier) #rcwnd * N 
            else:
                queueSize = queueSize * numberOfClients 

            if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    queueSizesQuantization.append(queueSize)
            
        #     else:     
        #         queueSize = queueSize * numberOfClients
        #     print(testName + str(queueSize) +  "b_GBR" + str(gbrMultiplier))
            testNames.append(testName + str(queueSize) +  "b_GBR" + str(gbrMultiplier)) 
    print(testNames)
    print(queueSizesQuantization)
    meanMosAllCli = pd.DataFrame(columns=[x for x in queueSizes]) #create df with all apps as columns , index = [x for x in gbr]
    meanMosAllCli = pd.DataFrame() 
    print(meanMosAllCli)
    for scenario in testNames:    
        print(scenario)
        fullScenarioExportName = makeFullScenarioName(scenario, numCLI, nodeTypes, nodeSplit)
        print(fullScenarioExportName)
        #from here on is for getting average queue fullness
        # allData = pd.DataFrame()
        # fileToRead = '../' + str(scenario) + '/' + str(fullScenarioExportName) + '/vectors/' + str(fullScenarioExportName) + '_resAllocLink0' + '_vec.csv'
        # print("Importing: " + fileToRead)
        # df = pd.read_csv(fileToRead)
        #print("before if")
        #print(df.columns)

        # if not df.filter(like='queueBitLength').dropna().empty:
        #     print("*******in if now******")
        #     cols = [col for col in df.columns if 'queueBitLength' in col]
        #     for column in cols:
        #         print(df.columns.get_loc(column))
        #         print(column)
                

        #     #print(df.iloc[:, [166,167]])
        #     #print(df.columns.get_loc(df.filter(like='queueBitLength')))
        #     #print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
        #     print(df.iloc[:, [176]])
        #     df = df.iloc[:, [177]]
            
        #     df.columns = df.iloc[0,:].values
        #     df = df.tail(-1)
        #     queue = scenario.split("b_")[0].split("bufferStudiesNoFlowsLVD")[1]
        #     print(queue)
        #     print(df.dropna().head(50))
        #     df = ((df.dropna()/int(queue))*100)
           
        #     allData=pd.concat([allData, pd.DataFrame(df.values.tolist(), columns=[str(scenario)])], axis=1)
        #     print("------->Mean queue fullness is: ")
        #     print(statistics.mean(allData[str(scenario)].apply(float)))

        # for column in allData.columns:
        #     print(statistics.mean(allData[column].apply(float)))

        print(scenario)
        queueSize = int(scenario.split(testName)[1].split("b")[0])
        gbrMultiplier = int(scenario.split("_GBR")[1])
        print("***********************************************")
        print(queueSize)
        print(gbrMultiplier)
        #df = importDF(scenario, numCliArray[gbr.index(int(gbrMultiplier))], nodeTypes, [round(x*100/gbrMultiplier) for x in nodeSplit], folderName) #round/int
        
        
        
        #nodeSplit=[numberOfClients,0,0,0,0,0] #vid
        #nodeSplit= [0,0,numberOfClients, 0, 0, 0] #fdo
        nodeSplit=[0,numberOfClients,0,0,0,0] #lvd

        df = importDF(scenario, round(numberOfClients*100/gbrMultiplier), nodeTypes, [round(x*100/gbrMultiplier) for x in nodeSplit], folderName) #round/int

        
        print(df)
        for nodeType,numNodes in zip(nodeTypes,nodeSplit):
            if nodeType in nodeTypesToPlot:
                tempValue = []
                for nodeNum in range(numNodes):
                    print(makeNodeIdentifier(nodeType, nodeNum))
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                    data = df[colName].dropna().tolist()
                    if len(data) > 0:
                        tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                        print(statistics.mean(data))
                    else:
                        print("no data")
                        print(makeNodeIdentifier(nodeType, nodeNum))
                print(tempValue)
                print("this is mean")
                print(statistics.mean(tempValue))
                print(scenario)
                print("QueueSize is ")
                print(queueSize)
                print(int(100*40/gbrMultiplier))
                #comment out when we do QoSFlows and uncomment for when we do slicing 
                # if (queueSize % 65535 == 0):
                #     queueSizeOriginal = queueSize/int(100*numberOfClients/gbrMultiplier)
                # else:     
                #     queueSizeOriginal = queueSize/numberOfClients
                
                
                #queuSizeOriginal= int(queueSize)/int(100*40/gbrMultiplier)

                #this is for Slicing 
                #meanMosAllCli.loc[str(gbrMultiplier), str(queueSizeOriginal) + queueSizesText[queueSizes.index(queueSizeOriginal)] ] = float(statistics.mean(tempValue))
                #this is for QoS Flows
                print("Adjusted queue sizes")
                print(queueSizesQuantization)
                print("Current queue size")
                print(queueSize)
                print("index in the adjusted queue")
                print(queueSizesQuantization.index(queueSize))
                print("length of the queue sizes ")
                print(len(queueSizes))
                print("Adding to this position: ")
                print(queueSizesQuantization.index(queueSize)%len(queueSizes))
                if len(tempValue) > 0:
                    meanMosAllCli.loc[str(gbrMultiplier), queueSizesText[queueSizesQuantization.index(queueSize)%len(queueSizes)]] = float(statistics.mean(tempValue))
                    queueSizesQuantization[queueSizesQuantization.index(queueSize)]=0
                else:
                    meanMosAllCli.loc[str(gbrMultiplier), queueSizesText[queueSizesQuantization.index(queueSize)%len(queueSizes)]] = 1.0
                    queueSizesQuantization[queueSizesQuantization.index(queueSize)]=0
                print("MOS data is")
                print(meanMosAllCli)
    # meanMosAllCli.loc["200", "hostVID"] = float(statistics.mean(tempValue))
    # meanMosAllCli.loc["300", "hostVID"] = float(4.0)
    # meanMosAllCli.loc["400", "hostVID"] = float(4.0)
    
    print(type(meanMosAllCli))        
    print(meanMosAllCli)
    meanMosAllCli = meanMosAllCli.astype(float)
    fig, ax = plt.subplots(figsize=(40,30))
    sn.set(font_scale=5)
    sn.heatmap(meanMosAllCli, annot=True,  fmt='.3g', cmap='viridis', vmin=0, vmax=5, cbar_kws={'label': 'MOS','orientation': 'vertical' })
    ax.set_ylabel("GBR (percentage of the original GBR)")
    ax.set_xlabel("Queue size [bits]")
    ax.set_ylabel("GBR (percentage of the original GBR)")
    
    ax.collections[0].colorbar.set_label("MOS",rotation=270,  labelpad=40)

    #figure = heatmap.get_figure().set_figwidth(20)

    fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsVoD896000b_GBR100_133_VID50_LVD28_FDO5_SSH10_VIP40_HVIP0"+'/heatmap' + scenario + ".pdf", dpi=400, format="pdf") 
    #fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsLVD7339920b_GBR100_133_VID50_LVD28_FDO5_SSH10_VIP40_HVIP0"+'/heatmap' + scenario + '.pdf', dpi=400) 
    #/mnt/data/improved5gNS/analysis/exports/plots/bufferStudiesNoFlowsFDO112000b_GBR85_153_VID58_LVD32_FDO5_SSH11_VIP47_HVIP0 fig.savefig('../exports/plots/' + '/heatmapFDO' + '.pdf', dpi=400) 
    #fig.savefig('../exports/plots/' + "bufferStudiesNoFlowsFDO112000b_GBR85_153_VID58_LVD32_FDO5_SSH11_VIP47_HVIP0"+'/heatmap' + scenario +  '.pdf', dpi=400) 



#The function  mainEffectsPlot() creats a figure with sublots showing the main effect, i.e. one subplot for each of the key impact factors and the correponding trend.
def mainEffectsPlot(testNames, numCli, queueSizesText, throughputs, granularities):
    
    meanMosForXClients = [] #should contain mean mos for all scenarios where client number is 10,20, etc...
    for numberOfClients in numCli: 
        print(numberOfClients)
        tempMeanAllClientsInTheRun = []
            
        for testName in testNames: #testNames is a list of all configs we want to plot, we do the plot per application for now 
            if "n" + str(numberOfClients) +"_" in testName:
                print(testName)        
                originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
                nodeSplit= [0,0,0,0,0,0] #in kbps, based on CNSM heatmaps
                nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
                dataIdent="Mos"
                rtt = 20 #ms
                num=int(testName.split("n")[1].split("_q")[0])
                #numCli.append(int(testName.split("n")[1].split("_q")[0]))
                queueSizeText = testName.split("q")[1].split("_tp")[0]
                throughputPercentage = testName.split("tp")[1].split("_g")[0]#percetage of the orginial throughput assigned to the application
                application = "host" + testName.split("a")[1]
                nodeTypesToPlot = [application]
        
                nodeSplit[nodeTypes.index(application)] = num
                df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")
                
                for nodeType,numNodes in zip(nodeTypes,nodeSplit):
                    if nodeType in nodeTypesToPlot:
                        tempValue = []
                        for nodeNum in range(int(num)):
                            colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                            data = df[colName].dropna().tolist()
                            if len(data) > 0:
                                tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                            else:
                                print(makeNodeIdentifier(nodeType, nodeNum))
                        print(tempValue) 
                        #print("This is mean")
                        #print(statistics.mean(tempValue))
                        #print(meanMosForXClients)
                        if len(data) > 0:
                            tempMeanAllClientsInTheRun.append(statistics.mean(tempValue)) #mean of all clients in the run
                        else:
                            tempMeanAllClientsInTheRun.append(1.0) #mean of all clients in the run
                        #print(meanMosForXClients)
        meanMosForXClients.append(statistics.mean(tempMeanAllClientsInTheRun))    
        #print(meanMosForXClients)    

    print(meanMosForXClients)
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 10}

    matplotlib.rc('font', **font)
    fig, axs = plt.subplots(4)
    fig.subplots_adjust(wspace=None, hspace=0.8)
    fig.suptitle('Main Effect Plot for '+ testName.split("a")[1])
    axs[0].plot(numCli, meanMosForXClients)
    axs[0].set_ylim(2.5,3.6)
    axs[0].set_xlabel("Number of clients")
    

    
    meanMosForXClients = [] 
    for queueSize in queueSizesText: 
        print(numberOfClients)
        tempMeanAllClientsInTheRun = []
            
        for testName in testNames: #testNames is a list of all configs we want to plot, we do the plot per application for now 
            if "q" + queueSize +"_" in testName:
                print(testName)        
                originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
                nodeSplit= [0,0,0,0,0,0] #in kbps, based on CNSM heatmaps
                nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
                dataIdent="Mos"
                rtt = 20 #ms
                num=int(testName.split("n")[1].split("_q")[0])
                #numCli.append(int(testName.split("n")[1].split("_q")[0]))
                queueSizeText = testName.split("q")[1].split("_tp")[0]
                throughputPercentage = testName.split("tp")[1].split("_g")[0]#percetage of the orginial throughput assigned to the application
                application = "host" + testName.split("a")[1]
                nodeTypesToPlot = [application]
        
                nodeSplit[nodeTypes.index(application)] = num
                df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")
                
                for nodeType,numNodes in zip(nodeTypes,nodeSplit):
                    if nodeType in nodeTypesToPlot:
                        tempValue = []
                        for nodeNum in range(int(num)):
                            colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                            data = df[colName].dropna().tolist()
                            if len(data) > 0:
                                tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                            else:
                                print(makeNodeIdentifier(nodeType, nodeNum))
                        if len(data) > 0:
                            tempMeanAllClientsInTheRun.append(statistics.mean(tempValue)) #mean of all clients in the run
                        else:
                            tempMeanAllClientsInTheRun.append(1.0) #mean of all clients in the run
        meanMosForXClients.append(statistics.mean(tempMeanAllClientsInTheRun))    
        #print(meanMosForXClients)    
    axs[1].plot(queueSizesText, meanMosForXClients)
    axs[1].set_ylim(2.5,3.6)
    axs[1].set_xlabel("Queue sizes (B=BDP, R2=rcwnd/2, R=rcwnd)")

    meanMosForXClients = [] 
    for tp in throughputs: 
        print(numberOfClients)
        tempMeanAllClientsInTheRun = []
            
        for testName in testNames: #testNames is a list of all configs we want to plot, we do the plot per application for now 
            if "tp" + str(tp) +"_" in testName:
                print(testName)        
                originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
                nodeSplit= [0,0,0,0,0,0] #in kbps, based on CNSM heatmaps
                nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
                dataIdent="Mos"
                rtt = 20 #ms
                num=int(testName.split("n")[1].split("_q")[0])
                queueSizeText = testName.split("q")[1].split("_tp")[0]
                throughputPercentage = testName.split("tp")[1].split("_g")[0]#percentage of the orginial throughput assigned to the application
                application = "host" + testName.split("a")[1]
                nodeTypesToPlot = [application]
        
                nodeSplit[nodeTypes.index(application)] = num
                df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")
                
                for nodeType,numNodes in zip(nodeTypes,nodeSplit):
                    if nodeType in nodeTypesToPlot:
                        tempValue = []
                        for nodeNum in range(int(num)):
                            colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                            data = df[colName].dropna().tolist()
                            if len(data) > 0:
                                tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                            else:
                                print(makeNodeIdentifier(nodeType, nodeNum))
                        print(tempValue) 
                        #print("This is mean")
                        #print(statistics.mean(tempValue))
                        #print(meanMosForXClients)
                        if len(tempValue) > 0:
                            tempMeanAllClientsInTheRun.append(statistics.mean(tempValue)) #mean of all clients in the run
                        else:
                            tempMeanAllClientsInTheRun.append(1.0)
                        #print(meanMosForXClients)
        meanMosForXClients.append(statistics.mean(tempMeanAllClientsInTheRun))    
        print("-------------------------------------------------------------")
        print(meanMosForXClients)    
    axs[2].plot(throughputs, meanMosForXClients)
    axs[2].set_ylim(2,3.7)
    axs[2].set_xlabel("Throughput (as % of the $Tp_{ref}$="  + str(originalTPperClient[testName.split("a")[1]]) + "kbps for " + testName.split("a")[1]  + ")")


    meanMosForXClients = [] 
    for gran in granularities: 
        print(numberOfClients)
        tempMeanAllClientsInTheRun = []
            
        for testName in testNames: #testNames is a list of all configs we want to plot, we do the plot per application for now 
            if "g" + str(gran) +"_" in testName:
                print(testName)        
                originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
                nodeSplit= [0,0,0,0,0,0] #in kbps, based on CNSM heatmaps
                nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
                dataIdent="Mos"
                rtt = 20 #ms
                num=int(testName.split("n")[1].split("_q")[0])
                #numCli.append(int(testName.split("n")[1].split("_q")[0]))
                queueSizeText = testName.split("q")[1].split("_tp")[0]

                throughputPercentage = testName.split("tp")[1].split("_g")[0]#percetage of the orginial throughput assigned to the application

                application = "host" + testName.split("a")[1]
                nodeTypesToPlot = [application]
        
                nodeSplit[nodeTypes.index(application)] = num
                df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")
                
                for nodeType,numNodes in zip(nodeTypes,nodeSplit):
                    if nodeType in nodeTypesToPlot:
                        tempValue = []
                        for nodeNum in range(int(num)):
                            colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                            data = df[colName].dropna().tolist()
                            if len(data) > 0:
                                tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                            else:
                                print(makeNodeIdentifier(nodeType, nodeNum))
                        print(tempValue) 
                        #print("This is mean")
                        #print(statistics.mean(tempValue))
                        #print(meanMosForXClients)
                        if len(tempValue) > 0:
                            tempMeanAllClientsInTheRun.append(statistics.mean(tempValue)) #mean of all clients in the run
                        else:
                            tempMeanAllClientsInTheRun.append(1.0)
                        #print(meanMosForXClients)
        meanMosForXClients.append(statistics.mean(tempMeanAllClientsInTheRun))    
        print("-------------------------------------------------------------")
        print(meanMosForXClients)    
    axs[3].plot(granularities, meanMosForXClients)
    axs[3].set_ylim(2.5,3.5)
    axs[3].set_xlabel("Granularity of the Resource Allocation Mechanism (\"F\" = per flow, \"S\" = per slice)")

    fig.savefig('../exports/plots/' + testName + ".pdf", dpi=400, format="pdf") 


#The function createCSV(testNames) extracts the MOS data from OMNeT++ scavetool exports and saves it to a csv. testNames represent the configuration names. 

def createCSV(testNames):

     for testName in testNames: 
        print(testName)        
        originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM paper heatmaps
        nodeSplit= [0,0,0,0,0,0] # initiate empty array indicating the number of clients for each application in the scenario evaluated
        nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
        dataIdent="Mos"
        rtt = 20 #ms, this is the delay set in the simulation configuration, was set to 20 constantly in the scope of this paper. 
        num=int(testName.split("n")[1].split("_q")[0])
        queueSizeText = testName.split("q")[1].split("_tp")[0]
        throughputPercentage = testName.split("tp")[1].split("_g")[0]#percentage of the orginial throughput assigned to the application
        granularity = testName.split("g")[1].split("_a")[0]#granurality of the resource allocation schemes
        application = "host" + testName.split("a")[1]
        nodeTypesToPlot = [application]

        nodeSplit[nodeTypes.index(application)] = num
        try:
            df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")
        except:
            print("---------No file found!-------------")
            print(testName)
            continue
        
        for nodeType,numNodes in zip(nodeTypes,nodeSplit):
            if nodeType in nodeTypesToPlot:
                tempValue = []
                for nodeNum in range(int(num)):
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                    data = df[colName].dropna().tolist()
                    if len(data) > 0:
                        tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                    else:
                        print(makeNodeIdentifier(nodeType, nodeNum))
                        tempValue.append(1.0) 
        if len(tempValue) > 0:
            if len(tempValue) > 1:
                myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + granularity + ", " + application + ", " + str(statistics.mean(tempValue))  + ", " + str(statistics.stdev(tempValue)) + "\n" #+ ", " + str(statistics.stdev(tempValue))
            else:
                myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + granularity + ", " + application + ", " + str(statistics.mean(tempValue))  + ", " + str(0.0) + "\n" #+ ", " + str(statistics.stdev(tempValue))

        else:
            myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + granularity + ", " + application + ", " + "1.0" + "\n"

        with open('../extracted/mos2/dataMOS0409.csv','a') as fd: #FIXME: change the name of the cs file here if needed
            fd.write(myCsvRow)
#The function createCSVWithActualQueueSize(testNames) is analogue to createCSV(testNames) for extracting the actual queue size data from OMNeT++ and saving it to a csv        
def createCSVWithActualQueueSize(testNames):

     for testName in testNames:
        print(testName)        
        delay=20
        originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
        nodeSplit= [0,0,0,0,0,0] 
        nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
        dataIdent="Mos"
        rtt = 20 #ms
        num=int(testName.split("n")[1].split("_q")[0])
       
        queueSizeText = testName.split("q")[1].split("_tp")[0]
        throughputPercentage = testName.split("tp")[1].split("_g")[0]
        granularity = testName.split("g")[1].split("_a")[0]
        application = "host" + testName.split("a")[1]
        nodeTypesToPlot = [application]

        if granularity == "S": #coarse granular, slice configurations 
            if queueSizeText == "B":
                queueSize = int(throughputPercentage) * num * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "10B":
                queueSize = 10 * int(throughputPercentage) * num * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "5B":
                queueSize = 5 * int(throughputPercentage) * num * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "R":
                queueSize = 65535 * 8 * n
            elif queueSizeText == "T":
                queueSize = (int(throughputPercentage) * num * originalTPperClient[testName.split("a")[1]] * delay /100) / math.sqrt(num)

            if testName.split("a")[1] != "VIP":
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
            else:
                if (queueSize % (75*8) !=0):
                    queueSize = math.ceil(queueSize/(75 * 8))*75*8 #MSS = 75B
        else:
            if queueSizeText == "B":
                queueSize = int(throughputPercentage) * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "10B":
                queueSize = 10 * int(throughputPercentage) * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "5B":
                queueSize = 5 * int(throughputPercentage) * originalTPperClient[testName.split("a")[1]] * delay /100
            elif queueSizeText == "R":
                queueSize = 65535 * 8
            elif queueSizeText == "T":
                queueSize = (int(throughputPercentage) * originalTPperClient[testName.split("a")[1]] * delay /100) / math.sqrt(num)
            if testName.split("a")[1] != "VIP":
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
            else:
                if (queueSize % (75*8) !=0):
                    queueSize = math.ceil(queueSize/(75 * 8))*75*8 #MSS = 1499B

        nodeSplit[nodeTypes.index(application)] = num
        try:
            df = importDF(testName, num, nodeTypes, nodeSplit, "mos2")

        except:
            print("--------------------------No file found!---------------------------") # for some comibinations, e.g. 1 client and TinyBuffer queue size there are no simulations since it is the same as for BDP, so those should be skipped
            print(testName)
            continue
        
        for nodeType,numNodes in zip(nodeTypes,nodeSplit):
            if nodeType in nodeTypesToPlot:
                tempValue = []
                for nodeNum in range(int(num)):
                    colName = makeNodeIdentifier(nodeType, nodeNum) + " " + dataIdent + " Val"
                    data = df[colName].dropna().tolist()
                    if len(data) > 0:
                        tempValue.append(statistics.mean(data)) #tempValue will contain mean for all clients of specific types 
                    else:
                        print(makeNodeIdentifier(nodeType, nodeNum))
                        tempValue.append(1.0) 
        if granularity == "F":
            g=0
        else:
            g=1
        if len(tempValue) > 0:
            if len(tempValue) > 1:
                myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + str(g) + ", " + application + ", " + str(statistics.mean(tempValue))  + ", " + str(statistics.stdev(tempValue)) + ", " + str(queueSize) + "\n" #+ ", " + str(statistics.stdev(tempValue))
            else:
                myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + str(g) + ", " + application + ", " + str(statistics.mean(tempValue))  + ", " + str(0.0) + ", " + str(queueSize) + "\n" #+ ", " + str(statistics.stdev(tempValue))

        else:
            myCsvRow = str(num) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + granularity + ", " + application + ", " + "1.0" + "\n"

        with open('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueueFDO2109.csv','a') as fd:
            fd.write(myCsvRow)

#The  function mergeCSVs() merges the data about system utilization, queue and mos, in one csv file. 
def mergeCSVs():
    df1 = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')
    df2 = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtil2.csv')
    merged = df1.merge(df2)
    merged.to_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandUtil2512.csv', mode='a', header=False, index=False)
    

#The function plotEcdfQueueSizes(testNames) was used to plot the ECDF of all the queue values in the simulations in [bits], see Figure 18 in the paper.
def plotEcdfQueueSizes(testNames):

    fig, axes = plt.subplots(1, 2, figsize=(10,6))
   
    data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')

    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' app':'application'}, inplace = True)
    data.rename(columns = {' tp':'Throughput [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' host', '', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace('VIP', 'VoIP', regex=True)
    data = data.replace('VID', 'VoD', regex=True)
    data = data.replace(' 5B', '5BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)
    queueSizes = ["10BDP","BDP","Tiny Buffer"]
    granularities = [0, 1]
    throughputs = data["Throughput [% of the $Tp_{ref}$]"].unique()
    applications  = ["VoD","LVD","VoIP","FDO"]
    linestyles = ['--', '-', '-.', ':']
    colors = ["#fde725e5", "#35b779e5", "#31688ee5", "#440154e5"]

    for gran in granularities:
        for app in applications: 
            MOSforDifferentQueues = []
            STDforDifferentQueues= []
            barsMOS = pd.DataFrame()
            barsSTD = pd.DataFrame()
            df=pd.DataFrame()
            df=data.loc[data['granularity'] == gran]
            df=df.loc[df['application'] == app]
            print(df)

            values, counts = np.unique( df[" Queue"], return_counts=True)
            probabilities = counts / counts.sum()
            
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            # Plot the CDF
            plt.rcdefaults()
            axes[granularities.index(gran)].step(values, cdf, where='post', label= app, linewidth=2.5, linestyle=linestyles[applications.index(app)], color=colors[applications.index(app)])
            axes[granularities.index(gran)].set_xlabel(xlabel="Queue size [bits]",labelpad=15,fontsize=17)
            axes[granularities.index(gran)].tick_params(axis='x', labelsize=15)
            axes[granularities.index(gran)].tick_params(axis='y', labelsize=15)
            axes[granularities.index(gran)].xaxis.get_offset_text().set_fontsize(14)
            axes[granularities.index(gran)].legend(fontsize=17)
            axes[granularities.index(gran)].ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
      
            if gran == 0:
                granu = " Flow"
            else:
                granu = " Slice"
            axes[granularities.index(gran)].set_title("Granularity: per" + granu, fontsize=17)
            axes[0].set_ylabel(ylabel="ECDF",fontsize=17)
            
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "ECDFqueueSizesV2" + ".png", bbox_inches='tight'  ) 

def plotFacetsBarPlotsv2(testNames,keyword):

    plt.style.use('default')
    fig, axes = plt.subplots(4, 2, figsize=(15, 15))
    matplotlib.rcParams['hatch.linewidth'] = 0.25
    if keyword == " MOS":
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')
    else:
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtil2.csv')
    print(data)
    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' app':'application'}, inplace = True)
    data.rename(columns = {' tp':'Link Capacity [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' host', '', regex=True)
    data = data.replace('VIP', 'VoIP', regex=True)
    data = data.replace('VID', 'VoD', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace(' 5B', '5BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)
    queueSizes = ["10BDP","BDP","Tiny Buffer", "Rcwnd"]
    granularities = [0, 1]
    throughputs = data["Link Capacity [% of the $Tp_{ref}$]"].unique()
    throughputs = np.array([50,70,90,110,130,150])
    applications  = ["VoD", "LVD", "VoIP", "FDO"]

    for app in applications: 
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        for gran in granularities:
            MOSforDifferentQueues = []
            STDforDifferentQueues= []
            barsMOS = pd.DataFrame()
            barsSTD = pd.DataFrame()
            for queueSize in queueSizes: 
                MOSforDifferentQueues = []
                STDforDifferentQueues= []
                
                for tp in throughputs:
                    if queueSize == "Tiny Buffer" and gran==0: 
                        MOSforDifferentQueues.append(float("nan"))
                        STDforDifferentQueues.append(float("nan"))
                        continue
                   
                    df=pd.DataFrame()
                    print(df)
                    df=data.loc[data['Queue size'] == queueSize]
                    df=df.loc[df['granularity'] == gran]
                    df=df.loc[df['application'] == app]
                    df=df.loc[df["Link Capacity [% of the $Tp_{ref}$]"] == tp]
                    try:
                        MOSforDifferentQueues.append(statistics.mean(df[keyword]))
                        mean, margin_of_error = calculate_confidence_interval(df[keyword])
                        STDforDifferentQueues.append(margin_of_error)
                    except:
                        print(queueSize)
                    
             
                barsMOS.insert(loc=0, column=queueSize, value=pd.Series(MOSforDifferentQueues))
                barsMOS.set_index(throughputs)
                barsSTD.insert(loc=0, column=queueSize, value=pd.Series(STDforDifferentQueues))
                barsSTD.set_index(throughputs)
            
            barsMOS.insert(loc=0, column="Link Capacity [% of the $Tp_{ref}$]", value=pd.Series(throughputs))
            barsSTD.insert(loc=0, column="Link Capacity [% of the $Tp_{ref}$]", value=pd.Series(throughputs))

          
            #colors = ['#1f77b490', '#ff7f0e90', '#2ca02c90','#d6272890'] #matplotlib default
            #colors = ["#440154b3", "#31688eb3", "#35b779b3", "#fde725b3"] #viridis
            colors = ["#fde725b3","#35b779b3","#31688eb3","#440154b3"] #viridis with transparency to make it look less agressive
           

            textures = ["",'//', '\\','/']
            color_texture_map = {color: texture for color, texture in zip(colors, textures)}

            barsMOS.plot(x="Link Capacity [% of the $Tp_{ref}$]", y=["Tiny Buffer","BDP", "10BDP","Rcwnd"],color=colors, kind="bar",edgecolor='black',linewidth=0.8,yerr=barsSTD[["Tiny Buffer","BDP","10BDP","Rcwnd"]].to_numpy().T, ax=axes[applications.index(app),gran],legend=False,width=0.8, capsize=2,error_kw={'elinewidth': 1, 'ecolor': 'black','capthick': 0.5},align='center') 
          
            for bar in axes[applications.index(app), gran].patches:
                face_color_hex = '#{:02x}{:02x}{:02x}{:02x}'.format(
                    int(bar.get_facecolor()[0] * 255),
                    int(bar.get_facecolor()[1] * 255),
                    int(bar.get_facecolor()[2] * 255),
                    int(bar.get_facecolor()[3] * 255)  
                )
            
                if face_color_hex in color_texture_map:
                    bar.set_hatch(color_texture_map[face_color_hex])
              
            bar.set_hatch('default_hatch_pattern') 
            bar.set_hatch(color_texture_map[face_color_hex])
            if applications.index(app) ==0:
                if gran == 0:
                    granularity="Flow"
                else:
                    granularity="Slice"
                axes[applications.index(app),gran].set_title('Granularity: per ' + granularity,fontsize=17)
                
            if applications.index(app) != len(applications)-1: 
                axes[applications.index(app),gran].tick_params(labelbottom=False)
                axes[applications.index(app),gran].set(xlabel=None)
                
            if keyword == " MOS":
                axes[applications.index(app),gran].set_yticks([1.0,2.0,3.0,4.0,5.0])
                axes[applications.index(app),0].set_ylabel("MOS " + app,fontsize=16)
            else:
                 axes[applications.index(app),gran].set_yticks([0,0.5,1.0])
                 axes[applications.index(app),gran].set_ylim([0,1.0])
                 axes[applications.index(app),0].set_ylabel("SU " + app,fontsize=18)
            axes[applications.index(app),gran].tick_params(axis='y', labelsize=16)
            axes[applications.index(app),gran].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
            axes[applications.index(app),gran].tick_params(axis='x', labelsize=16)
            axes[applications.index(app),gran].grid(axis='y',linewidth=0.3)
            axes[applications.index(app),gran].set_axisbelow(True)
            axes[applications.index(app),gran].xaxis.label.set_size(17)
  
        lines_labels = [axes[0,0].get_legend_handles_labels()]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        fig.legend(lines, labels, loc='lower center', ncol=4, fontsize=18)

        fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "BarsFacetsTESTConfInt" + keyword +".png",bbox_inches='tight' )  


                    
          
def plotFacetsBarPlotsQuantizationFDO(testNames,keyword):
    fig, axes = plt.subplots(1, 1, figsize=(12, 5.5)) #, figsize=(12, 11)
    matplotlib.rcParams['hatch.linewidth'] = 0.25
    if keyword == " MOS":
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOS0409.csv')
    else:
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtil2.csv')
  
    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' app':'application'}, inplace = True)
    data.rename(columns = {' tp':'Link Capacity [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' host', '', regex=True)
    data = data.replace('VIP', 'VoIP', regex=True)
    data = data.replace('VID', 'VoD', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace(' 5B', '5BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)
    queueSizes = ["10BDP","BDP","Tiny Buffer"]
    queueSizes = ["BDP"]
    granularities = [" F"]
    throughputs = data["Link Capacity [% of the $Tp_{ref}$]"].unique()
    throughputs = np.array([50,60,70,75,80,81,90,100,106,107,108,110,120,130,140,150])
    applications  = ["FDO"]
    for app in applications: 
        for gran in granularities:
            MOSforDifferentQueues = []
            STDforDifferentQueues= []
            barsMOS = pd.DataFrame()
            barsSTD = pd.DataFrame()
            for queueSize in queueSizes: 
                MOSforDifferentQueues = []
                STDforDifferentQueues= []
                
                for tp in throughputs:
                    if queueSize == "Tiny Buffer" and gran==0: 
                        MOSforDifferentQueues.append(float("nan"))
                        STDforDifferentQueues.append(float("nan"))
                        continue
                   
                    df=pd.DataFrame()
                    df=data.loc[data['Queue size'] == queueSize]
                    df=df.loc[df['granularity'] == gran]
                    df=df.loc[df['application'] == app]
                    df=df.loc[df["Link Capacity [% of the $Tp_{ref}$]"] == tp]
                    
                    MOSforDifferentQueues.append(statistics.mean(df[keyword]))
                    mean, margin_of_error = calculate_confidence_interval(df[keyword])
                    STDforDifferentQueues.append(margin_of_error)
                    
                barsMOS.insert(loc=0, column=queueSize, value=pd.Series(MOSforDifferentQueues))
                barsMOS.set_index(throughputs)
                barsSTD.insert(loc=0, column=queueSize, value=pd.Series(STDforDifferentQueues))
                barsSTD.set_index(throughputs)
            
            barsMOS.insert(loc=0, column="Link Capacity [% of the $Tp_{ref}$]", value=pd.Series(throughputs))
            barsSTD.insert(loc=0, column="Link Capacity [% of the $Tp_{ref}$]", value=pd.Series(throughputs))
            colors = ['#ff7f0e95']
            colors = ["#35b779e5"]
            textures = ["",'//', '\\' ]
            textures = ['//']

            color_texture_map = {color: texture for color, texture in zip(colors, textures)}
            barsMOS.plot(x="Link Capacity [% of the $Tp_{ref}$]", y=["BDP"],color=colors, kind="bar",edgecolor='black',linewidth=0.3,yerr=barsSTD[["BDP"]].to_numpy().T, ax=axes,legend=True,width=0.5, capsize=0.5,error_kw={'elinewidth': 0.5, 'ecolor': 'black','capthick': 0.5},align='center') 

            for bar in axes.patches:
                face_color_hex = '#{:02x}{:02x}{:02x}{:02x}'.format(
                    int(bar.get_facecolor()[0] * 255),
                    int(bar.get_facecolor()[1] * 255),
                    int(bar.get_facecolor()[2] * 255),
                    int(bar.get_facecolor()[3] * 255)  
                )
                
                if face_color_hex in color_texture_map:
                    bar.set_hatch(color_texture_map[face_color_hex])
              
            bar.set_hatch('default_hatch_pattern') 
            bar.set_hatch(color_texture_map[face_color_hex])
            if applications.index(app) ==0:
                if gran == 0:
                    granularity="Flow"
                else:
                    granularity="Slice"
            
            
            if keyword == " MOS":
                axes.set_yticks([1.0,2.0,3.0,4.0])
                axes.set_ylabel("MOS " + app,fontsize=18)
                axes.set_xlabel("Link Capacity [% of the $Tp_{ref}$]",fontsize=18)
        
            axes.tick_params(axis='y', labelsize=17)
            axes.tick_params(axis='x', labelsize=17)
           
            axes.grid(axis='y',linewidth=0.3)
            
            axes.set_axisbelow(True)
            axes.xaxis.label.set_size(18)
            axes.legend().set_visible(False)
        
        fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "BarsFacetsV7ConfInt" + keyword +".png", bbox_inches='tight'  ) #, bbox_inches='tight'  

def plotFacetsBarPlots(testNames,keyword):

    plt.style.use('default')
    fig, axes = plt.subplots(4, 2, figsize=(15, 15)) #12,13.5
    matplotlib.rcParams['hatch.linewidth'] = 0.25
    if keyword == " MOS":
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')
    else:
        data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtil2.csv')
    print(data)
    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' app':'application'}, inplace = True)
    data.rename(columns = {' tp':'Throughput [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' host', '', regex=True)
    data = data.replace('VIP', 'VoIP', regex=True)
    data = data.replace('VID', 'VoD', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace(' 5B', '5BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)
    queueSizes = ["10BDP","BDP","Tiny Buffer","Rcwnd"]
    granularities = [0, 1]
    throughputs = data["Throughput [% of the $Tp_{ref}$]"].unique()
    throughputs = np.array([50,70,90,110,130,150])
    applications  = ["VoD", "LVD", "VoIP", "FDO"]

    for app in applications: 
        for gran in granularities:
            MOSforDifferentQueues = []
            STDforDifferentQueues= []
            barsMOS = pd.DataFrame()
            barsSTD = pd.DataFrame()
            for queueSize in queueSizes: 
                MOSforDifferentQueues = []
                STDforDifferentQueues= []
                
                for tp in throughputs:
                    if queueSize == "Tiny Buffer" and gran==0: 
                        MOSforDifferentQueues.append(float("nan"))
                        STDforDifferentQueues.append(float("nan"))
                        continue
                   
                    df=pd.DataFrame()
                    df=data.loc[data['Queue size'] == queueSize]
                    df=df.loc[df['granularity'] == gran]
                    df=df.loc[df['application'] == app]
                    df=df.loc[df["Throughput [% of the $Tp_{ref}$]"] == tp]
                    try:
                        MOSforDifferentQueues.append(statistics.mean(df[keyword]))
                        mean, margin_of_error = calculate_confidence_interval(df[keyword])
                        STDforDifferentQueues.append(margin_of_error)
                    except:
                        print("no data")
             
                barsMOS.insert(loc=0, column=queueSize, value=pd.Series(MOSforDifferentQueues))
                barsMOS.set_index(throughputs)
                barsSTD.insert(loc=0, column=queueSize, value=pd.Series(STDforDifferentQueues))
                barsSTD.set_index(throughputs)
            
            barsMOS.insert(loc=0, column="Throughput [% of the $Tp_{ref}$]", value=pd.Series(throughputs))
            barsSTD.insert(loc=0, column="Throughput [% of the $Tp_{ref}$]", value=pd.Series(throughputs))

            colors = ['#1f77b495', '#ff7f0e95', '#2ca02c95']
            colors = ['#1f77b490', '#ff7f0e90', '#2ca02c90','#d6272890']

            textures = ["",'//', '\\' ,"///"]
            color_texture_map = {color: texture for color, texture in zip(colors, textures)}
            fig.subplots_adjust(hspace=0.13) 
            fig.subplots_adjust(wspace=0.1) 
            barsMOS.plot(x="Throughput [% of the $Tp_{ref}$]", y=["Tiny Buffer","BDP", "10BDP","Rcwnd"],color=colors, kind="bar",edgecolor='black',linewidth=0.3,yerr=barsSTD[["Tiny Buffer","BDP","10BDP","Rcwnd"]].to_numpy().T, ax=axes[applications.index(app),gran],legend=False,width=0.7, capsize=0.5,error_kw={'elinewidth': 0.5, 'ecolor': 'black','capthick': 0.5},align='center') 
          
            for bar in axes[applications.index(app), gran].patches:
                face_color_hex = '#{:02x}{:02x}{:02x}{:02x}'.format(
                    int(bar.get_facecolor()[0] * 255),
                    int(bar.get_facecolor()[1] * 255),
                    int(bar.get_facecolor()[2] * 255),
                    int(bar.get_facecolor()[3] * 255)  
                )
              
                if face_color_hex in color_texture_map:
                    bar.set_hatch(color_texture_map[face_color_hex])
              
            bar.set_hatch('default_hatch_pattern') 
            bar.set_hatch(color_texture_map[face_color_hex])
            if applications.index(app) ==0:
                if gran == 0:
                    granularity="Flow"
                else:
                    granularity="Slice"
                axes[applications.index(app),gran].set_title('Granularity: per ' + granularity,fontsize=22)
                
            if applications.index(app) != len(applications)-1: 
                axes[applications.index(app),gran].tick_params(labelbottom=False)
                axes[applications.index(app),gran].set(xlabel=None)
                
            if keyword == " MOS":
                axes[applications.index(app),gran].set_yticks([1.0,2.0,3.0,4.0,5.0])
                axes[applications.index(app),0].set_ylabel("MOS " + app,fontsize=20)
            else:
                 axes[applications.index(app),gran].set_yticks([0,0.5,1.0])
                 axes[applications.index(app),gran].set_ylim([0,1.0])
                 axes[applications.index(app),0].set_ylabel("SU " + app,fontsize=20)
            axes[applications.index(app),gran].tick_params(axis='y', labelsize=18)
            axes[applications.index(app),gran].tick_params(axis='x', labelsize=18)
            axes[applications.index(app),gran].grid(axis='y',linewidth=0.3)
            axes[applications.index(app),gran].set_axisbelow(True)
            axes[applications.index(app),gran].xaxis.label.set_size(19)
  
        lines_labels = [axes[0,0].get_legend_handles_labels()]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        fig.legend(lines, labels, loc='lower center', ncol=4, fontsize=22)

        fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "BarsFacetsV3ConfInt" + keyword +".png")  

def calculate_confidence_interval(data, confidence=0.95):
    data = np.array(data)
    mean = np.mean(data)
    sem = stats.sem(data)
    margin_of_error = sem * stats.t.ppf((1 + confidence) / 2., len(data) - 1)
    return mean, margin_of_error
     

#Function plotFacetsBarPlotsSUvsNumCli(testNames) was used to create Figure 10 in the paper. It shows the effects of queue quantization on MOS for FDO clients. 
def plotFacetsBarPlotsSUvsNumCli(testNames): 
    plt.style.use('default')
    fig, axes = plt.subplots(1, 1, figsize=(11,7))
    matplotlib.rcParams['hatch.linewidth'] = 0.25

    data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtilisation.csv')
    
    data.rename(columns = {'n':'Number of clients'}, inplace = True)
    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' app':'application'}, inplace = True)
    data.rename(columns = {' tp':'Throughput [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' host', '', regex=True)
    data = data.replace('VIP', 'VoIP', regex=True)
    data = data.replace('VID', 'VoD', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace(' 5B', '5BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)
    queueSizes = ["10BDP","BDP","Tiny Buffer"]
    numberOfClients = [1,10,20,30,40,50,60,70,80,90,100]
    numberOfClients = [1,20,40,60,80,100]
   
    throughputs = data["Throughput [% of the $Tp_{ref}$]"].unique()
    applications  = ["VoD", "LVD", "VoIP", "FDO"]
    
    barsMOS = pd.DataFrame()
    barsSTD = pd.DataFrame()
    barsMOS.insert(loc=0, column="Number of clients", value=pd.Series(numberOfClients))
    barsSTD.insert(loc=0, column="Number of clients", value=pd.Series(numberOfClients)) 
    for app in applications: 
         
        MOSforDifferentQueues = []
        STDforDifferentQueues= []
        #for gran in granularities:
        errors = []
        
        
        for number in numberOfClients:

            df=pd.DataFrame()
            df=data.loc[data['Number of clients'] == number]
            df=df.loc[df['application'] == app]
            MOSforDifferentQueues.append(statistics.mean(df[" SU"]))
            mean, margin_of_error = calculate_confidence_interval(df[" SU"])
            STDforDifferentQueues.append(margin_of_error)

        barsMOS.insert(loc=0, column=app, value=pd.Series(MOSforDifferentQueues))
        barsMOS.set_index("Number of clients")
        barsSTD.insert(loc=0, column=app, value=pd.Series(STDforDifferentQueues))
        barsSTD.set_index("Number of clients")
       
    colors = ['#1f77b490', '#ff7f0e90', '#2ca02c90','#d6272890']
    colors = ["#fde725e5", "#35b779e5", "#31688ee5", "#440154e5"]
    colors = ["#fde725b3","#35b779b3","#31688eb3","#440154b3"]

    textures = ['/', '', '\\', '///']
    x_pos = np.arange(len(numberOfClients)) 
    barsMOS.plot(x="Number of clients", y=applications,yerr=STDforDifferentQueues, kind="bar",ax=axes,legend=False,width=0.5, color=colors,edgecolor='black',linewidth=0.3, capsize=0.5,error_kw={'elinewidth': 0.5, 'ecolor': 'black','capthick': 0.5},align='center')
    color_texture_map = {color: texture for color, texture in zip(colors, textures)}

    for bar in axes.patches: #match texture with the color
        face_color_hex = '#{:02x}{:02x}{:02x}{:02x}'.format(
            int(bar.get_facecolor()[0] * 255),
            int(bar.get_facecolor()[1] * 255),
            int(bar.get_facecolor()[2] * 255),
            int(bar.get_facecolor()[3] * 255)  
        )
        if face_color_hex in color_texture_map:
            bar.set_hatch(color_texture_map[face_color_hex])
        
    bar.set_hatch('default_hatch_pattern') 
    bar.set_hatch(color_texture_map[face_color_hex])

    axes.set_ylabel("SU",fontsize=17)
    axes.set_xlabel("Number of clients",fontsize=17)
    axes.set_xticks(x_pos)
    axes.set_xticklabels(numberOfClients, fontsize=15)
    axes.tick_params(axis='y', labelsize=15)
   
    axes.grid(axis='y',linewidth=0.3)
   
    lines_labels = [axes.get_legend_handles_labels()]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.subplots_adjust(left=0.2, right=0.95, top=0.9, bottom=0.2, wspace=0.4)
    fig.legend(lines, labels,  loc='upper center', ncol=len(applications), fontsize=18)
    axes.tick_params(axis='x', labelrotation=360)
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "BarsFacetsSUvsNumCliV9" +".png", bbox_inches='tight') 


def extractTPperClient(testNames):
    allData=pd.DataFrame() 
    originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
    nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
    nodeSplit = [0,0,1,0,0,0]
    scenarioMean = []
    scenarioStDev = []
    for testName in testNames: 
        numCLI =  testName.split("n")[1].split("_q")[0]
        queueSizeText = testName.split("q")[1].split("_tp")[0]
        throughputPercentage = testName.split("tp")[1].split("_g")[0]#percetage of the orginial throughput assigned to the application
        granularity = testName.split("g")[1].split("_a")[0]#percetage of the orginial throughput assigned to the application
        application = "host" + testName.split("a")[1]

        if int(throughputPercentage) == 80:
            print(throughputPercentage)
            tp=originalTPperClient["FDO"]*int(throughputPercentage)
            delay = 20

            meanPerClient = []
            AllClients = []
            print("before node iteration")

            nodeMean= []
            nodeStDev = []
            for node in range(int(numCLI)):
                print("Node is " + str(node))
                df = importDFextended(testName, numCLI, nodeTypes, [x*int(numCLI) for x in nodeSplit ], 'throughputs', '_' + "Downlink")
                filtered_df = df.filter(like='FDO')
                nodeMean.append(statistics.mean(filtered_df["Downlink Throughput hostFDO"+str(node)]))
                nodeStDev.append(statistics.stdev(filtered_df["Downlink Throughput hostFDO"+str(node)]))
            print(nodeMean)
            print(nodeStDev)
            if int(numCLI) != 1:
                scenarioMean.append(statistics.stdev(nodeMean))
            else:
                scenarioMean.append(0.0)
            # if int(numCLI) != 1:
            #     scenarioStDev.append(statistics.mean(nodeStDev))
            # else:
            #     scenarioStDev.append(0.0)                 

    totalNumCli=[1,10,20,30,40,50]
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    # plt.ylim(0,2200)
    plt.xlabel("Number of clients")
    plt.ylabel("Throughput")
    plt.errorbar(totalNumCli, scenarioMean, marker='^')
    plt.savefig("../exports/plots/tpvariation_" + testName + ".png")



#The function createCSVwithSU(testNames) extracts the link utilization across all scenarios, similarly to createCSV function
def createCSVwithSU(testNames):

    nodeTypes = ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP']
    originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
    font = {'weight' : 'normal',
        'size'   : 50}
    matplotlib.rc('font', **font)
    prePath = '../exports/extracted/throughputs/'
    runs = {}
    runCliNum = {}
    fig, ax = plt.subplots(1, figsize=(55,11))

    for testName in testNames:
        queueSizeText = testName.split("q")[1].split("_tp")[0]
        granularity = testName.split("g")[1].split("_a")[0]#percetage of the orginial throughput assigned to the application
        application = "host" + testName.split("a")[1]
        throughputPercentage = testName.split("tp")[1].split("_g")[0]#granularity of the resource allocation scheme
        numCli =  testName.split("n")[1].split("_q")[0]
        linkTP = int(throughputPercentage)/100 * int(numCli) * originalTPperClient[testName.split("a")[1]]
        print('-------------', testName, '-------------')
        filenames = glob.glob(prePath+testName+'*Downlink*')
        #print(filenames)
        filterName = 'Throughput'
        df = pd.read_csv(filenames[0])
        df = df.iloc[:, 1:]

        df["Sum"] = df.sum(axis=1, numeric_only=True)
  

        myCsvRow = str(numCli) + ", " + queueSizeText + ", " + str(throughputPercentage) + ", " + granularity + ", " + application + ", " + str(statistics.mean(df["Sum"])/linkTP)  + "\n" #+ ", " + str(statistics.stdev(tempValue))
    
        with open('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtilisation.csv','a') as fd:
            fd.write(myCsvRow)

def queueCost():
    throughputs = [x for x in range(50,110,10)]
    originalTPperClient = OrderedDict([('VIP', 30), ('LVD',1820), ('VID',1120), ('FDO',2240), ('SSH',10),('HVIP', 0)]) #in kbps, based on CNSM heatmaps
    delay = 20
    rcwnd = [65535*8 for x in range(50,110,10)]
    app = "VID"
    bdp1 = [throughput/100 * originalTPperClient[app] * delay *1 for throughput in throughputs]
    bdp10 = [throughput/100 * originalTPperClient[app] * delay *10 for throughput in throughputs]
    bdp100 = [throughput/100 * originalTPperClient[app] * delay *100 for throughput in throughputs]
    tiny10 = [throughput/100 * originalTPperClient[app] * delay *10 /math.sqrt(10) for throughput in throughputs]
    tiny100 = [throughput/100 * originalTPperClient[app] * delay *10 /math.sqrt(100) for throughput in throughputs]
    plt.rcParams.update(plt.rcParamsDefault)
    #plt.plot(throughputs, rcwnd, label = "Rcwnd 1 client", color="moccasin") 
    plt.plot(throughputs, [x*10 for x in  rcwnd], label = "Rcwnd 10 clients", color="orange") 
    #plt.plot(throughputs, [x*100 for x in  rcwnd], label = "Rcwnd 100 clients", color="darkorange") 

    #plt.plot(throughputs, bdp1, label = "BDP 1 client", color = "royalblue" )
    plt.plot(throughputs, bdp10, label = "BDP 10 clients", color = "lightskyblue" )
    #plt.plot(throughputs, bdp100, label = "BDP 100 clients", color = "dodgerblue") 
    plt.plot(throughputs, tiny10, label = "Tiny Buffers 10 clients", color = "brown")
    #plt.plot(throughputs, tiny100, label = "Tiny Buffers 100 client", color =  "firebrick")   
    plt.xlabel("Throughput [% of the $Tp_{ref}$]")
    plt.ylabel("Queue size [bits]")

    plt.legend()
    plt.ticklabel_format(useOffset=False)
    plt.savefig('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/fdo.png') 

def plotFacetsQueue():
    df = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataQueueCopy.csv')
    #df = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataUtilisation.csv')

    df.rename(columns = {' g':'granularity'}, inplace = True)
    df.rename(columns = {' q':'Queue size'}, inplace = True)
    df.rename(columns = {' tp':'Throughput [% of the $Tp_{ref}$]'}, inplace = True)
    df = df.replace(' g', 'granularity', regex=True)
    df = df.replace(' host', '', regex=True)

    df = df.replace(' F', 'per Flow', regex=True)
    df = df.replace(' S', 'per Slice', regex=True)
    
    df = df.replace(' B', 'BDP', regex=True)
    df = df.replace(' T', 'Tiny Buffer', regex=True)
    df = df.replace(' R', 'Rcwnd', regex=True)

    sns.set_context("paper",rc={"font.size":8,"axes.titlesize":8,"axes.labelsize":8,"legend.fontsize":12})   
    sns.set_style("whitegrid")
  
    test = sns.relplot(data=df, x= 'Throughput [% of the $Tp_{ref}$]', y=' QU', hue = 'Queue size', col= "granularity", row=" app", kind = "line", markers=True ,height=1.27, aspect=2.5/1.27, lw=0.5,ci="sd",style="Queue size")
    test.set(ylim=(0, 1))
    
    print("plotting queue3")
    test.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "testqueueFacets" + ".png") 

def plotHeatmapQueueSize():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataQueue.csv')
    
    queueSizeText = [" R", " B", " T"]
    queueSizeText = [" 10B", " B", " T"]
    queueSizeText = [" B", " T"]
    queueSizeText = [" B", " R"]
    queueSizeTextFull = ["BDP","Rcwnd"]


    applications = ["hostVID","hostLVD"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=len(applications), ncols=len(queueSizeText),figsize=(5,8*len(applications)),sharey=True,gridspec_kw={'width_ratios': [1, 1.3]}) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps

    for app in applications:
        for queueSize in queueSizeText:
            fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            print(df[' tp'])
            df=df.loc[df[' g'] == " S"]
            df=df.loc[df[' q'] == queueSize]
            df=df.loc[df[' tp'] == 50]
            print("thus us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data["Queue size"]=df[" TotalQueueSize"]
            queueLabel = []

            for x in data["Queue size"]:
                if x >= 100000:
                    queueLabel.append(str(round(x/1000000, 1)) + "M")
                elif x>=1000 and x < 100000:
                    queueLabel.append(str(round(x/1000, 1)) + "K")
                else:
                    queueLabel.append(str(x))
            data["Queue label"]=queueLabel
            
            data.sort_values(by=['Number of clients'],ascending=False, inplace=True)

            if queueSizeText.index(queueSize) == len(queueSizeText)-1:
                print("This is a last one needs a colorbar")
                sns.heatmap(data.pivot(index='Number of clients', columns='Throughput percentage', values='Queue size'),ax=axes[applications.index(app),queueSizeText.index(queueSize)], vmin=dfOriginal.nsmallest(1, ' TotalQueueSize')[' TotalQueueSize'], vmax=dfOriginal.nlargest(1, ' TotalQueueSize')[' TotalQueueSize'],norm=LogNorm(), annot=data.pivot(index='Number of clients', columns='Throughput percentage', values='Queue label'),annot_kws={'size': 24},fmt ='') #cbar=False
            else:
                print("No color bar")
                sns.heatmap(data.pivot(index='Number of clients', columns='Throughput percentage', values='Queue size'),ax=axes[applications.index(app),queueSizeText.index(queueSize)], vmin=dfOriginal.nsmallest(1, ' TotalQueueSize')[' TotalQueueSize'], vmax=dfOriginal.nlargest(1, ' TotalQueueSize')[' TotalQueueSize'],norm=LogNorm(), annot=data.pivot(index='Number of clients', columns='Throughput percentage', values='Queue label'),cbar=False,annot_kws={'size': 24},fmt = '') #cbar=False
            
            axes[applications.index(app), queueSizeText.index(queueSize)].tick_params(labelsize=18)
            axes[applications.index(app), queueSizeText.index(queueSize)].invert_yaxis()
            axes[0, queueSizeText.index(queueSize)].set_title(queueSizeTextFull[queueSizeText.index(queueSize)], fontsize=24)
            axes[applications.index(app), len(queueSizeText)-1].set(ylabel=None)
            axes[applications.index(app), queueSizeText.index(queueSize)].set(xlabel=None) 
            axes[applications.index(app), 0].xaxis.get_label().set_fontsize(24)
            axes[applications.index(app), 0].xaxis.set_tick_params(labelsize = 18)
            axes[applications.index(app), 0].yaxis.set_tick_params(labelsize = 18)
            axes[applications.index(app), queueSizeText.index(queueSize)].tick_params(labelbottom=False)    
            axes[applications.index(app), 0].yaxis.get_label().set_fontsize(24)
        
        cbar = axes[applications.index(app), len(queueSizeText)-1].collections[0].colorbar
        cbar.ax.tick_params(labelsize=22)  # Adjust tick label size
        cbar.set_label('Queue size [bits]', fontsize=24)  # Adjust colorbar label size
    axes[applications.index(app), 0].tick_params(labelbottom=True) 
    axes[applications.index(app), len(queueSizeText)-1].tick_params(labelbottom=True) 

    fig.text(0.5, 0.079, 'Throughput [% of the $Tp_{ref}$ ]', ha='center', fontsize=24) # + str(originalTPperClient[applications[0]]) + "kbps]"
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "heatmap" + applications[0]+".png",bbox_inches='tight', pad_inches=0.01)  

def plotCDF_MOS():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOS2608.csv')
    
    queueSizeText = [" R", " B", " T"]
    queueSizeText = [" 10B", " B", " T"]
    queueSizeText = [" B", " T"]
    queueSizeText = [" T", " B" , " 5B", " 10B", " R"]
    queueSizeText = [" T", " B" , " 5B"]
    #queueSizeText = [" B"]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","5BDP ","10BDP ","Rcwnd "]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","10BDP"]
    #queueSizeTextFull = ["BDP"]


    applications = ["hostLVD"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]
    for app in applications:
        for queueSize in queueSizeText:
            print(queueSize)
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            #df=df.loc[df[' g'] == granularity]
            df=df.loc[df[' q'] == queueSize]
            df=df.drop_duplicates()
            #df=df.loc[df[' tp'] == 80]
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("this us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" stdev"] = df[" stdev"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            #Plot the CDF with varable length of a line - thinner line means lower tp
            # lwidths=1+values[:-1]
            # lwidths = []
            # widths = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            # allTps = [ 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
            # for tp in data["Throughput percentage"]:
            #     print(allTps.index(tp))
            #     lwidths.append(widths[allTps.index(tp)])
            
            # colors = ['b','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']
            # print(len(lwidths))
            # points = np.array([values, cdf]).T.reshape(-1, 1, 2)
            # segments = np.concatenate([points[:-1], points[1:]], axis=1)
            # lc = LineCollection(segments, linewidths=lwidths, color = colors[queueSizeText.index(queueSize)])
            # axes.add_collection(lc)        
           
            #plt.plot(values, cdf,label=queueSizeTextFull[queueSizeText.index(queueSize)]) #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            #plt.fill_between(values, cdf-data[" stdev"], cdf+data[" stdev"])
            plt.xlabel('MOS',fontsize=16)
            plt.ylabel('ECDF',fontsize=16)
            
            plt.tick_params(axis="both", labelsize=14)
 
            leg = plt.legend(title="Queue size:", fontsize=14,title_fontsize=14)
            leg._legend_box.align = "left"  
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOS" + app +".png",bbox_inches='tight', pad_inches=0.01)  

#This function plots ECDF of MOS values, for different queue sizes including the variation as line thickness. See Figure 9 in the paper. 
def plotECDF_MOS_Variation():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')
    
    queueSizeText = [" T", " B" , " 10B"]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","5BDP ","10BDP ","Rcwnd "]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","10BDP"]
    applications = ["hostVID"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    for app in applications:
        for queueSize in queueSizeText:
            print(queueSize)
            df=dfOriginal[dfOriginal[' app'] == " " + app]

            df=df.loc[df[' q'] == queueSize]
            df=df.drop_duplicates()

            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" stdev"] = df[" stdev"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
            
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
           
            #linestyles = ['-', '-.', ':']      
            colors = ["#fde725", "#35b779", "#31688e", "#440154"]
            colors = ["#440154","#31688e","#35b779","#fde725"]
            plt.plot(values, cdf,label=queueSizeTextFull[queueSizeText.index(queueSize)],linewidth=2,color=colors[queueSizeText.index(queueSize)]) #linestyles #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            # colors = ['#ADD8E6', '#FFDAB9', '#2ca02c70']
            colors = ["#fde725cc", "#35b779cc", "#31688ecc", "#440154cc"]
            #colors = ["#fde725b2", "#35b779b2", "#31688eb2", "#440154b2"]
            colors = ["#440154b3", "#31688eb3", "#35b779b3", "#fde725b3"]

            
            plt.fill_betweenx(cdf, data.groupby(' MOS').apply(lambda x: x.sample(1)).reset_index(drop=True)[" MOS"]-data.groupby(' MOS').apply(lambda x: x.sample(1)).reset_index(drop=True)[" stdev"],data.groupby(' MOS').apply(lambda x: x.sample(1)).reset_index(drop=True)[" MOS"]+data.groupby(' MOS').apply(lambda x: x.sample(1)).reset_index(drop=True)[" stdev"], color=colors[queueSizeText.index(queueSize)] )
            plt.xlabel('MOS',fontsize=17)
            plt.ylabel('ECDF',fontsize=17)
            plt.xlim(0,5)
            plt.ylim(0,1)
            plt.tick_params(axis="both", labelsize=15)
            leg = plt.legend(title="Queue size:", fontsize=17,title_fontsize=17)
            leg._legend_box.align = "left"  
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOS" + app +"v2.png",bbox_inches='tight', pad_inches=0.01)  

#The function plotCDF_MOSbasic() plots ECDF of all MOS values actoss all scenarios. 
def plotCDF_MOSbasic():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')

    queueSizeText = [" T", " B" , " 5B", " 10B", " R"]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","5BDP ","10BDP ","Rcwnd "]


    applications = ["hostFDO"] #"hostVIP","hostLVD","hostVID",
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]
    for app in applications:
        for queueSize in queueSizeText:
            print(queueSize)
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            #df=df.loc[df[' g'] == granularity]
            df=df.loc[df[' q'] == queueSize]
            df=df.drop_duplicates()
            #df=df.loc[df[' tp'] == 80]
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("this us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
      
            plt.plot(values, cdf,label=queueSizeTextFull[queueSizeText.index(queueSize)]) #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            plt.xlabel('MOS')
            plt.ylabel('CDF')
            plt.legend()
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOSbasic" + app +".png",bbox_inches='tight', pad_inches=0.01)  

#The function plotCDFnumCli_MOSbasic() generates Figure 11 in the paper, showing the potential benefits of intraslice multiplexing gain on MOS
def plotCDFnumCli_MOSbasic(): 
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')

    applications = ["hostFDO","hostLVD","hostVIP","hostLVID"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]

    for app in applications:
        numCli= [1]
        numCli.extend([x for x in range (10,110,10)])
        numCli = [1,20,40,80]
        print(numCli)
        dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue0409.csv')
        
        for num in numCli:
            df=pd.DataFrame()
            print(num)
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
           
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            print(df)
            #df=df.loc[df[' g'] == granularity]
            df=df.loc[df['n'] ==num]
            df=df.drop_duplicates()
            #df=df.loc[df[' tp'] == 80]
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("this us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            #Plot the CDF with varable length of a line - thinner line means lower tp
            # lwidths=1+values[:-1]
            # lwidths = []
            # widths = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            # allTps = [ 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
            # for tp in data["Throughput percentage"]:
            #     print(allTps.index(tp))
            #     lwidths.append(widths[allTps.index(tp)])
            
            # colors = ['b','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']
            # print(len(lwidths))
            # points = np.array([values, cdf]).T.reshape(-1, 1, 2)
            # segments = np.concatenate([points[:-1], points[1:]], axis=1)
            # lc = LineCollection(segments, linewidths=lwidths, color = colors[queueSizeText.index(queueSize)])
            # axes.add_collection(lc)        
            #colors=["mediumblue", "darkmagenta","teal"]
            #colors=["midnightblue","mediumblue","blue"]
            colors = ['#1f77b4e6', '#ff7f0ee6', '#2ca02ce6', '#d62728e6']
            colors = ["#fde725e5", "#35b779e5", "#31688ee5", "#440154e5"]
            colors = ["#440154b3", "#31688eb3", "#35b779b3", "#fde725b3"]
            linestyles= ["solid", "dashed", "dotted", "-."]
            plt.plot(values, cdf,label= str(num), linewidth=2.5, color=colors[numCli.index(num)]) # , linestyle=linestyles[numCli.index(num)]label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            plt.xlabel('MOS', fontsize=17)
            plt.xlim(0,5)
            plt.ylabel('ECDF',fontsize=17)
            plt.tick_params(axis="both", labelsize=15)
            plt.tight_layout()
            #plt.legend(title="Number of " + app.replace("host","") + " clients:", fontsize=14,loc="center",title_fontsize=14)
            if app != "hostVIP":
                plt.legend(title="Number of clients:",  ncol=1, fontsize=16,loc="upper left",title_fontsize=17)._legend_box.align = "left" #+ app.replace("host","")
        # lines_labels = [axes.get_legend_handles_labels()]
        # lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        # fig.legend(lines, labels, loc='lower center',title="Number of " + app.replace("host","") + " clients:")
        fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOSnumCLIbasicTEST" + app +".png",bbox_inches='tight', pad_inches=0.01)  
        plt.clf()

def plotCDF_MOS_granularityThickness():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOS2608.csv')

    
    queueSizeText = [" R", " B", " T"]
    queueSizeText = [" 10B", " B", " T"]
    queueSizeText = [" B", " T"]
    queueSizeText = [" T", " B" , " 5B", " 10B", " R"]
    queueSizeText = [" T", " B" , " 5B"]
    queueSizeText = [ " B" , " 5B"]
    #queueSizeText = [" B"]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","5BDP ","10BDP ","Rcwnd "]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","5BDP"]
    queueSizeTextFull = ["BDP ","5BDP"]
    #queueSizeTextFull = ["BDP"]


    applications = ["hostFDO"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]
    for app in applications:
        for queueSize in queueSizeText:
            print(queueSize)
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            #df=df.loc[df[' g'] == granularity]
            df=df.loc[df[' q'] == queueSize]
            df=df.drop_duplicates()
            #df=df.loc[df[' tp'] == 80]
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("this us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            data["Granularity"] = df[" g"]

            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            #Plot the CDF with varable length of a line - thinner line means lower tp
            lwidths=1+values[:-1]
            lwidths = []
            widths = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            widths = [1,7]
            allTps = [ 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
            allGranularities = [" F", " S"]
            for g in data["Granularity"]:
                print(allGranularities.index(g))
                lwidths.append(widths[allGranularities.index(g)])
            
            colors = ['b','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']
            print(len(lwidths))
            points = np.array([values, cdf]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, linewidths=lwidths, color = colors[queueSizeText.index(queueSize)])
            axes.add_collection(lc)        
           
            plt.plot(values, cdf,label=queueSizeTextFull[queueSizeText.index(queueSize)] + app) #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            plt.xlabel('MOS')
            plt.ylabel('CDF')
            plt.legend()
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOSGranularityThicknessV2" + app +".png",bbox_inches='tight', pad_inches=0.01)  

def plotCDF_MOS_numberCliThickness():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOS2608.csv')

    queueSizeText = [" T", " B" , " 10B"]
    queueSizeTextFull = ["Tiny Buffer ","BDP ","10BDP "]
   
    applications = ["hostFDO"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]
    for app in applications:
        for queueSize in queueSizeText:
            print(queueSize)
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            #df=df.loc[df[' g'] == granularity]
            df=df.loc[df[' q'] == queueSize]
            df=df.drop_duplicates()
            #df=df.loc[df[' tp'] == 80]
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("this us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            data["Granularity"] = df[" g"]

            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)
            data=data.sort_values(by=[" MOS"])
            probabilities = counts / counts.sum()
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            #Plot the CDF with varable length of a line - thinner line means lower tp
            lwidths=1+values[:-1]
            lwidths = []
            widths = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            allNumCli = [ 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
          
            for numCli in data["Number of clients"]:
                lwidths.append(widths[allNumCli.index(numCli)])
            
            colors = ['b','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']
            print(len(lwidths))
            points = np.array([values, cdf]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, linewidths=lwidths, color = colors[queueSizeText.index(queueSize)])
            axes.add_collection(lc)        
           
            plt.plot(values, cdf,label=queueSizeTextFull[queueSizeText.index(queueSize)] + app) #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            plt.xlabel('MOS')
            plt.ylabel('CDF')
            plt.legend()
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfMOSGranularityNumCliV2" + app +".png",bbox_inches='tight', pad_inches=0.01)  

    
def plotCDF_TpVsMOS():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOS.csv')
    
    queueSizeText = [" R", " B", " T"]
    throughputs = [ 50, 60, 70, 80, 90, 100]

    applications = ["hostVIP"]
    sns.reset_defaults()
    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps
    #g = [" F", " S"]
    for app in applications:
        for tp in throughputs:
            #for granularity in g:
            #fig.subplots_adjust(wspace=0.03, hspace=0.1)
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            print(df[' tp'])
            #df=df.loc[df[' g'] == granularity]
            #df=df.loc[df[' q'] == queueSize]
            df=df.loc[df[' tp'] == tp]
            df=df.drop_duplicates()
            #df=df.loc[df['n'] == 50]
            #df=df.loc[df['n'] == 50]
            print("thus us filtered data frame")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
           
            values, counts = np.unique(data[" MOS"], return_counts=True)

            sortedTP= [x for _, x in sorted(zip(values, data["Throughput percentage"]))]
            print(sortedTP)
            probabilities = counts / counts.sum()
            
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            
            plt.plot(values, cdf,label= "tp"+ str(tp) + "%_" + app) #label=queueSizeTextFull[queueSizeText.index(queueSize)] + app + granularity
            
            plt.xlabel('MOS')
            plt.ylabel('CDF')
            plt.legend()
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "cdfTpvsMOS" + app +".png",bbox_inches='tight', pad_inches=0.01)  


#The function plotCDF_gVsMOS() is used to compare two different granularities of the resource allocation schemes with respect to the achieved MOS. Additionally, line thicknes can denote the available throughput. 
def plotCDF_gVsMOS():
    df=pd.DataFrame()
    labels=pd.DataFrame()
    dfOriginal = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')

    granularity= [" F"," S"]
    granularity= [ 0, 1]
    applications = ["hostFDO"]
    sns.reset_defaults()

    fig, axes = plt.subplots(nrows=1, ncols=1) #
    originalTPperClient = OrderedDict([('hostVIP', 30), ('hostLVD',1820), ('hostVID',1120), ('hostFDO',2240), ('hostSSH',10),('hostHVIP', 0)]) #in kbps, based on CNSM heatmaps


    for app in applications:
        for g in granularity:
            df=dfOriginal[dfOriginal[' app'] == " " + app]
            df=df.loc[df[' g'] == g]
            print("This is filtered dataframe based on the application and granularity")
            print(df)
            data = pd.DataFrame()
            data["Number of clients"] = df["n"]
            data["Throughput percentage"] = df[" tp"]
            data[" MOS"] = df[" MOS"]
            queueLabel = []
        
            values, counts = np.unique(data[" MOS"], return_counts=True)
            probabilities = counts / counts.sum()
            
            # Calculate the CDF
            cdf = np.cumsum(probabilities)
            data=data.sort_values(' MOS')
            print(data)
            lwidths=1+values[:-1]
            lwidths = []
            widths = [1,2,3,4,5,6,7,8,9,10,11,12,13]

            allNumCli = [ 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            allTPs= [x for x in range (50,160,10)]
            #thickness of the line indicates the available capacity in that scenario
            for tp in data["Throughput percentage"]:
                lwidths.append(widths[allTPs.index(tp)])

            #t hickness of the line indicates the number of clients in that scenario
            # for n in data["Number of clients"]:
            #     #print(n)
            #         lwidths.append(widths[allNumCli.index(n)])

            #colors = ['#1f77b490', '#ff7f0e90', '#2ca02c90', '#d6272890']
            colors = [ "#35b779e5", "#440154e5"]
   
            points = np.array([values, cdf]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, linewidths=lwidths, color = colors[granularity.index(g)])
            axes.add_collection(lc)        
           
            if g == 0:
                g = " Flow"
                a=0
            else:
                g = " Slice"
                a=1
            plt.tick_params(axis='both', labelsize=16)    

            plt.plot(values, cdf,label= "Granularity: per" + str(g), color=colors[granularity.index(a)]) 
            plt.xlim(1.00,4.5)
            plt.xlabel('MOS', fontsize=17)
            plt.ylabel('ECDF', fontsize=17)
            plt.legend(fontsize=17)
            plt.grid(True)
    
    fig.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/" + "ThickNumClicdfgMOSV4" + app +".png",bbox_inches='tight', pad_inches=0.01)  

#This function (plotTpMOS35()) plots minimum throughout needed to reach QoE of 3.5 for all application and different queue sizes
def plotTpMOS35():  
    data = pd.read_csv('/mnt/data/improved5gNS/analysis/exports/extracted/mos2/dataMOSandQueue1609.csv')
    data.rename(columns = {' g':'granularity'}, inplace = True)
    data.rename(columns = {' q':'Queue size'}, inplace = True)
    data.rename(columns = {' tp':'Throughput [% of the $Tp_{ref}$]'}, inplace = True)
    data = data.replace(' g', 'granularity', regex=True)
    data = data.replace(' host', '', regex=True)
    data = data.replace(' F', 'per Flow', regex=True)
    data = data.replace(' S', 'per Slice', regex=True)
    data = data.replace(' B', 'BDP', regex=True)
    data = data.replace(' 10B', '10BDP', regex=True)
    data = data.replace(' T', 'Tiny Buffer', regex=True)
    data = data.replace(' R', 'Rcwnd', regex=True)

    queueSizes = ["BDP","10BDP"]
    queueSizes = ["Tiny Buffer","BDP","10BDP"]
    plt.style.use('default')
    fig, ax = plt.subplots()
    app = "FDO"
    for queueSize in queueSizes: 
        
        df=pd.DataFrame()
        tpMOS35=[]
        df=data.loc[data['Queue size'] == queueSize]
        df=df.loc[df['granularity'] == 1]
        df=df.loc[df[' app'] == app]

        if queueSize == "Tiny Buffer":
             tpMOS35.append(float("nan"))
        for n in df['n'].unique():
            dfProcessed= df.loc[df['n'] == n]
            flagTP35 = 0

            for index, row in dfProcessed.iterrows():
                print(row["Throughput [% of the $Tp_{ref}$]"])
                print(row[" MOS"])
                if row[" MOS"] >= 3.5:
                    tpMOS35.append(row["Throughput [% of the $Tp_{ref}$]"])
                    flagTP35 = 1
                    break
            if not flagTP35:
                print("appending NAN")
                tpMOS35.append(float("nan"))

        print(tpMOS35)
        if queueSizes.index(queueSize) == 0:
            bars = pd.DataFrame({queueSize: tpMOS35 })
        else:
            column_values = pd.Series(tpMOS35)
            bars.insert(loc=0, column=queueSize, value=column_values)
        plt.style.use('default')
        m = ['o', 'x','s']
        l = ["solid","dashed","dotted"]
    bars.insert(loc=0, column="Number of clients", value=df['n'].unique())
    colors = ['#1f77b495', '#ff7f0e95', '#2ca02c95']
    colors = ["#fde725e5", "#35b779e5", "#31688ee5"]
    textures = ["",'//', '\\' ]
    color_texture_map = {color: texture for color, texture in zip(colors, textures)}
    matplotlib.rcParams['hatch.linewidth'] = 0.25
    ax = bars.plot(x="Number of clients", y=["Tiny Buffer","BDP", "10BDP"], kind="bar", edgecolor='black',fontsize=18,legend=False,color=colors,linewidth=0.3,width=0.7)
    for bar in ax.patches:
        face_color_hex = '#{:02x}{:02x}{:02x}{:02x}'.format(
            int(bar.get_facecolor()[0] * 255),
            int(bar.get_facecolor()[1] * 255),
            int(bar.get_facecolor()[2] * 255),
            int(bar.get_facecolor()[3] * 255)  
        )
       
        if face_color_hex in color_texture_map:
            bar.set_hatch(color_texture_map[face_color_hex])
        
        bar.set_hatch('default_hatch_pattern')  
        bar.set_hatch(color_texture_map[face_color_hex])
    x_positions = []
    for bar in ax.patches:
        x_positions.append(bar.get_x() + bar.get_width() / 2)
    print(x_positions)
    print(bars['Number of clients'])
    print(bars["Tiny Buffer"])
    ax.plot(x_positions[:11],bars["Tiny Buffer"], linestyle='dashed', zorder=5, label="_", color="#fde725e5")
    ax.plot(x_positions[11:22],bars["BDP"], linestyle='dashed', zorder=5, label="_",color="#35b779e5")
    ax.plot(x_positions[22:33],bars["10BDP"], linestyle='dashed', zorder=5, label="_",color="#31688ee5")
   
    ax.set_ylabel("$C_{min}$", fontsize = 19)
    ax.set_xlabel("Number of clients", fontsize = 19)
    ax.set_ylim(0,150)
    #legend = ax.legend(bbox_to_anchor=(0.162,0.85015), loc="lower left", bbox_transform=fig.transFigure, ncol=3, fontsize = 14.4)
    ax.figure.savefig("/mnt/data/improved5gNS/analysis/exports/extracted/mos2/tpNeededforQoE35v2" + "a" + app + ".png",bbox_inches='tight')


#Function plotCorrelationMatrixAggregated() was used to create heatmaps shown in Figures 5 and 6 in the paper. 

def plotCorrelationMatrixAggregated(): 
    applications = ["Overall","hostVoD","hostLVD","hostVoIP","hostFDO"]
    fig, axs = plt.subplots(5,figsize=(12, 9))#
    type = "spearman"
    for app in applications: 
        print(app)
        df=pd.DataFrame()
        df = pd.read_csv('../exports/extracted/mos2/dataMOSandUtil2512.csv') #EDIT path if you have different folder structure 
        df[' q']=df[' q'].astype('category').cat.codes
        df=df[["n"," tp"," Queue",  " g", " MOS", " stdev", " app", " SU"]] #, " g"
        df = df.replace('VIP', 'VoIP', regex=True)
        df = df.replace('VID', 'VoD', regex=True)
        df = df.rename(columns={'n': 'Number of \n clients', ' tp': 'Throughput', " g": "Granularity" ,' app': 'Application type',  ' MOS': 'MOS Mean', ' stdev': 'MOS SD', " SU": "Sys. Util."}) #' g': 'Granularity',
        if app != "Overall":
            df=df.loc[df['Application type'] == " " + app]

        axs[applications.index(app)].matshow(df.corr(method=type).iloc[4:,:4], vmin=-1, vmax=1,aspect='auto') #select rows with nuber 5,6,7, 
        axs[0].set_xticks(range(df.iloc[4:,:4].select_dtypes(['number']).shape[1]))#,)
        axs[applications.index(app)].set_yticks(range(df.corr(method=type).iloc[:,-3:].select_dtypes(['number']).shape[1])) #select last three columns
        axs[applications.index(app)].set_ylabel(app.replace("host",""))

        axs[0].set(xticklabels=df.iloc[4:,:4].select_dtypes(['number']).columns)
        axs[applications.index(app)].tick_params(axis='x',labelsize=19)  #,rotation=22.5
        axs[applications.index(app)].tick_params(axis='y',labelsize=19) 
        axs[applications.index(app)].set_yticks(range(df.corr(method=type).iloc[4:,-3:].select_dtypes(['number']).shape[1]))
        axs[applications.index(app)].set_xticks([])
        plt.tight_layout()
        if app != "Overall":
            axs[applications.index(app)].set_ylabel(app.replace("host",""),rotation=-90,labelpad=20, fontsize=19)
        else:
            axs[applications.index(app)].set_ylabel(app,rotation=-90,labelpad=20, fontsize=19)

        axs[applications.index(app)].yaxis.set_label_position("right")
        axs[applications.index(app)].set(yticklabels=df.corr(method=type).iloc[:,-3:].select_dtypes(['number']).columns)
        for (x, y), value in np.ndenumerate(df.corr(method=type).iloc[:-3,-3:]):
            if value > -0.59:
                axs[applications.index(app)].text(x, y, f"{value:.3f}", va="center", ha="center", fontsize=17)
            else:
                axs[applications.index(app)].text(x, y, f"{value:.3f}", va="center", ha="center", color="white",fontsize=17)


    cmap = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([]) 

    cbar = fig.colorbar(sm, ax=axs.ravel().tolist(), shrink=0.95)
    cbar.ax.tick_params(labelsize=17)

    fig.savefig("../exports/extracted/mos2/" + "correlationAggregatedV3" + type + ".png") 

def plotCorrelationMatrixAggregatedV2(): 
    applications = ["Overall","hostVoD","hostLVD","hostVoIP","hostFDO"]
    fig, axs = plt.subplots(5,figsize=(18, 13))#
    fig.subplots_adjust(hspace=0.001)
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, hspace=0.3)

    
    type = "pearson"
    for app in applications: 
        print(app)
        df=pd.DataFrame()
        df = pd.read_csv('../exports/extracted/mos2/dataMOSandUtil2512.csv') #EDIT path if you have different folder structure 
        df[' q']=df[' q'].astype('category').cat.codes
        df=df[["n"," tp"," Queue",  " g", " MOS", " stdev", " app", " SU"]] #, " g"
        df = df.replace('VIP', 'VoIP', regex=True)
        df = df.replace('VID', 'VoD', regex=True)
        df = df.rename(columns={'n': 'Number of \n clients', ' tp': 'Link \n Capacity', " g": "Granularity" ,' app': 'Application type',  ' MOS': 'MOS Mean', ' stdev': 'MOS SD', " SU": "Sys. Util."}) #' g': 'Granularity',
        if app != "Overall":
            df=df.loc[df['Application type'] == " " + app]
        print(df)
        print(df.corr)
        axs[applications.index(app)].matshow(df.corr(method=type).iloc[4:,:7], vmin=-1, vmax=1,aspect='auto') #select rows  
        
        axs[0].set_xticks(range(df.iloc[:,:].select_dtypes(['number']).shape[1]))
        axs[applications.index(app)].set_yticks(range(df.corr(method=type).iloc[:,-3:].select_dtypes(['number']).shape[1])) #select last three columns
        axs[applications.index(app)].set_ylabel(app.replace("host",""))

        axs[0].set(xticklabels=df.iloc[:,:].select_dtypes(['number']).columns)
        axs[applications.index(app)].tick_params(axis='x',labelsize=26,rotation=22.5)  #,rotation=22.5
        axs[applications.index(app)].tick_params(axis='y',labelsize=26) 
        axs[applications.index(app)].set_yticks(range(df.corr(method=type).iloc[:,-3:].select_dtypes(['number']).shape[1]))
        axs[applications.index(app)].set_xticks([])
        plt.tight_layout()
        if app != "Overall":
            axs[applications.index(app)].set_ylabel(app.replace("host",""),rotation=-90,labelpad=25, fontsize=26)
        else:
            axs[applications.index(app)].set_ylabel(app,rotation=-90,labelpad=25, fontsize=26)

        axs[applications.index(app)].yaxis.set_label_position("right")
        axs[applications.index(app)].set(yticklabels=df.corr(method=type).iloc[:,-3:].select_dtypes(['number']).columns)
        for (x, y), value in np.ndenumerate(df.corr(method=type).iloc[:,-3:]):
            if value > -0.4:
                axs[applications.index(app)].text(x, y, f"{value:.3f}", va="center", ha="center", fontsize=26)
            else:
                axs[applications.index(app)].text(x, y, f"{value:.3f}", va="center", ha="center", color="white",fontsize=26)

    cmap = plt.get_cmap('viridis')
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  

    cbar = fig.colorbar(sm, ax=axs.ravel().tolist(), shrink=0.95)
    cbar.ax.tick_params(labelsize=24)
  
    fig.savefig("../exports/extracted/mos2/" + "correlationAggregatedV3" + type + ".png", bbox_inches='tight') 

if __name__ == "__main__":
    numberOfClients = [1]
    numberOfClients.extend([x for x in range (10,110,10)])
    granularity = ["F","S"] 
    throughputs = [x for x in range(50,160,10)]
    app = ["VID","LVD","FDO","VIP"] 
    queue =["T","B","10B"] #Possible values and their meanings are: B = BDP, 5B= 5BDP, T = TinyBuffers, R = Rcwnd"

    testNames = []
    for n in numberOfClients:
        scenarios = []
        for q in queue:
            for g in granularity:
                for t in throughputs:
                    for a in app:
                        testNames.append("n" + str(n) + "_q" + q + "_tp" + str(t) +  "_g" + g + "_a" + a)

    #The three functiond below were used to create csv files from OMNeT++ scavetool exports
    #createCSV(testNames)
    #createCSVWithActualQueueSize(testNames)
    #createCSVwithSU(testNames)

    #mergeCSVs()
    

    ########
    #The following function block generate figures used in the paper. 
    ########
    #plotEcdfQueueSizes(testNames) # Figure 4
    #plotCorrelationMatrixAggregatedV2() # Figure 5 and 6, change type to obtain plots for pearson and spearman
    plotFacetsBarPlots(testNames," SU") #use " SU" as a keyword to get a plot for system utilization and " MOS" to get a plot for MOS, Figures 7 and 8 

    #plotECDF_MOS_Variation() #Figure 9 
    #plotFacetsBarPlotsQuantizationFDO(testNames," SU") #Figure 10
    #plotCDFnumCli_MOSbasic() #Figure 11
    #plotTpMOS35() #Figure 12 
    #plotCDF_gVsMOS()#Figure 14 
    #plotFacetsBarPlotsSUvsNumCli(testNames) #Figure 13
    


    ########
    #The following function block generate supplemetary figures which were not included in the final version of the paper. 
    ########
    #mainEffectsPlot(testNames,numberOfClients,queue,throughputs, granularity)
    #plotFacetsQueue()
    #extractTPperClient(testNames)
    #plotCDF_TpVsMOS()
    #plotCDF_MOS_granularityThickness()
    #plotCDF_MOSbasic()
    
   
  
   
   