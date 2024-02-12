import pandas as pd
import csv
import statistics
from termcolor import colored
import sys
import os
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
maxSimTime = 400
DEBUG = 0

downlink = ['Downlink', 'rxPkOk:vector(packetBytes)']
uplink = ['Uplink', 'txPk:vector(packetBytes)']




def makeFullScenarioName(testName,nodeSplit):
    scenName = str(testName)
    numCLI=sum(nodeSplit)
    #return scenName

    return str(testName) + '_' + str(numCLI) + '_VID' + str(nodeSplit[1]) + '_LVD' + str(nodeSplit[0]) +  '_FDO' + str(nodeSplit[4]) + '_SSH' + str(nodeSplit[2]) + '_VIP' + str(nodeSplit[3])  + '_HVIP' + str(nodeSplit[5])

def makeNodeIdentifier(tp, delay):
    return 'tp' + str(tp) + '_del' + str(delay)

# Function that imports node information into a dataframe
#   - testName - name of the test
#   - numCLI - total number of clients in the test
#   - nodeSplit - number of nodes running certain applications in the test
#       [numVID, numFDO, numSSH, numVIP]
#   - nodeType - type of the node to import (String), curr. used
#       hostVID, hostFDO, hostSSH, hostVIP, links, serverSSH
#   - nodeNum - number of the node to import, omitted if -1
def importDF(testName, tp, delay,nodeSplit,host):
    # File that will be read
    fullScenarioExportName = makeFullScenarioName(testName,nodeSplit)
    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + str(testName)  + '_' + makeNodeIdentifier(tp, delay) + '_' + host + '_vec.csv'
    print("Importing: " + fileToRead)
    # Read the CSV
    return pd.read_csv(fileToRead,nrows=10000)

def filterDFType(df, filterType):
    return df.filter(like=filterType)

def getFilteredDFtypeAndTS(df, filterType):
    filteredDF = filterDFType(df, filterType)
    if len(filteredDF.columns):
        colNoTS = df.columns.get_loc(df.filter(filteredDF).columns[0])
        newDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
        newDF.rename(columns={str(newDF.columns[0]) : "TS", str(newDF.columns[1]) : filterType + " Val"})
        return newDF.rename(columns={str(newDF.columns[0]) : "TS", str(newDF.columns[1]) : filterType + " Val"})
    else:
        return pd.DataFrame(columns=['ts', 'mos Val'])

def mapApplicationToInteger(host):
   
    if host == "hostVIP":
        return 3
    elif host == "hostLVD":
        return 0
    elif host == "hostVID":
        return 1
    elif host == "hostSSH":
        return 2
    elif host == "hostFDO":
        print("In if: " + host)
        return 4
    elif host == "hostHVIP"  : 
        return 5

def mapIntegerToApplication(host):
    if host == 3:
        return "hostVIP"
    elif host == 0:
        return "hostLVD"
    elif host == 1:
        return "hostVID"
    elif host == 2:
        return "hostSSH"
    elif host == 4:
        return "hostFDO"
    elif host == 5: 
        return "hostHVIP"
#extractMosVal return average for all clients in the run
def extractMosVal(testName, tp, delay, nodeSplit, host):
    mosListAllClientsAvg = []
    for i in range (0,nodeSplit[mapApplicationToInteger(host)]): #[mapApplicationToInteger(host)]nodeSplit.index(host)
        hostNumber=host+str(i)
        df = importDF(testName, tp, delay,nodeSplit,hostNumber) #read a file for each client
        print(df)
        mosDF = getFilteredDFtypeAndTS(df, 'mos')
        mosList = mosDF['mos Val'].tolist() #all MOS values for one client
        if len(mosList) > 0:
            mosListAllClientsAvg.append(statistics.mean(mosList)) #add 1 avg value for each client
        else:
            mosListAllClientsAvg.append(1.0)   
    print(mosListAllClientsAvg)
    return statistics.mean(mosListAllClientsAvg) #returns mean mos for all the clients, there should be one per run


def extractAllMosVal(testName, tp, delay, nodeSplit, host):
    mosListAllClientsAvg = []
    for i in range (0,nodeSplit[mapApplicationToInteger(host)]): #[mapApplicationToInteger(host)]nodeSplit.index(host)
        hostNumber=host+str(i)
        df = importDF(testName, tp, delay,nodeSplit,hostNumber) #read a file for each client
        print(df)
        mosDF = getFilteredDFtypeAndTS(df, 'mos')
        mosList = mosDF['mos Val'].tolist() #all MOS values for one client
        if len(mosList) > 0:
            mosListAllClientsAvg.append(statistics.mean(mosList)) #add 1 avg value for each client
        else:
            mosListAllClientsAvg.append(1.0)   
    print(mosListAllClientsAvg)
    return mosListAllClientsAvg #returns mean mos for all the clients, there should be one per run

def prepare4Dcsv(testNames,nodeSplit):
    data4D = pd.DataFrame(columns=["numCli","del","tp","mos"], index=range(20000))
    for testName in testNames:
        
        multiplier = testName.split("scale")[1]
        fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
        fileToRead = '../exports/heatMap/' + fullScenarioExportName + '.csv'
        

        file = open(fileToRead, 'r')
        lines = file.readlines()

        if int(multiplier)==1: 
            print(lines[0].replace("\n", ""))
            print(np.array(lines[1].replace("\n", "")))
            throughputs = []
            delays = []
            #TODO: THE SAME ONE FOR DELAYS IS NEEDED!   
            for element in lines[1].split(","):
                throughputs.append(int(element))
            delays.append(int(20))
            delays.append(int(25))
            delays.append(int(30))
            throughputs=np.array(throughputs)
            delays = np.array(delays)
        
        
        
            carteseanProduct = np.transpose([np.tile(delays, len(throughputs)), np.repeat(throughputs, len(delays))]) #the order is 20,30 ,20,30
            print(carteseanProduct)
            for num in range(0,len(numberOfClients)):
                for i in range(0,len(carteseanProduct)):
                    
                    data4D["numCli"][i+(num*len(carteseanProduct))] = numberOfClients[num]
                    data4D["del"][i+(num*len(carteseanProduct))] = carteseanProduct[i][0]
                    data4D["tp"][i+(num*len(carteseanProduct))] = carteseanProduct[i][1]
                    #print(data4D)
                #print(data4D.iloc[24])
                #print(data4D.iloc[48])
          
        lines[2]=lines[2].replace("\"[", "").replace("]\"","").replace("\n","")
        print(lines[2])
        for i in range(0,len(lines[2].split(","))):
             data4D["mos"][i*len(delays)+testNames.index(testName)*len(carteseanProduct)] = lines[2].split(",")[i]
             data4D["mos"][i*len(delays)+1+testNames.index(testName)*len(carteseanProduct)] = lines[2].split(",")[i] #this is improvisation for 30ms delay
             data4D["mos"][i*len(delays)+2+testNames.index(testName)*len(carteseanProduct)] = lines[2].split(",")[i]
        print(data4D)

    data4D.to_csv("../exports/heatMap/" + testName + '.csv', index=False)
        

        # for i in range(0, len(df[3])):
        #     line.append[multiplier]
        #     line.append[", "]
        # for d in df[0]:
        #     line.append[d]
        #     line.append[", "]
        #     for t in df[1]:
        #          line.append[t]
        #          line.append[", "]
        #          for mos in df[3]:
        #              line.append[mos]
        #              line.append[]










def plot4dHeatmap(fileName, tps, delays, numberOfClients): #number of clients is a list with all scaling factors
    #'Create a list for every parameter'
    x = []
    y = []
    z = []
    v = []

    fileToRead = '../exports/heatMap/' + fileName + '.csv'
    print("Importing: " + fileToRead)
    # Read the CSV
    #df= pd.read_csv(fileToRead)
    df = pd.read_csv(fileToRead)
    df.dropna()
    print(df)
    for i in range (0,len(df)):
        x.append(df.iloc[i][0])
        y.append(df.iloc[i][1])
        z.append(df.iloc[i][2])
        v.append(df.iloc[i][3])
    print(x)
    print(v)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  
    img = ax.scatter(x, y, z, c=v, cmap=plt.viridis())
    ax.set_xlabel('Number of clients')
    ax.set_ylabel('Delay')
    #ax.set_zlabel("Throughput")
    ax.zaxis.set_rotate_label(False)  # disable automatic rotation
    ax.set_zlabel('Throughput', rotation=90)    
    fig.colorbar(img,location = 'left')
    # #'Create axis data'
    # xi = np.linspace(min(x), max(x), 1000)
    # zi = np.linspace(min(z), max(z), 1000)
    # vi = griddata((x, z), v, (xi[None,:], zi[:,None]), method='cubic')

    # #'Create the contour plot'
    # CS = plt.contourf(xi, zi, vi, 20, cmap=plt.cm.rainbow)
    # plt.title("Heatmap xz-plane", y=1.05, fontweight="bold")
    # plt.xlabel("length x in cm")
    # plt.xticks(np.arange(0, 4, step=1))
    # plt.ylabel("height z in cm")
    # plt.yticks(np.arange(110, 251, step=20))
    # cbar = plt.colorbar()
    # cbar.set_label("velocity v in m/s", labelpad=10)
    plt.title("VoD 4D Heatmap")
    plt.savefig('../exports/plots/' + fileName + '.png', dpi=400)  
    #plt.show()




def plotGainTotalMeanMos(testNames, tps, delay, nodeSplit, host):

    minTPforQoE35 =  []
    multipliers = []
    baselineMosVals = []

    for testName in testNames:
        multiplier = testName.split("scale")[1]
        print("This is multiplier" + multiplier)
        multipliers.append(multiplier)
        fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
        fileToRead = '../exports/heatMap/' + fullScenarioExportName + '.csv'
        print("Importing: " + fileToRead)
        # Read the CSV
        #df= pd.read_csv(fileToRead)
        df = pd.read_csv(fileToRead,header=None, skiprows=1)
        columns = pd.read_csv(fileToRead,nrows=0).columns.tolist()
        num_missing_cols = len(df.columns) - len(columns)
        new_cols = ['col' + str(i+1) for i in range(num_missing_cols)]
        df.columns = columns + new_cols
        #print(float(df.iloc[1].tolist()[1]))
        #print(df.iloc[0])
        mosVals = df.iloc[1].tolist()
        print(len(mosVals))
        print(mosVals)
        mosValsFloat = []
        for i in range(0, len(mosVals),1 ):
            mosValsFloat.append(float(mosVals[i][1:mosVals[i].index("]")]))
        
        if multiplier == str(1): #this is a baseline, reference from which we will take a difference to 
            print(multiplier)
            print("This is multiolier.")
            baselineMosVals = mosValsFloat
            print("this is baseline")
            print(baselineMosVals)

        for val in mosValsFloat:            
            if val>=3.5:
                #print(val)
                minTPforQoE35.append(mosValsFloat.index(val)*(tps[1]-tps[0])+tps[0])
                break
            else:
                if mosValsFloat.index(val) == len(mosValsFloat) - 1:   
                    print("At the last one in MOS values.") 
                    minTPforQoE35.append(10000) 
        difference = [a - b for a, b in zip(mosValsFloat,baselineMosVals)]
        print(difference)
        plt.plot(tps,difference,label=testName)
    plt.xlabel("Throughput [kbps]")
    plt.ylabel("Gain in MOS")
    plt.legend()
    plt.savefig("../exports/plots/MosGainComparisson_" + host + ".png") #+ "_" + testNames[1] 
    # plt.close()
    # print("This is min tp for 3.5 MOS")
    # print(minTPforQoE35)
    # print("This is multipliers.")
    # print(multipliers)
    # plt.plot(multipliers,minTPforQoE35,label=testName)
    # plt.xlabel("Number of clients")
    # plt.ylabel("Bandwidth needed for QoE 3.5")
    # plt.savefig("../exports/plots/bandwidthQoE35_" + host + ".png") #+ "_" + testNames[1] 
    # plt.close()



def extractMeanMosAllThroughputs(testNames, tps, delay, nodeSplit, host):
    labels = ["Queue size: Dynamic", "Queue size: 6Mb", "Queue size: 12Mb"]
    minTPforQoE35 =  []
    multipliers = []
    for testName in testNames:
        multiplier = testName.split("scale")[1].split("tcp")[0]
        multipliers.append(multiplier)
        fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
        fileToRead = '../exports/heatMap/' + fullScenarioExportName + '.csv'
        print("Importing: " + fileToRead)
        df = pd.read_csv(fileToRead,header=None, skiprows=1)
        columns = pd.read_csv(fileToRead,nrows=0).columns.tolist()
        num_missing_cols = len(df.columns) - len(columns)
        new_cols = ['col' + str(i+1) for i in range(num_missing_cols)]
        df.columns = columns + new_cols
        mosVals = df.iloc[1].tolist()
        print(len(mosVals))
        print(mosVals)
        mosValsFloat = []
        for i in range(0, len(mosVals),1 ):
            mosValsFloat.append(float(mosVals[i][1:mosVals[i].index("]")]))
        for val in mosValsFloat:
            
            if val>=3.5:
                print(tps)
                minTPforQoE35.append(mosValsFloat.index(val)*(tps[1]-tps[0])+tps[0])
                break
            else:
                if mosValsFloat.index(val) == len(mosValsFloat) - 1:   
                    print("At the last one in MOS values.") 
                    minTPforQoE35.append(10000) 


        #markers_x = [tps[23],tps[28]]
        #markers_y=[mosValsFloat[23],mosValsFloat[28]]
        #plt.plot(markers_x,markers_y,marker='o',color="black", linestyle="None")
        plt.plot(tps,mosValsFloat,label= str(multiplier),marker='o', markersize=1)  #labels[testNames.index(testName)]
    plt.axhline(y=3.5, color='gray', linestyle='--')    
    #plt.axvline(x=220, color='gray', linestyle='dashed')
    #plt.axvline(x=450, color='gray', linestyle='dashed')  
    #plt.axvspan(220, 450, alpha=0.8, color='gainsboro')
    #plt.axvline(x=375, color='sienna', linestyle='dotted')
    #plt.axvline(x=750, color='sienna', linestyle='dotted')
    #plt.axvspan(375, 750, alpha=0.6, color='linen') 


    plt.xlabel("Throughput per client [kbps]")
    plt.ylabel("MOS")
    plt.ylim(1.0,5.0)
    plt.legend(title = "Number of hosts: ",loc='lower right')
    plt.savefig("../exports/plots/bufferStudies/MOS/"+ testName +  ".png") #+ "_" + testNames[1] 
    plt.close()
    plt.plot(multipliers,minTPforQoE35,label=testName)
    plt.xlabel("Number of clients")
    plt.ylabel("Throughput per client needed for QoE 3.5 [kbps]")
    plt.savefig("../exports/plots/bufferStudies/MOS/ThroughputNeededForQoE35" + testName + ".png") #+ "_" + testNames[1] 
    plt.close()




def videoQualityBox(testNames, numCLI, nodeTypes, nodeSplit, nodeType, tps, delays):
    print(tps)
    allData = pd.DataFrame()
    for testName in testNames:
        
        multiplier = testName.split("scale")[1].split("tcp")[0]
        for tp in tps:     
            AllClients = []
            tp=tp*int(multiplier)
            for delay in delays:
                print(AllClients) 
                for node in range(int(multiplier)):
                    print("Going through the nodes")
                    print(tp)
                    #if node==33 or node == 3: # or  node ==7: # or node == 37 or node==45 or node ==2 or node ==24 or node ==7 or node==78 or node==94
                    df = importDF(testName, tp, delay,  [x * int(multiplier) for x in nodeSplit], "hostVID" + str(node))    
                    colNoTS = df.columns.get_loc(df.filter(like="DASHVideoResolution").columns[0])
                    #colNoTS = df.columns.get_loc(df.filter(like="DASHBufferLength").columns[0])
                    tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                    tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'video resolution'}, inplace = True)
                    print("There is in total" + str(len(tempDF)) + "entries for video resolution. ")
                    #AllClients.extend(tempDF['video resolution'])
                    qualityChangeCount = 0
                    i=1
                    allTimes = []
                    timeBegin = tempDF["ts"][0]
                    for resolution in tempDF["video resolution"].tail(-1):
                        if resolution != tempDF["video resolution"][i-1]:
                            qualityChangeCount +=1
                            timeDuration = tempDF["ts"][i] - timeBegin
                            timeBegin=tempDF["ts"][i]
                            allTimes.append(timeDuration)
                        i=i+1
                    print("Quality change count: " + str(qualityChangeCount))
                    print(allTimes)

                    

                    AllClients.extend(allTimes)
                    #AllClients.append(qualityChangeCount)

                    #AllClients.append(statistics.mean(tempDF['video resolution']))

                #meanVidQual.append(statistics.mean(meanOfAllClients))
        #plot max video resolution
        # plt.plot(tps, meanVidQual, label=testName)
        # plt.legend()
        # plt.xlabel("Throughput")
        # plt.ylabel("VideoResolution")
        # plt.savefig("../../../exports/heatMap/MaxVideoResolution_" + testName + ".png")
                    print(AllClients)
                allData=pd.concat([allData, pd.DataFrame(AllClients, columns=[str(multiplier)])], axis=1)
                print(allData)
    bp=allData.boxplot(showmeans = True, meanline = True)
    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')
    plt. axhline(y=30, color='r', linestyle='-', linewidth=2, label='Duration threshold') 
    plt.legend()
    plt.xlabel("Number of clients")
    plt.ylabel("Buffer length")
    plt.ylabel("Resolution")
    plt.ylabel("Duration without quality changes")

    #plt.savefig("../exports/plots/BoxVideoResolutionAMean_" + testName + ".png")
    plt.savefig("../exports/plots/BoxResolutionSwitchDuration_" + testName + ".png")
    #plt.savefig("../exports/plots/BoxVideoBufferMean_" + testName + ".png")




def cwnd(testNames, numCLI, nodeTypes, nodeSplit, nodeType, tps, delays):
    print(tps)
    allData = pd.DataFrame()
    for testName in testNames:
        multiplier = testName.split("scale")[1]
        for tp in tps:
            if tp == 100 or tp== 1000 or tp ==1000:   
                AllClients = []
                tp=tp*int(multiplier)
                for delay in delays:
                    print(AllClients) 
                    for node in range(int(multiplier)):
                        print("Going through the nodes")
                        if node==0:
                            df = importDF(testName, tp, delay,  [x * int(multiplier) for x in nodeSplit], "serverVID") # serverFDO   serverVID_run0
                            print("There is in total columns with cwnd")
                            colNoTS = df.columns.get_loc(df.filter(like="cwnd:vector").columns[node]) #get_loc will return integer location of the index of the column 
                            print(df.filter(like="cwnd:vector").columns[node])
                            #colNoTS = df.columns.get_loc(df.filter(like="DASHBufferLength").columns[0])
                            tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                            tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'cwnd'}, inplace = True)
                            print("There is in total" + str(len(tempDF)) + "entries for cwnd. ")
                            plt.plot(tempDF['ts'],tempDF['cwnd'], label = "node" + str(node) + "tp" + str(tp))
                        #AllClients.extend(tempDF['cwnd'])
                        #print(AllClients)
                #allData=pd.concat([allData, pd.DataFrame(AllClients, columns=[str(multiplier)])], axis=1)
                #print(allData)
        #bp=allData.boxplot(showmeans = True, meanline = True)
        #plt.plot([], [], '-', linewidth=1, color='green', label='median')
        #plt.plot([], [], '--', linewidth=1, color='green', label='mean')
        #plt. axhline(y=30, color='r', linestyle='-', linewidth=2, label='Duration threshold') 
        plt.legend()
        plt.ylabel("cwnd")
        #plt.xlim(0,50)
        #plt.ylim(0)
        
    
        #plt.savefig("../exports/plots/BoxVideoResolutionAMean_" + testName + ".png")
        plt.savefig("../exports/plots/bufferStudies/cwndTimeSeries_" + testName + ".png")
        #plt.savefig("../exports/plots/BoxVideoBufferMean_" + testName + ".png")

def rcvWnd(testNames, numCLI, nodeTypes, nodeSplit, nodeType, tps, delays):
    print(tps)
    allData = pd.DataFrame()
    for testName in testNames:
        multiplier = testName.split("scale")[1]
        for tp in tps:
            if tp == 100 or tp== 1000 or tp ==1000:   
                AllClients = []
                tp=tp*int(multiplier)
                for delay in delays:
                    print(AllClients) 
                    for node in range(int(multiplier)):
                        print("Going through the nodes")
                        if node==0:
                            df = importDF(testName, tp, delay,  [x * int(multiplier) for x in nodeSplit], "hostVID0") # serverFDO   serverVID_run0
                            print("There is in total columns with rcvWnd")
                            colNoTS = df.columns.get_loc(df.filter(like="rcvWnd:vector").columns[node]) #get_loc will return integer location of the index of the column 
                            print(df.filter(like="rcvWnd:vector").columns[node])
                            #colNoTS = df.columns.get_loc(df.filter(like="DASHBufferLength").columns[0])
                            tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                            tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'rcvWnd'}, inplace = True)
                            print("There is in total" + str(len(tempDF)) + "entries for rcvWnd. ")
                            plt.plot(tempDF['ts'],tempDF['rcvWnd'], label = "node" + str(node) + "tp" + str(tp))
                        #AllClients.extend(tempDF['rcvWnd'])
                        #print(AllClients)
                #allData=pd.concat([allData, pd.DataFrame(AllClients, columns=[str(multiplier)])], axis=1)
                #print(allData)
        #bp=allData.boxplot(showmeans = True, meanline = True)
        #plt.plot([], [], '-', linewidth=1, color='green', label='median')
        #plt.plot([], [], '--', linewidth=1, color='green', label='mean')
        #plt. axhline(y=30, color='r', linestyle='-', linewidth=2, label='Duration threshold') 
        plt.legend()
        plt.ylabel("rcvWnd")
        #plt.ylim(0,60000)
        #plt.ylim(0,100000)
        
    
        #plt.savefig("../exports/plots/BoxVideoResolutionAMean_" + testName + ".png")
        plt.savefig("../exports/plots/bufferStudies/rcvWndTimeSeries_" + testName + ".png")
        #plt.savefig("../exports/plots/BoxVideoBufferMean_" + testName + ".png")





def plotBoxMOSvsNumCli(testNames, tps, delay, nodeSplit, host):
    print("TPs are:")
    print(tps)
    minTPforQoE35 =  []
    multipliers = []
    counter=0
    allData = pd.DataFrame()
    for testName in testNames:
        multiplier = testName.split("scale")[1].split("tcp")[0]
        multipliers.append(multiplier)
        fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
        # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostVID0_vec.csv'
        #fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostFDO0_vec.csv'
        # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_vec.csv'
        #fileToRead = '../' + str(testName) + "/heatMapTest_VoIP_scalability10_10_VID0_FDO0_SSH0_VIP10" + "/heatMapTest_VoIP_scalability10"  + '_' + makeNodeIdentifier(tp, delay) + '_hostVIP0_vec.csv'
        fileToRead = '../exports/heatMap/All' + fullScenarioExportName + '.csv' #
        print("Importing: " + fileToRead)
        df = pd.read_csv(fileToRead,header=None, skiprows=1)
        columns = pd.read_csv(fileToRead,nrows=0).columns.tolist()
        num_missing_cols = len(df.columns) - len(columns)
        new_cols = ['col' + str(i+1) for i in range(num_missing_cols)]
        df.columns = columns + new_cols
        #print(float(df.iloc[1].tolist()[1]))
        #print(df.iloc[0])
        mosVals = df.iloc[1].tolist()
        print(len(mosVals))
        print(mosVals)
        mosValsFloat = []
        for i in range(0, len(mosVals),1 ):
            print(mosVals[i][1:mosVals[i].index("]")].split("[")[1])
            if "," in mosVals[i][1:mosVals[i].index("]")].split("[")[1]:
                for j in mosVals[i][1:mosVals[i].index("]")].split("[")[1].split(", "):
                    mosValsFloat.append(float(j))
            else:    
                mosValsFloat.append(float(mosVals[i][1:mosVals[i].index("]")].split("[")[1]))
        print(len(mosValsFloat))
        # for val in mosValsFloat:
        #     if val>=3.5:
        #         #print(val)
        #         minTPforQoE35.append(mosValsFloat.index(val)*(tps[1]-tps[0])+tps[0])
        #         break
        #     else:
        #         if mosValsFloat.index(val) == len(mosValsFloat) - 1:   
        #             print("At the last one in MOS values.") 
        #             minTPforQoE35.append(10000) 

        allData=pd.concat([allData, pd.DataFrame(mosValsFloat, columns=[str(multiplier)])], axis=1)
        #counter+=1
    c="blue"
    bp=allData.boxplot(showmeans = True, meanline = True)
    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')
    #plt.xticks([10,15,20,30,40,45,60, or tp= 1000,200], [10,15,20,30,40,45,60, or tp= 1000,200])
    plt.legend()
    plt.ylim(2.5,5.0)
    plt.ylabel("MOS")
    plt.xlabel("Number of clients")
    plt.savefig("../exports/plots/bufferStudies/MOS/" + testName + "BoxMos_.png") #+ "_" + testNames[1] _run0 
    plt.close()
    #plt.plot(tps,mosValsFloat,label= "Number of hosts: " + str(multiplier))  #labels[testNames.index(testName)]
    #plt.axhline(y=3.5, color='gray', linestyle='--')    
    #plt.axvline(x=220, color='gray', linestyle='dashed')
    #plt.axvline(x=450, color='gray', linestyle='dashed')  
    #plt.axvspan(220, 450, alpha=0.8, color='gainsboro')
    #plt.axvline(x=375, color='sienna', linestyle='dotted')
    #plt.axvline(x=750, color='sienna', linestyle='dotted')
    #plt.axvspan(375, 750, alpha=0.6, color='linen') 


    # plt.xlabel("Throughput per client [kbps]")
    # plt.ylabel("MOS")
    # plt.ylim(1.0,5.0)
    # plt.legend(loc='upper left')
    # plt.savefig("../exports/plots/comparisson_" + host + ".png") #+ "_" + testNames[1] 
    # plt.close()
    # print("This is min tp for 3.5 MOS")
    # print(minTPforQoE35)
    # print("This is multipliers.")
    # print(multipliers)
    # plt.plot(multipliers,minTPforQoE35,label=testName)
    # 
    # plt.ylabel("Bandwidth needed for QoE 3.5")

def plotBoxQueueFullness(testNames, tps, delay, nodeSplit, host):
    print("TPs are:")
    print(tps)
    minTPforQoE35 =  []
    multipliers = []
    counter=0
    allData = pd.DataFrame()
    for tp in tps: 
        if tp ==100  or tp== 1000 or tp==1000: 
            print("Tp is " + str(tp))
            for testName in testNames:
                print(testName.split("scale")[0].split(host.split("host")[1])[0])
                queueSize = int(testName.split("scale")[0].split(host.split("host")[1])[0].split("testqueue")[1].split("Mb")[0])
                print(queueSize)
                print(queueSize)
                multiplier = testName.split("scale")[1]
                multipliers.append(multiplier)
                #tp=tps[0]*int(multiplier)
                fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
                # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostVID0_vec.csv'
                #fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostFDO0_vec.csv'
                # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_vec.csv'
                #fileToRead = '../' + str(testName) + "/heatMapTest_VoIP_scalability10_10_VID0_FDO0_SSH0_VIP10" + "/heatMapTest_VoIP_scalability10"  + '_' + makeNodeIdentifier(tp, delay) + '_hostVIP0_vec.csv'
                #fileToRead = '../exports/heatMap/All' + fullScenarioExportName + '.csv'
                fileToRead = '../' + str(testName) + '/' + str(fullScenarioExportName) + '/' + str(testName) + '_tp' + str(tp*int(multiplier)) + '_del20_router1' + '_vec.csv'
                print("Importing: " + fileToRead)
                df = pd.read_csv(fileToRead)
                print(df.filter(like='State'))
                if not df.filter(like='queueBitLength').dropna().empty:
                    print(df.iloc[:, [13]])
                    #print(df.columns.get_loc(df.filter(like='queueBitLength')))
                    #print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
                    df = df.iloc[:, [13]]
                    df.columns = df.iloc[0,:].values
                    df = df.tail(-1)    
                    df = (df/(queueSize*10000))
                    allData=pd.concat([allData, pd.DataFrame(df.values.tolist(), columns=[str(queueSize) + "Q" + str(multiplier) + "node" + str(tp) + "kbps"])], axis=1)
                    #allData=pd.concat([allData, pd.DataFrame(AllClients, columns=[str(multiplier)])], axis=1)
                    print(allData)
                else:
                    allData[str(multiplier)]=[0]
                    print(allData)

    bp=allData.boxplot(showmeans = True, meanline = True,figsize=(15,6))

    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')

    plt.legend()

   
    plt.ylabel("Queue fullness (%) ")
    plt.xlabel("Number of clients")
    plt.savefig("../exports/plots/bufferStudies/BoxFullnessQueue_run0.png") #+ "_" + testNames[1] 
    plt.close()

def plotMosVsQueueFullness(testNamesLists, tps, delay, nodeSplit, host):
    #colors = ["C0", "C1", "C2"]

    for testNames in testNamesLists:
        print(testNames)
        for tp in tps:
            if tp == 100 or tp== 563 or tp == 1575:
                if tp ==100  or tp== 563 or tp==1575:
                    marker = "v"
                elif tp == 1000:
                    marker =  "^"  
                elif tp==500:
                    marker="s"
                         
                allData = pd.DataFrame()
                avgQueueFullness = []
                multipliers = []
                counter=0
                queueSize = int(testNames[0].split("scale")[0].split(host.split("host")[1])[0].split("queue")[1].split("Mb")[0])
                print(queueSize)
                print(testNames)
                for testName in testNames:
                    print(testName)
                    multiplier = testName.split("scale")[1]
        
                    print(tp)
                    if multiplier not in multipliers:
                        multipliers.append(multiplier)
                    fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostVID0_vec.csv'
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostFDO0_vec.csv'
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_vec.csv'
                    fileToRead = '../' + str(testName) + "/heatMapTest_VoIP_scalability10_10_VID0_FDO0_SSH0_VIP10" + "/heatMapTest_VoIP_scalability10"  + '_' + makeNodeIdentifier(tp, delay) + '_hostVIP0_vec.csv'
                    fileToRead = '../exports/heatMap/All' + fullScenarioExportName + '.csv'
                    fileToRead = '../' + str(testName) + '/' + str(fullScenarioExportName) + '/' + str(testName) + '_tp' + str(tp*int(multiplier)) + '_del20_router1' + '_vec.csv'
                    print("Importing: " + fileToRead)
                    df = pd.read_csv(fileToRead)
                    if not df.filter(like='queueBitLength').dropna().empty:
                        #print(df.iloc[:, [13]])
                        #print(df.columns.get_loc(df.filter(like='queueBitLength')))
                        #print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
                        df = df.iloc[:, [13]]
                        df.columns = df.iloc[0,:].values
                        df = df.tail(-1)
                        #print(df)
                        df = (df/(int(testName.split("scale")[0].split(host.split("host")[1])[0].split("queue")[1].split("Mb")[0])*10000))
                        allData=pd.concat([allData, pd.DataFrame(df.values.tolist(), columns=[str(multiplier)])], axis=1)
                        #allData=pd.concat([allData, pd.DataFrame(AllClients, columns=[str(multiplier)])], axis=1)
                        print(allData[multiplier])
                        avgQueueFullness.append(statistics.mean(allData[multiplier].apply(float)))

                    else:
                        allData[str(multiplier)]=[0]
                    print("End of the script")        
                    print(multipliers)
                    print(avgQueueFullness)
                plt.plot([queueSize*1000/int(x) for x in multipliers], avgQueueFullness, label = "queue =" + str(queueSize) + "Mb, tp= " + str(tp), marker=marker, linestyle="dashed", linewidth=0.5)
    plt.legend()
    plt.ylim(0,101)
    #plt.xlim(0,2000)
    plt.ylabel("Queue fullness (%) ")
    plt.xlabel("kb of queue available per client ")
    plt.savefig("../exports/plots/bufferStudies/BoxFullnessQueue_"  + "_" + testNames[0] + ".png") 
    plt.close()

def plotQueueBitLength(testNamesLists, tps, delay, nodeSplit, host):
    #colors = ["C0", "C1", "C2"]

    for testNames in testNamesLists:
        for tp in tps:
            if tp == 100 or tp== 1000:
                allData = pd.DataFrame()
                avgQueueFullness = []
                multipliers = []
                counter=0
                #queueSize = int(testNames.split("scale")[0].split(host.split("host")[1])[0].split("queue")[1].split("Mb")[0])
                #print(queueSize)
                print(testNames)
                for testName in testNames:
                    queueSize = int(testName.split("scale")[0].split(host.split("host")[1])[0].split("queue")[1].split("Mb")[0])
                    print(testName)
                    multiplier = testName.split("scale")[1]
                    print(tp)
                    if multiplier not in multipliers:
                        multipliers.append(multiplier)
                    fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostVID0_vec.csv'
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostFDO0_vec.csv'
                    fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_vec.csv'
                    fileToRead = '../' + str(testName) + "/heatMapTest_VoIP_scalability10_10_VID0_FDO0_SSH0_VIP10" + "/heatMapTest_VoIP_scalability10"  + '_' + makeNodeIdentifier(tp, delay) + '_hostVIP0_vec.csv'
                    fileToRead = '../exports/heatMap/All' + fullScenarioExportName + '.csv'
                    fileToRead = '../' + str(testName) + '/' + str(fullScenarioExportName) + '/' + str(testName) + '_tp' + str(tp*int(multiplier)) + '_del20_router1' + '_vec.csv'
                    print("Importing: " + fileToRead)
                    df = pd.read_csv(fileToRead)
                    if not df.filter(like='queueBitLength').dropna().empty:
                        print("the index is")
                        print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
                        #print(df.iloc[:, [13]])
                        #print(df.columns.get_loc(df.filter(like='queueBitLength')))
                        #print(df.columns.get_loc(df.filter(like='queueBitLength').columns[0]))
                        
                        df = df.iloc[:, [12,13]]
                        #df=df[df.columns[1:13]]
                        #df.columns = df.iloc[0,:].values
                        #df = df.tail(-1)
                        print(df.columns)
                        #print(df[1])
                        #df.columns = df.iloc[0,:].values
                        #
                        #print(df)
                        plt.plot(df.iloc[:,0].values, df.iloc[:,1].values, label = "queue =" + str(queueSize) + "Mb, tp= " + str(tp))

                #plt.plot([queueSize*1000/int(x) for x in multipliers], avgQueueFullness, label = "queue =" + str(queueSize) + "Mb, tp= " + str(tp), marker=marker, linestyle="dashed", linewidth=0.5)
    plt.legend()
   #plt.ylim(0,101)
    #plt.xlim(0,2000)
    plt.ylim(0,queueSize*1000000)
    plt.ylabel("Queue length ")
    plt.xlabel("Time [s] ")
    plt.savefig("../exports/plots/bufferStudies/QueueBitLength_"  + "_" + testNames[0] + ".png") 


def plotBoxDroppedQueue(testNames, tps, delay, nodeSplit, host):
    print("TPs are:")
    print(tps)
    minTPforQoE35 =  []
    multipliers = []
    counter=0
    allData = pd.DataFrame()
    for testName in testNames:
        multiplier = testName.split("scale")[1].split("tcp")[0]
        multipliers.append(multiplier)
        tp=tps[0]*int(multiplier)
        fullScenarioExportName = makeFullScenarioName(testName,[int(x)*int(multiplier) for x in nodeSplit])
        # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostVID0_vec.csv'
        #fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_hostFDO0_vec.csv'
        # fileToRead = '../' + str(testName) + '/' + fullScenarioExportName + '/' + fullScenarioExportName + '_' + makeNodeIdentifier(tp, delay) + '_vec.csv'
        #fileToRead = '../' + str(testName) + "/heatMapTest_VoIP_scalability10_10_VID0_FDO0_SSH0_VIP10" + "/heatMapTest_VoIP_scalability10"  + '_' + makeNodeIdentifier(tp, delay) + '_hostVIP0_vec.csv'
        #fileToRead = '../exports/heatMap/All' + fullScenarioExportName + '.csv'
        fileToRead = '../' + str(testName) + '/' + str(fullScenarioExportName) + '/' + str(testName) + '_tp' + str(tp) + '_del20_router1' + '_vec.csv'
        print("Importing: " + fileToRead)
        df = pd.read_csv(fileToRead)
        if not df.filter(like='dropped').dropna().empty:
            print(len(df.filter(like='dropped').dropna()))
            allData[str(multiplier)]=[len(df.filter(like='dropped').dropna())/int(multiplier)]
            print(allData)
        else:
            allData[str(multiplier)]=[0]
            print(allData)

    bp=allData.boxplot(showmeans = True, meanline = True)
    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')

    plt.legend()
  
    plt.ylabel("Dropped packets count")
    plt.xlabel("Number of clients")
    plt.savefig("../exports/plots/BoxDroppedQueue"+ testName + ".png") #+ "_" + testNames[1] 
    plt.close()

 
def countMOS():
    df =  pd.read_csv('countMos1.csv')
    df.columns =['Host', 'TP', 'count']
    
    for i in range(5,50):
        hostName="hostVIP"
        hostName=hostName + str(i) #for each host
        count =[]
        for i in range(0,25):
            print(len(list(df.loc[df["Host"] == hostName, "count"])))
            count.append(list(df.loc[df["Host"] == hostName, "count"])[i]) #get values for first 5 BW
        plt.plot([x for x in range(5,30,1)],count,label=hostName)
    plt.xlabel("Throughput [kbps]")
    plt.ylabel("CountMOS")
    plt.legend()

    plt.savefig("../exports/plots/count.png")


def plotMosCdf(testNames, tps, delay,nodeSplit):
    mosValues = {} #initialize array and save all points in there
    tpsOriginal=tps

    for testName in testNames:
        # if testName == "heatMapTest_VoIP_scalability10s1":
        #     nodeSplit = [0, 0, 0, 0, 1,0]
        #     tps[:] = [int(x / 10) for x in tps]
        #     print(tps)
        # if testName == "heatMapTest_VoIP_scalability1s100":
        #     nodeSplit = [0, 0, 0, 0,  or tp= 1000,0]
        #     tps[:] = [int(x *  or tp= 1000) for x in tps]
        mosValues[testName]=[]
        for i in tps:
            mosValues[testName].append(extractMosVal(testName, i, delay, nodeSplit, "hostVIP"))

        print(tpsOriginal)
        plt.plot( [x for x in range(5,30,1)],mosValues[testName],label=testName.split("_")[2].replace("scalability",""))
        plt.xlabel("Throughput [kbps]")
        plt.ylabel("MOS")
        
        plt.legend()
        plt.close()

    plt.savefig("../exports/plots/comparisson_" + testNames[0] + "_" + testNames[1] + ".png")

def extracte2ed(testName, tp, delay):
    df = importDF(testName, tp, delay)
    mosDF = getFilteredDFtypeAndTS(df, 'endToEndDelay')
    print(mosDF['endToEndDelay Val'])
    return mosDF['endToEndDelay Val']

# extractMosVal('heatMapTest_VoIPnewSettings', 540, 0)
# extracte2ed('singleAppDelayTest_VoIP_1cli', 10000, 50)


def prepareMosValsForHeatmap(testName, tps, delays,nodeSplit):
    xAxis = []
    yAxis = []
    mosMap = []
    for x in delays:
        if x not in xAxis:
            xAxis.append(x)
        for y in tps:
            if y not in yAxis:
                yAxis.append(y)
                mosMap.append([])

            mosMap[yAxis.index(y)].append(extractMosVal(testName, y, x, nodeSplit, mapIntegerToApplication(nodeSplit.index(next(x for x in nodeSplit if x > 0)))))
    if not os.path.exists('../exports/heatMap/'):
        os.makedirs('../exports/heatMap/')
    with open('../exports/heatMap/'+makeFullScenarioName(testName,nodeSplit)+'.csv', mode='w') as writeFile:
        fw = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        fw.writerow(xAxis)
        fw.writerow(yAxis)
        fw.writerow(mosMap)




def prepareAllMosValsForHeatmap(testName, tps, delays,nodeSplit):
    xAxis = []
    yAxis = []
    mosMap = []
    for x in delays:
        if x not in xAxis:
            xAxis.append(x)
        for y in tps:
            if y not in yAxis:
                yAxis.append(y)
                mosMap.append([])

            mosMap[yAxis.index(y)].append(extractAllMosVal(testName, y, x, nodeSplit, mapIntegerToApplication(nodeSplit.index(next(x for x in nodeSplit if x > 0)))))
    if not os.path.exists('../exports/heatMap/'):
        os.makedirs('../exports/heatMap/')
    with open('../exports/heatMap/All'+makeFullScenarioName(testName,nodeSplit)+'.csv', mode='w') as writeFile:
        print("Writing the heatmap with all values.")
        fw = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        fw.writerow(xAxis)
        fw.writerow(yAxis)
        fw.writerow(mosMap)        

def plotMosVsBw(testNames, tps, delay,nodeSplit, host):
    mosValues = {} #initialize array and save all points in there
    minTP = {}
    tpsOriginal=tps
    
    for testName in testNames:
     
        multiplier = testName.split("scale")[1]
        print(multiplier)
        # if testName == "heatMapTest_VoIP_scalability10s1Queue10000":
        #     nodeSplit = [0, 0, 0, 0, 1,0]
        #     tps[:] = [int(x / 10) for x in tps]

        #     print(tps)
        # if  testName=="heatMapTest_VoIP_scalability10s100Queue10000" or testName=="heatMapTest_VoIP_scalability1s100NoOffset200ms": #testName == "heatMapTest_VoIP_scalability1s100" or heatMapTest_VoIP_scalability1s100Queue500
        #     nodeSplit = [0, 0, 0, 0,  or tp= 1000,0]
        #     tps[:] = [int(x * 10) for x in tpsOriginal]
        # if  testName=="heatMapTest_VoIP_scalability10s1000Queue10000": 
        #     nodeSplit = [0, 0, 0, 0, 1000,0]
        #     tps[:] = [int(x * 10) for x in tpsOriginal]
        mosValues[testName]=[]
        for i in tps:
            mosValues[testName].append(extractMeanMosAllThroughputs(testName, i, delay,  nodeSplit, host))

        for val in mosValues[testName]:
            print(val)
            if val>=3.5:
                minTP[testName]= mosValues[testName].index(val)
                break     

        plt.plot([float(x)/float(multiplier) for x in tps],mosValues[testName],label=testName)
        plt.xlabel("Throughput [kbps]")
        plt.ylabel("MOS")
        plt.legend()
    plt.savefig("../exports/plots/comparisson_" + host + ".png") #+ "_" + testNames[1] 
    for i in testNames:
        print(minTP[i])
    # if not os.path.exists('../exports/heatMap/'):
    #     os.makedirs('../exports/heatMap/')
    # with open('../exports/heatMap/'+makeFullScenarioName(testName,nodeSplit)+'.csv', mode='w') as writeFile:
    #     fw = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    #     fw.writerow(xAxis)
    #     fw.writerow(yAxis)
    #     fw.writerow(mosMap)
    # for i in testNames:
    #     mosValues = [] #initialize array and save all points in there
    #     for i in tps:
    #     mosValues.append(extractMosVal(testName, i, delay, nodeSplit, "hostVIP"))

    #     plt.plot(tps,mosValues)
    #     plt.savefig("../exports/plots/" + makeFullScenarioName(testName,nodeSplit) +".png")

# prepareMosValsForHeatmap('heatMapTest_SSH', [5,10,150,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95, or tp= 1000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620])
# prepareMosValsForHeatmap('heatMapTest_VoIP', [555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980])
# prepareMosValsForHeatmap('heatMapTest_VoIPnewSettings', [540,542,544,546,548,550,552,554,556,558,560,562,564,566,568,570,572,574,576,578,580,582,584,586,588,590,592,594,596,598,600], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800])
# prepareMosValsForHeatmap('heatMapTest_Video', [250,290,330,370,410,450,490,530,570,610,650,690,730,770,810,850,890,930,970,1010,1050,1090,1130,1170,1210,1250,1290,1330,1370,1410,1450,1490,1530], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_VideoV2', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoV2', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_NewLiveVideoClient', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_NewLiveVideoClient', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoV2', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideo', [250,290,330,370,410,450,490,530,570,610,650,690,730,770,810,850,890,930,970,1010,1050,1090,1130,1170,1210,1250,1290,1330,1370,1410,1450,1490,1530], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_FileDownload', [250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_FileDownload2-5MB', [250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])

# prepareMosValsForHeatmap('heatMapTest_VideoFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_FileDownloadFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_VideoLong', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoFineLong', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineShort', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineLong', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoShort', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoLong', [50+i*300 for i in range(33)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_VoIP_corrected', [x for x in range(5,56)], [x*20 for x in range(0,50)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineLongV2', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoFineLongV2', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])
#prepareMosValsForHeatmap('heatMapTest_FileDownloadFineV3', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])

#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability100',[x for x in range(500,5100, or tp= 1000)], [x for x in range(0,1000,20)])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability10s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[0, 0, 0, 0, 10,0])


#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[numVID, numLVD, numFDO, numSSH, numVIP,numcVP, numcF, numcLV])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[0, 0, 0, 0, 10,0])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s100',[x for x in range(500,3000, or tp= 1000)], [20],[0, 0, 0, 0,  or tp= 1000,0])


#countMOS()
#'heatMapTest_VoIP_scalability1s10','heatMapTest_VoIP_scalability10s10',"heatMapTest_VoIP_scalability10s1","heatMapTest_VoIP_scalability1s1"



#plotMosVsBw(["heatMapTest_VoIP_scalability10s1Queue10000","heatMapTest_VoIP_scalability10s100Queue10000","heatMapTest_VoIP_scalability10s1000Queue10000"],[x for x in range(50,300,10)],20,[0, 0, 0, 0, 10,0])
#plotMosVsBw(["heatMapTest_VoIP_scale10","heatMapTest_VoIP_scale50","heatMapTest_VoIP_scale100","heatMapTest_VoIP_scale1000"],[x for x in range(5,30,1)],20,[0, 0, 0, 0, 1,0])
#plotMosVsBw(["heatMapTest_VoIP_scale1","heatMapTest_VoIP_scale5","heatMapTest_VoIP_scale10","heatMapTest_VoIP_scale50","heatMapTest_VoIP_scale100","heatMapTest_VoIP_scale500","heatMapTest_VoIP_scale1000"],[x for x in range(5,30,1)],20,[0, 0, 0, 0, 1,0])



#

def extractTPtimeSeries(testNames, numCLI, nodeTypes, nodeSplit, nodeType, nodeNumOriginal, tpsOriginal, delays):
    allData=pd.DataFrame() 
    for testName in testNames: 
        multiplier = testName.split("scale")[1].split("tcp")[0]
        print(multiplier)
        numCLI = numCLI*int(multiplier)
        nodeNum= nodeNumOriginal*int(multiplier)
        tps = [x * int(multiplier) for x in tpsOriginal]
        print(tps)
        for tp in tps:
            print(tp)
            if tp/int(multiplier) == 1400:
                print("before delay")
                for delay in delays:
                    meanPerClient = []
                    AllClients = []
                    print("before node iteration")
                    for node in range(nodeNum):
                        print("Node is " + str(node))
                        if node == 1 or node ==int(multiplier) - 1:
                            host = nodeType + str(node)
                            df = importDF(testName, tp, delay,[x * int(multiplier) for x in nodeSplit], host) 
                            colNoTS = df.columns.get_loc(df.filter(like="rxPkOk").columns[0])
                            tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                            tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'bytes'}, inplace = True)
                            tB = [0,1] # time bounds for calculation
                            #print(tempDF.to_string())
                            colName = 'Downlink Throughput ' + makeNodeIdentifier(nodeType, nodeNum)
                            tpDirDF = pd.DataFrame(columns=[colName])
                            while tB[1] <= 400:
                                
                                throughput = tempDF.loc[(tempDF['ts'] > tB[0]) & (tempDF['ts'] <= tB[1])]["bytes"].sum()
                                tpDirDF = tpDirDF.append({colName : throughput*8/1000}, ignore_index=True)
                            
                                tB = [x+1 for x in tB]
                            #plt.plot([x for x in range(len(tpDirDF))], tpDirDF, label="host" + str(node))
                            data_x = []
                            for i in tpDirDF.values.tolist():
                            #     #print(i.type())
                                for elem in i:
                                    data_x.append(elem)
                                
                            print(data_x) #all values for one client
                            plt.plot([x for x in range(0,400)],data_x, label="node"+str(node))
                    plt.xlabel("Time [s]")
                    plt.xlim(0,50)
                    plt.ylabel("Throughput time series")
                    plt.savefig("../exports/plots/TPtimeSeries_" + testName + ".png")
                   
                        












def extractTPperClient(testNames, numCLI, nodeTypes, nodeSplit, nodeType, nodeNumOriginal, tpsOriginal, delays):
    allData=pd.DataFrame() 
    for testName in testNames: 
        multiplier = testName.split("scale")[1].split("tcp")[0]
        print(multiplier)
        numCLI = numCLI*int(multiplier)
        nodeNum= nodeNumOriginal*int(multiplier)
        tps = [x * int(multiplier) for x in tpsOriginal]
        print(tps)
        for tp in tps:
            print(tp)
            if tp/int(multiplier) == 1400:
                print("before delay")
                for delay in delays:
                    meanPerClient = []
                    AllClients = []
                    print("before node iteration")
                    for node in range(nodeNum):
                        print("Node is " + str(node))
                    # if node == 10 or node ==52 or node == 37 or node==45 or node ==2 or node ==24 or node ==7 or node==78 or node==94:
                        host = nodeType + str(node)
                        df = importDF(testName, tp, delay,[x * int(multiplier) for x in nodeSplit], host) 
                        colNoTS = df.columns.get_loc(df.filter(like="rxPkOk").columns[0])
                        tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                        tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'bytes'}, inplace = True)
                        tB = [0,1] # time bounds for calculation
                        #print(tempDF.to_string())
                        colName = 'Downlink Throughput ' + makeNodeIdentifier(nodeType, nodeNum)
                        tpDirDF = pd.DataFrame(columns=[colName])
                        while tB[1] <= 400:
                            
                            throughput = tempDF.loc[(tempDF['ts'] > tB[0]) & (tempDF['ts'] <= tB[1])]["bytes"].sum()
                            tpDirDF = tpDirDF.append({colName : throughput*8/1000}, ignore_index=True)
                        
                            tB = [x+1 for x in tB]
                        #plt.plot([x for x in range(len(tpDirDF))], tpDirDF, label="host" + str(node))
                        data_x = []
                        for i in tpDirDF.values.tolist():
                        #     #print(i.type())
                            for elem in i:
                                data_x.append(elem)
                            
                        print(data_x) #all values for one client
                        
                    
                        meanPerClient.append(statistics.mean(data_x))
                        #meanPerClient.extend(data_x)
                        print(meanPerClient)
                    AllClients.append(meanPerClient) 
                    print(AllClients)   
                allData=pd.concat([allData, pd.DataFrame(meanPerClient, columns=[str(multiplier)])], axis=1)
                print(allData)
                        # data_x = np.sort(meanPerClient)
                        # data_y = np.arange(len(meanPerClient)) / len(meanPerClient)
                        # plt.plot(data_x, data_y, marker='o', label="node" + str(node))
                        # #plt.legend()
                        # plt.xlabel("TP")
                        # #plt.xlim(0,4000)
                        # plt.ylabel("CDF")
                        # plt.savefig("../exports/plots/cdfTpAllValues_" + testName + ".png")
        
    bp=allData.boxplot(showmeans = True, meanline = True)
    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')
    plt.legend()
    #plt.ylim(600,1400)
    plt.xlabel("Number of clients")
    plt.ylabel("Throughput (all values) ")
    plt.savefig("../exports/plots/BoTpMeanValues_" + testName + ".png")
    #plt.savefig("../exports/plots/BoxVideoBufferMean_" + testName + ".png")
    

def extractTPCoeffVarPerClient(testNames, numCLI, nodeTypes, nodeSplit, nodeType, nodeNumOriginal, tpsOriginal, delays):
    allData=pd.DataFrame() 
    for testName in testNames: 
        multiplier = testName.split("scale")[1].split("tcp")[0]
        print(multiplier)
        numCLI = numCLI*int(multiplier)
        nodeNum= nodeNumOriginal*int(multiplier)
        tps = [x * int(multiplier) for x in tpsOriginal]
        for tp in tps:
            if tp/int(multiplier) == 1400:
                for delay in delays:
                    meanPerClient = []
                    AllClients = []
                    for node in range(nodeNum):
                        print("Node is " + str(node))
                    # if node == 10 or node ==52 or node == 37 or node==45 or node ==2 or node ==24 or node ==7 or node==78 or node==94:
                        host = nodeType + str(node)
                        df = importDF(testName, tp, delay,[x * int(multiplier) for x in nodeSplit], host) 
                        colNoTS = df.columns.get_loc(df.filter(like="rxPkOk").columns[0])
                        tempDF = df.iloc[:,[colNoTS,colNoTS+1]].dropna()
                        tempDF.rename(columns={tempDF.columns[0]: "ts", tempDF.columns[1]:'bytes'}, inplace = True)
                        tB = [0,1] # time bounds for calculation
                        #print(tempDF.to_string())
                        colName = 'Downlink Throughput ' + makeNodeIdentifier(nodeType, nodeNum)
                        tpDirDF = pd.DataFrame(columns=[colName])
                        while tB[1] <= 400:
                            
                            throughput = tempDF.loc[(tempDF['ts'] > tB[0]) & (tempDF['ts'] <= tB[1])]["bytes"].sum()
                            tpDirDF = tpDirDF.append({colName : throughput*8/1000}, ignore_index=True)
                        
                            tB = [x+1 for x in tB]
                        #plt.plot([x for x in range(len(tpDirDF))], tpDirDF, label="host" + str(node))
                        data_x = []
                        for i in tpDirDF.values.tolist():
                        #     #print(i.type())
                            for elem in i:
                                data_x.append(elem)
                            
                        #print(data_x) #all values for one client
                        
                    
                        #meanPerClient.append(statistics.stdev(filter(lambda num: num != 0, data_x))/statistics.mean(filter(lambda num: num != 0, data_x )))
                        meanPerClient.append(statistics.mean(filter(lambda num: num != 0, data_x )))

                        #meanPerClient.extend(data_x)
                        #print(meanPerClient)
                    AllClients.append(meanPerClient) 
                    print(AllClients)   
                allData=pd.concat([allData, pd.DataFrame(meanPerClient, columns=[str(multiplier)])], axis=1)
                print(allData)
                        # data_x = np.sort(meanPerClient)
                        # data_y = np.arange(len(meanPerClient)) / len(meanPerClient)
                        # plt.plot(data_x, data_y, marker='o', label="node" + str(node))
                        # #plt.legend()
                        # plt.xlabel("TP")
                        # #plt.xlim(0,4000)
                        # plt.ylabel("CDF")
                        # plt.savefig("../exports/plots/cdfTpAllValues_" + testName + ".png")
        
    bp=allData.boxplot(showmeans = True, meanline = True)
    plt.plot([], [], '-', linewidth=1, color='green', label='median')
    plt.plot([], [], '--', linewidth=1, color='green', label='mean')
    plt.legend()
    #plt.ylim(600,1400)
    plt.xlabel("Number of clients")
    plt.ylabel("Coefficient of variation throughput")
    plt.savefig("../exports/plots/BoTpCoeffVarValues_" + testName + ".png")
    #plt.savefig("../exports/plots/BoxVideoBufferMean_" + testName + ".png")
  




def getStallings(filenames, tps, tp, numCli):
    allData=pd.DataFrame()
    for filename in filenames:
        
        multiplier = filename.split(".csv")[0].split("stallings")[1]
        df = pd.read_csv ("/mnt/data/improved5gNS/analysis/code/videoMOScalcFiles/code/" + filename)
        begin = int(multiplier)*tps.index(tp)
        end = int(multiplier)*tps.index(tp)+int(multiplier)
        print(begin)
        print(end)
        dfExtracted = df.iloc[begin:end]
        print("Maximum count of stallings for tp" + str(tp) +  "is:" + str(max(dfExtracted.iloc[:, 0])))
        print("Macimum duration of stalllings for tp" + str(tp) +  "is:" + str(max(dfExtracted.iloc[:, 1])))
        print("Average count of stalllings for tp" + str(tp) +  "is:" + str(statistics.mean(dfExtracted.iloc[:, 0])))
        print("Average duration of stalllings for tp" + str(tp) +  "is:" + str(statistics.mean(dfExtracted.iloc[:, 1])))
        print("STDEV count of stalllings for tp" + str(tp) +  "is:" + str(statistics.stdev(dfExtracted.iloc[:, 0])))
        print("STDEV duration of stalllings for tp" + str(tp) +  "is:" + str(statistics.stdev(dfExtracted.iloc[:, 1])))
        allData=pd.concat([allData, pd.DataFrame(dfExtracted.iloc[:, 1].tolist(), columns=[str(multiplier)])], axis=1)
        print(allData)
    bp=allData.boxplot(showmeans = True, meanline = True)
    
    #plt.ylim(2.5,5.0)
    plt.ylabel("Stallings duration")
    plt.xlabel("Number of clients")
    plt.savefig("../exports/plots/BoxAllStallings_duration" + filename + ".png") #+ "_" + testNames[1] _run0 
    plt.close()




applications = ["VID"] #,LVD ,"SSH","VIP","FDO"   
numberOfClients = [20,30,40,50,60] #50, or tp= 1000,200 5,10,50, or tp= 1000,200 ,20,40,60,80,90, or tp= 1000
#numberOfClients = [40,45,50,55] #50, or tp= 1000,200
#numberOfClients = [1,5,10] 
#numberOfClients = [10,15,20,30,40,45,60, or tp= 1000,200,300]
#numberOfClients = [ or tp= 1000,200,300,400,500] 
#numberOfClients = [400]

testNames = []
fileNames = []
#numberOfClients = [1]
#for num in numberOfClients:
    #prepareMosValsForHeatmap('queue6MbheatMapTestFDO_scale'+ str(num),[x for x in range( or tp= 1000*num,2800*num,20*num)], [20], [0, 0, 0, 0, 1*num, 0])
    #prepareAllMosValsForHeatmap('heatMapTestFDO_scale'+ str(num) + 'tcp' ,[1400*num], [20], [0, 0, 0, 0, 1*num, 0])
    #prepareMosValsForHeatmap('bwDelayHeatMapTestVIP_scale'+ str(num),[x for x in range(5*num,30*num,1*num)], [20], [0, 0, 0, 1*num, 0, 0])
    #plotMosVsBw(['heatMapTestFDO_scale' + str(num)],[x for x in range( or tp= 1000*num,2800*num,20*num)],20,[0, 0, 0, 0, 1*num,0], "hostFDO")
    #extractMeanMosAllThroughputs(['heatMapTestVID_scale' + str(num)],[x for x in range( or tp= 1000*num,1500*num,20*num)],20,[0, 1*num, 0, 0, 0, 0], "hostVID")
    #prepareMosValsForHeatmap('heatMapTestVID_scale' + str(num),[x for x in range( or tp= 1000*num,1500*num,20*num)], [20], [0, 1*num, 0, 0, 0, 0])
    #prepareMosValsForHeatmap('heatMapTestLVD_scale' + str(num),[x for x in range( or tp= 1000*num,1900*num,20*num)], [20], [1*num, 0, 0, 0, 0, 0])
    #prepareMosValsForHeatmap('heatMapTestqueue10000SSH_scale' + str(num),[x for x in range(5*num,10*num,1*num)], [20], [0, 0, 1*num, 0, 0, 0])


for app in applications:
    testNames = []
    if app == "VID":
        print("in if")
        nodeSplit = [0, 1, 0, 0, 0, 0]
        #tps = [x for x in range( or tp= 1000,1520,20)]
        #tps = [x for x in range( 100,1520,20)]
        #tps=[560,660]
        #tps=[1400]
        tps=[100, 563, 1575]
    elif app == "SSH":
        nodeSplit = [0, 0, 1, 0, 0, 0]
        tps = [x for x in range(5,11,1)]
    elif app == "LVD":
        nodeSplit = [1, 0, 0, 0, 0, 0]
        tps = [x for x in range( 1000,1920,20)]
        #tps = [x for x in range( or tp= 1000,1920,20)]
    elif app == "VIP":
        nodeSplit = [0, 0, 0, 1, 0, 0]
        tps = [x for x in range(5,30,1)]
    elif app == "FDO":
        nodeSplit = [0, 0, 0, 0, 1, 0]
        tps = [x for x in range(100,2800,20)]
    print(nodeSplit)
    fileNames= ["testqueue12Mb"]#,"queue3Mb",
    #scenarios=[]
    for fileName in fileNames:
        scenarios=[]
        for num in numberOfClients:
            #testNames.append("smallQueueheatMapTest"+ app + "_scale" + str(num))
            #testNames.append("queue6MbheatMapTest"+ app + "_scale" + str(num))
            #testNames.append("queue12MbheatMapTest"+ app + "_scale" + str(num))
            
            #testNames.append("v2heatMapTest"+ app + "_scale" + str(num))
            #testNames.append("bwDelayHeatMapTest"+ app + "_scale" + str(num))

            #testNames.append("queue112MbheatMapTest"+ app + "_scale" + str(num))
            #testNames.append("queue6MbheatMapTest"+ app + "_scale" + str(num))
            #testNames.append("heatMapTest"+ app + "_scale" + str(num)) #+ str(num)+"tcp"
            
            #testNames.append("queue3Mb"+ app + "_scale" + str(num))
            #testNames.append("queueBdpSqrt"+ app + "_scale" + str(num))
            scenarios.append(fileName + app + "_scale" + str(num))
        testNames.append(scenarios)
    print("here")        
    print(testNames)
    print("here")
            #testNames.append("queue6Mb"+ app + "_scale" + str(num))
            #testNames.append("queue3Mb"+ app + "_scale" + str(num))
            
            #fileNames.append("stallings" + str(num) + ".csv")
            #testNames.append("heatMapTest"+ app + "repeat_scale" + str(num)+"tcp")
            #testNames.append("heatMapTest"+ app + "_scale" + str(num)+"tcpOffset")
    # getStallings("stallings20.csv", tps, 1400, 20)
    # getStallings("stallings30.csv", tps, 1400, 30)
    # getStallings("stallings40.csv", tps, 1400, 40)
    # getStallings("stallings45.csv", tps, 1400, 45)
    # getStallings("stallings60.csv", tps, 1400, 60)
    # getStallings("stallings100.csv", tps, 1400,  or tp= 1000)
    # getStallings("stallings300.csv", tps, 1400, 300)

    #getStallings(fileNames,tps,1400,500)
    #plotQueueBitLength(testNames, tps, 20, nodeSplit, "host" + app)
    #extractMeanMosAllThroughputs(testNames, tps, 20, nodeSplit, "host" + app)
    #testNames=sorted(testNames)
    #
    #plotBoxQueueFullness(scenarios, tps, 20, nodeSplit, "host" + app)
    plotMosVsQueueFullness(testNames, tps, 20, nodeSplit, "host" + app)

    #plotBoxMOSvsNumCli(testNames, tps, 20, nodeSplit, "host" + app)
    #videoQualityBox(testNames, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'],  [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', tps, [20])
    #cwnd(scenarios, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'],  [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', tps, [20])
    #rcvWnd(scenarios, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'],  [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', tps, [20])
    #cwnd(testNames, nodeSplit[4], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0, 0, 0, 0,nodeSplit[4], 0], 'hostFDO', tps, [20])
    #extractTPtimeSeries(testNames, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', nodeSplit[1], tps, [20])
    #extractTPtimeSeries(testNames, nodeSplit[4], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0, 0, 0, 0,nodeSplit[4], 0], 'hostFDO', nodeSplit[4], tps, [20])
    #extractTPperClient(testNames, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', nodeSplit[1], tps, [20])
    #extractTPCoeffVarPerClient(testNames, nodeSplit[1], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0,nodeSplit[1], 0, 0, 0, 0], 'hostVID', nodeSplit[1], tps, [20])
    #the next line is for FD
    #extractTPCoeffVarPerClient(testNames, nodeSplit[4], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0, 0, 0, 0,nodeSplit[4], 0], 'hostFDO', nodeSplit[4], tps, [20])
    #extractTPCoeffVarPerClient(testNames, nodeSplit[4], ['hostVID', 'hostLVD', 'hostFDO', 'hostSSH', 'hostVIP', 'hostHVIP'], [0, 0, 0, 0,nodeSplit[4], 0], 'hostFDO', nodeSplit[4], tps, [20])
    #plotBoxDroppedQueue(testNames, tps, 20, nodeSplit, "host" + app)
    #plotBoxQueueFullness(scenarios, tps, 20, nodeSplit, "host" + app)

    

    #plotGainTotalMeanMos(testNames, tps, 20, 20, nodeSplit, "host" + app)
    #prepare4Dcsv(testNames,nodeSplit)
    #plot4dHeatmap("heatMapTestVIP_scale200", tps, [20], [1,5,10,50,200])
    #




def plotBwVs35(testNames, tps, delay,nodeSplit):
    mosValues = {} #initialize array and save all points in there
    minTP = []
    multipliers = []
    tpsOriginal=tps
    name = ""
    for testName in testNames:
        name += testName + "_"
        multiplier = testName.split("scale")[1]
        multipliers.append(multiplier)
        print(multiplier)
        mosValues[testName]=[]
        for i in tps:
            mosValues[testName].append(extractMosVal(testName, i*int(multiplier), delay,  [ns *  int(multiplier) for ns in nodeSplit], "hostVIP"))
        print(tpsOriginal)

        for i in mosValues[testName]:
            if i>3.5:
                minTP.append(mosValues[testName].index(i)+5)
                break
    plt.xlim(0, 100)
 
    
    plt.plot(multipliers,minTP)
    plt.xlabel("Num. of clients")
    plt.ylabel("BW needed for MOS 3.5")
  

    plt.savefig("../exports/plots/comparisson35_" + name + ".png") #+ "_" + testNames[1] 
  
    # if not os.path.exists('../exports/heatMap/'):
    #     os.makedirs('../exports/heatMap/')
    # with open('../exports/heatMap/'+makeFullScenarioName(testName,nodeSplit)+'.csv', mode='w') as writeFile:
    #     fw = csv.writer(writeFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    #     fw.writerow(xAxis)
    #     fw.writerow(yAxis)
    #     fw.writerow(mosMap)
    # for i in testNames:
    #     mosValues = [] #initialize array and save all points in there
    #     for i in tps:
    #     mosValues.append(extractMosVal(testName, i, delay, nodeSplit, "hostVIP"))

    #     plt.plot(tps,mosValues)
    #     plt.savefig("../exports/plots/" + makeFullScenarioName(testName,nodeSplit) +".png")

# prepareMosValsForHeatmap('heatMapTest_SSH', [5,10,150,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95, or tp= 1000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620])
# prepareMosValsForHeatmap('heatMapTest_VoIP', [555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980])
# prepareMosValsForHeatmap('heatMapTest_VoIPnewSettings', [540,542,544,546,548,550,552,554,556,558,560,562,564,566,568,570,572,574,576,578,580,582,584,586,588,590,592,594,596,598,600], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800])
# prepareMosValsForHeatmap('heatMapTest_Video', [250,290,330,370,410,450,490,530,570,610,650,690,730,770,810,850,890,930,970,1010,1050,1090,1130,1170,1210,1250,1290,1330,1370,1410,1450,1490,1530], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_VideoV2', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoV2', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_NewLiveVideoClient', [50,150,250,350,450,550,650,750,850,950,1050,1150,1250,1350,1450,1550,1650,1750,1850,1950,2050,2150,2250,2350,2450,2550,2650,2750,2850,2950,3050,3150,3250], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_NewLiveVideoClient', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoV2', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideo', [250,290,330,370,410,450,490,530,570,610,650,690,730,770,810,850,890,930,970,1010,1050,1090,1130,1170,1210,1250,1290,1330,1370,1410,1450,1490,1530], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_FileDownload', [250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])
# prepareMosValsForHeatmap('heatMapTest_FileDownload2-5MB', [250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000], [0,20,40,60,80, or tp= 1000,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600])

# prepareMosValsForHeatmap('heatMapTest_VideoFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_FileDownloadFine', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_VideoLong', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoFineLong', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineShort', [i*20 for i in range(1,51)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineLong', [i*20 for i in range(1,51)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoShort', [50+i*300 for i in range(33)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_LiveVideoLong', [50+i*300 for i in range(33)], [i*20 for i in range(31)])

# prepareMosValsForHeatmap('heatMapTest_VoIP_corrected', [x for x in range(5,56)], [x*20 for x in range(0,50)])

# prepareMosValsForHeatmap('heatMapTest_LiveVideoFineLongV2', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])
# prepareMosValsForHeatmap('heatMapTest_VideoFineLongV2', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])
#prepareMosValsForHeatmap('heatMapTest_FileDownloadFineV3', [ or tp= 1000+x*20 for x in range(226)], [i*20 for i in range(31)])

#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability100',[x for x in range(500,5100, or tp= 1000)], [x for x in range(0,1000,20)])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability10s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[0, 0, 0, 0, 10,0])


#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[numVID, numLVD, numFDO, numSSH, numVIP,numcVP, numcF, numcLV])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s10',[x for x in range(50,510,10)], [x for x in range(0,1000,20)],[0, 0, 0, 0, 10,0])
#prepareMosValsForHeatmap('heatMapTest_VoIP_scalability1s100',[x for x in range(500,3000, or tp= 1000)], [20],[0,ss 0, 0, 0,  or tp= 1000,0])
#countMOS()
#'heatMapTest_VoIP_scalability1s10','heatMapTest_VoIP_scalability10s10',"heatMapTest_VoIP_scalability10s1","heatMapTest_VoIP_scalability1s1"
#plotMosVsBw(['heatMapTest_VoIP_scalability1s100Queue500',"heatMapTest_VoIP_scalability1s100NoOffset","heatMapTest_VoIP_scalability10s1000Queue10000"],[x for x in range(50,300,10)],20,[0, 0, 0, 0, 10,0])


#plotMosVsBw(["heatMapTest_VoIP_scalability10s1Queue10000","heatMapTest_VoIP_scalability10s100Queue10000","heatMapTest_VoIP_scalability10s1000Queue10000"],[x for x in range(50,300,10)],20,[0, 0, 0, 0, 10,0]),"heatMapTest_VoIP_scale50","heatMapTest_VoIP_scale100","heatMapTest_VoIP_scale500","heatMapTest_VoIP_scale1000"

#plotBwVs35(["heatMapTest_VoIP_scale1","heatMapTest_VoIP_scale5","heatMapTest_VoIP_scale10","heatMapTest_VoIP_scale50","heatMapTest_VoIP_scale100","heatMapTest_VoIP_scale500","heatMapTest_VoIP_scale1000"],[x for x in range(5,30,1)],20,[0, 0, 0, 0, 1,0])







