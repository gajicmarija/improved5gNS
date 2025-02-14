from cfgGenLib_new import *
import math
import numpy as np
import itertools, operator

#function for generation of all combinations for RA, assuming voip and ssh take 2mbps this means 98 for rest pr 97*96/2 total combinations
def genCombinations(num):
    combo=set()
    for cuts in itertools.combinations_with_replacement(range(1,num), 3):
        if(sum(cuts)==num):
            for i in set(itertools.permutations(cuts)):
                combo.add(i)
    return combo

# REMINDER: if app A has priority 0 and app B has priority 1, app A will get preferential treatment.

def gen_cfg(cfgName, useTwoLevelHTB):

    # IP settings don't change from scenario to scenario.
    hostIPs = OrderedDict([('VIP', '10.0.x.x'), ('LVD', '10.1.x.x'), ('VID', '10.2.x.x'), ('FDO', '10.3.x.x'), ('SSH', '10.4.x.x'),('HVIP', '10.5.x.x')])
    serverIPs = OrderedDict([('VIP', '10.10.0.0'), ('LVD', '10.11.0.0'), ('VID', '10.12.0.0'), ('FDO', '10.13.0.0'), ('SSH', '10.14.0.0'),('HVIP', '10.15.x.x')])
    
    #hostIPs2S = OrderedDict([('VIP', '10.20.x.x'), ('LVD', '10.21.x.x'), ('VID', '10.22.x.x'), ('FDO', '10.23.x.x'), ('SSH', '10.24.x.x'),('cVP', '10.5.x.x'),('cF', '10.6.x.x'),('cLV', '10.7.x.x')])
    #serverIPs2S = OrderedDict([('VIP', '10.220.0.0'), ('LVD', '10.221.0.0'), ('VID', '10.222.0.0'), ('FDO', '10.223.0.0'), ('SSH', '10.224.0.0'),('cVP', '10.15.x.x'),('cF', '10.16.x.x'),('cLV', '10.17.x.x')])    

    # myCfg-001 -- VIP + LVD, no prio
    if cfgName == 'myCfg-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 15e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-002 -- VIP + LVD, with prio
    elif cfgName == 'myCfg-002':
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 15e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-003 -- LVD + VID scenario, no prio
    elif cfgName == 'myCfg-003':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-004 -- LVD + VID scenario, with prio
    elif cfgName == 'myCfg-004':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 1), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-005 -- LVD + VID scenario, with prio, but inverted
    elif cfgName == 'myCfg-005':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 1), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-006 -- LVD + VID scenario, with prio, but inverted -- copy of 005
    elif cfgName == 'myCfg-006':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 1), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-007 -- LVD + VID scenario, no prio
    elif cfgName == 'myCfg-007':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # myCfg-008 -- LVD + VID scenario, no prio -- copy of 007 -- used for 2-level version
    elif cfgName == 'myCfg-008':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 0), ('LVD', 30), ('VID', 30), ('FDO', 0), ('SSH', 0)])
        rate = 50e6
        bwSplits = [OrderedDict([('VIP', 0), ('LVD', round((100 - p) * .01 * rate)), ('VID', round(p * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # cfg-voip-lvd-001 -- LVD + VIP scenario, no prio
    elif cfgName == 'cfg-voip-lvd-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # cfg-voip-lvd-002 -- LVD + VIP scenario, no prio -- copy of 001 -- used for 2-level version
    elif cfgName == 'cfg-voip-lvd-002':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 10), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', round((100 - p) * .01 * rate)), ('VID', 0), ('FDO', 0), ('SSH', 0)]) for p in range(10, 100, 10)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    elif cfgName == 'cfg-voip-vod-fdl-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 2), ('LVD', 0), ('VID', 2), ('FDO', 2), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(.33 * rate)), ('LVD', 0), ('VID', round(.33 * rate)), ('FDO', round(.33 * rate)), ('SSH', 0)])]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    # 'cfg-fakevoip-vod-001' -- VoIP + VoD, 5% split steps, no prios.
    elif cfgName == 'cfg-fakevoip-vod-001':
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 20), ('LVD', 0), ('VID', 20), ('FDO', 0), ('SSH', 0)])
        rate = 25e6
        bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', 0), ('VID', round((100 - p) * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(5, 100, 5)]
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
    elif cfgName == '':
        bwSplits = []
        hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0)])
        hostNumbers = OrderedDict([('VIP', 35), ('LVD', 39), ('VID', 49), ('FDO', 41), ('SSH', 31)])
        rate = 100e6 #rate is in bytes
        baseCfgName = 'liteCbaselineTestTokenQoS_base'   
        setCombinations=genCombinations(98) 
        for i in setCombinations:
            cfgName=""
            bwSplits = []
            x = np.random.randint(0, 98, size=(3,))
            while sum(x) != 98: x = np.random.randint(10, 98, size=(3,))
            #x= x*1000000#because it is in bytes
            #bwSplits = [OrderedDict([('VIP', round(p * .01 * rate)), ('LVD', 0), ('VID', round((100 - p) * .01 * rate)), ('FDO', 0), ('SSH', 0)]) for p in range(5, 100, 5)]
            bwSplits.append(OrderedDict([('VIP', 1500000), ('LVD', i[0]*1000000), ('VID', i[1]*1000000), ('FDO', i[2]*1000000), ('SSH', 500000)]))
            cfgName+="v1500l%sd%sf%ss500" % (i[0],i[1],i[2])
            print(cfgName)
            generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, useTwoLevelHTB)
    elif cfgName=="zeroNoDisaster":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 9600000), ('LVD',286000000), ('VID',462000000), ('FDO',224000000), ('SSH',500000),('cVP', 120000),('cF', 11200000),('cLV', 5500000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 242), ('FDO', 1), ('SSH', 1),('cVP', 1),('cF', 1),('cLV', 1)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB) 
    elif cfgName=="Ddisaster8S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 260), ('VID', 485), ('FDO', 100), ('SSH', 100),('cVP', 100),('cF', 50),('cLV', 10)])
        percentage = [20,50,80]
        for i in percentage:
            bwSplits = []
            ceiling = []
            cfgName="Ddisaster8S"
            bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
            ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            rate = 2*1000*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceiling, rate, useTwoLevelHTB)
    elif cfgName=="Ddisaster2S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios2S = OrderedDict([('nonCritical', 1),('critical', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 260), ('VID', 485), ('FDO', 100), ('SSH', 100),('cVP', 100),('cF', 50),('cLV', 10)])
        percentage = [20,50,80]
        for i in percentage:
        #for i in range (10,100,10):
            bwSplits2S = []
            ceiling2S = []
            cfgName="Ddisaster2S"
            bwSplits2S.append(OrderedDict([('nonCritical', 0),('critical', 2*1000e6*(i/100))]))
            ceiling2S.append(OrderedDict([('nonCritical', 2*1000e6*(i/100)),('critical', 2*1000e6*(i/100))]))
            rate = 2*1000e6*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil2S(cfgName, baseCfgName, hostNumbers, hostPrios2S, hostIPs2S, serverIPs2S, bwSplits2S, ceiling2S,rate, useTwoLevelHTB) 
    elif cfgName=="cnsm":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 1750000), ('LVD',70000000), ('VID',54000000), ('FDO',5200000), ('SSH',70000),('cVP', 250000),('cF', 7800000),('cLV', 12500000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 35), ('LVD', 28), ('VID', 45), ('FDO', 2), ('SSH', 10),('cVP', 5),('cF', 3),('cLV', 5)])
        rate = 1000 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB)
    elif cfgName=="finalNoDisaster":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',700000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 250000000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 280), ('VID', 450), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 100)])
        rate = 1800 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB)  
    elif cfgName=="Ddisaster8S":
        baseCfgName = 'liteCbaselineTestTokenQoS_base'
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 400), ('LVD', 260), ('VID', 485), ('FDO', 100), ('SSH', 100),('cVP', 100),('cF', 50),('cLV', 10)])
        percentage = [20,50,80]
        for i in percentage:
            bwSplits = []
            ceiling = []
            cfgName="Ddisaster8S"
            bwSplits.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('cVP', 2*19000000*(i/100)),('cF', 2*896000000*(i/100)),('cLV', 2*85000000*(i/100))]))
            ceiling.append(OrderedDict([('VIP', 2*9600000), ('LVD',2*286000000*(i/100)), ('VID',2*461000000*(i/100)), ('FDO',2*224000000*(i/100)), ('SSH',2*500000*(i/100)),('cVP', 2*1000e6*(i/100)),('cF', 2*1000e6*(i/100)),('cLV', 2*1000e6*(i/100))]))
            rate = 2*1000*(i/100) #rate is in bytes
            cfgName+="%s" % (i)
            generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits, ceiling, rate, useTwoLevelHTB)
    elif cfgName=="testLVD":
        bwSplits = []
        bwSplits.append(OrderedDict([('VIP', 17500000), ('LVD',10000000), ('VID',540000000), ('FDO',52000000), ('SSH',700000),('cVP', 5000000),('cF', 156000000),('cLV', 10000000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1), ('SSH', 1),('cVP', 0),('cF', 0),('cLV', 0)])
        hostNumbers = OrderedDict([('VIP', 350), ('LVD', 2), ('VID', 450), ('FDO', 20), ('SSH', 100),('cVP', 100),('cF', 60),('cLV', 2)])
        rate = 1800 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, bwSplits,rate, useTwoLevelHTB) 
    elif cfgName=="cnsmcVIP":
        assured = []
        ceiling = []
        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        assured.append(OrderedDict([('VIP', 24000), ('LVD',1092000), ('VID',952000), ('FDO',2240000), ('SSH',5000),('cVP', 240000)]))
        ceiling.append(OrderedDict([('VIP', 60000), ('LVD',2730000), ('VID',1400000), ('FDO',2800000), ('SSH',10000),('cVP', 600000)]))
        hostPrios = OrderedDict([('VIP', 1), ('LVD', 1), ('VID', 1), ('FDO', 1),('cVP', 1)])
        hostNumbers = OrderedDict([('VIP', 40), ('LVD', 28), ('VID', 50), ('FDO', 5), ('SSH', 10),('cVP', 40)])
        rate = 105 
        baseCfgName = 'liteCbaselineTestTokenQoS_base'  
        generate_all_config_files_ceil(cfgName, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, useTwoLevelHTB)
    elif cfgName=="bufferStudiesNoFlowsV2VoD": #3Mb_GBR100"
        multipliers = [100, 85, 80, 50]
        numberOfClients = 50
        queueSizes = [65535*4,65535*8, 1120*10, int(1120*20/math.sqrt(numberOfClients)), 1120*20] #in bits
        #queueSizes = [int(1120*20/math.sqrt(numberOfClients))]
        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
           
            for queueSize in queueSizes:
                assured = []
                ceiling = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(numberOfClients*100/multiplier)
                else:     
                    queueSize = queueSize * numberOfClients
                assured.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceiling.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)
      
    elif cfgName=="bufferStudiesNoFlowsLVD": #3Mb_GBR100"
        multipliers = [100, 85, 80, 50]
        numberOfClients = 28
        queueSizes = [65535*4,65535*8, 1820*10, 1820*20] #in kilobits
        queueSizes = [int(1820*20/math.sqrt(numberOfClients))]
        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
        
            for queueSize in queueSizes:
                assured = []
                ceiling = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(28*100/multiplier)
                else:     
                    queueSize = queueSize * 28
                assured.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceiling.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="bufferStudiesNoFlowsFDO": #3Mb_GBR100"
        multipliers = [100, 85, 80, 50]
        numberOfClients = 5
        queueSizes = [65535*4,65535*8, 2240*10, (2240*20)/math.sqrt(numberOfClients), 2240*20] #in kilobits
        queueSizes = [int((2240*20)/math.sqrt(numberOfClients))]
        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assured = []
                ceiling = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(numberOfClients*100/multiplier)
                else:     
                    queueSize = queueSize * numberOfClients
                assured.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceiling.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="bufferStudiesQoSFlowsFDOV1": #3Mb_GBR100"
        multipliers = [100,85,80,50]
        numberOfClients = 5
        queueSizes = [65535*4,65535*8, 2240*10, int((2240*20)/math.sqrt(numberOfClients)), 2240*20] #in bits, per client
        

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                # if (queueSize % 65535 == 0):
                #     queueSize = queueSize * int(numberOfClients*100/multiplier)
                # else:     
                #     queueSize = queueSize * numberOfClients
                #set GBR and MBR for the slice/inner HTB node    
                assuredSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                #generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)   
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)  
    elif cfgName=="bufferStudiesQoSFlowsVoD": #3Mb_GBR100"
        multipliers = [100]#,85,80,50
        numberOfClients = 50
        queueSizes = [65535*4,65535*8, 1120*10, 1120*20] #in bits
        queueSizes =[1120*40]

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 != 0):
                    queueSize = round(queueSize * multiplier/100)
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                # else:     
                #     queueSize = queueSize * numberOfClients
                #set GBR and MBR for the slice/inner HTB node    
                assuredSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                #generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)   
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)           
    elif cfgName=="bufferStudiesQoSFlowsLVD": #3Mb_GBR100"
        multipliers = [100,85,80,50]
        numberOfClients = 28
        queueSizes = [65535*4,65535*8, 1820*10, 1820*20]  #in bits

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                # if (queueSize % 65535 == 0):
                #     queueSize = queueSize * int(numberOfClients*100/multiplier)
                # else:     
                #     queueSize = queueSize * numberOfClients
                #set GBR and MBR for the slice/inner HTB node    
                assuredSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                #generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)   
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)           
    elif cfgName=="bufferStudiesQoSFlowsFDO": #3Mb_GBR100"
        multipliers = [85,80,50]
        numberOfClients = 5
        queueSizes = [65535*4,65535*8, 2240*10, 2240*20] #in bits, per client
        queueSizes = [2240*10, 2240*20]

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                
                queueSize = round(queueSize * multiplier/100)
                #set GBR and MBR for the slice/inner HTB node    
                assuredSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 1200000), ('LVD',50960000), ('VID',56000000), ('FDO',11200000), ('SSH',100000),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', round(1200000/int(40*100/multiplier))), ('LVD', round(50960000/int(28*100/multiplier))), ('VID', round(56000000/int(50*100/multiplier))), ('FDO', round(11200000/int(5*100/multiplier))), ('SSH', round(100000/int(10*100/multiplier))),('HVIP', 0)]))
                
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', round(40*100/multiplier)), ('LVD', round(28*100/multiplier)), ('VID', round(50*100/multiplier)), ('FDO', round(5*100/multiplier)), ('SSH', round(10*100/multiplier)),('HVIP', 0)])
                rate = 300 #in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                #generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assured,ceiling,rate, queueSize,  useTwoLevelHTB)   
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)     
    elif cfgName=="QoSFlowsVID": #3Mb_GBR100"
        multipliers = [100,85,80,50]#,85,80,50
        numberOfClients = 50
        queueSizes = [65535*4,65535*8, 1120*10, 1120*20] #in bits
        

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 != 0):
                    queueSize = round(queueSize * multiplier/100)
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',56000000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',56000000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', round(56000000/int(numberOfClients*100/multiplier))), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', round(56000000/int(numberOfClients*100/multiplier))), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', round(numberOfClients*100/multiplier)), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    elif cfgName=="QoSFlowsFDO": #3Mb_GBR100"
        multipliers = [100,85,80,50]#,85,80,50
        numberOfClients = 5
        queueSizes = [65535*4,65535*8,2240*20] #in bits
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 != 0):
                    queueSize = round(queueSize * multiplier/100)
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',11200000), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',11200000), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', round(11200000/int(numberOfClients*100/multiplier))), ('SSH', 0),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', round(11200000/int(numberOfClients*100/multiplier))), ('SSH', 0),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO',round(numberOfClients*100/multiplier)), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    elif cfgName=="QoSFlowsLVD": #3Mb_GBR100"
        multipliers = [100,85,80,50]#,85,80,50
        numberOfClients = 28
        queueSizes = [65535*4,65535*8,1820*20] #in bits
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 != 0):
                    queueSize = round(queueSize * multiplier/100) #BDP * 0.85
                
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',50960000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',50960000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', round(50960000/int(numberOfClients*100/multiplier))), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', round(50960000/int(numberOfClients*100/multiplier))), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD', round(numberOfClients*100/multiplier)), ('VID', 0), ('FDO',0), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    elif cfgName=="SliceNoFlowsVID": #3Mb_GBR100"
        multipliers = [100]#,85,80,50
        numberOfClients = 50
        queueSizes = [1120*10, int(1120*20/math.sqrt(numberOfClients)), 1120*20] #in bits 65535*4,65535*8, 
        

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(numberOfClients*100/multiplier)
                else:     
                    queueSize = queueSize * numberOfClients    
                print("Queue Size before quantization: ")
                print(queueSize)
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',56000000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',56000000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', round(numberOfClients*100/multiplier)), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="SliceNoFlowsFDO": #3Mb_GBR100"
        multipliers = [100,85,80,50]#,85,80,50
        numberOfClients = 5
        queueSizes = [65535*4,65535*8, 2240*10, int(2240*20/math.sqrt(numberOfClients)), 2240*20] #in bits
        queueSizes = [65535*4,65535*8, 2240*10, int((2240*20)/math.sqrt(numberOfClients)), 2240*20] #in bits, per client

        

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(numberOfClients*100/multiplier)
                else:     
                    queueSize = queueSize * numberOfClients    
                print("Queue Size before quantization: ")
                print(queueSize)
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',11200000), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',11200000), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', round(numberOfClients*100/multiplier)), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="SliceNoFlowsLVD": #3Mb_GBR100"
        multipliers = [100,85,80,50]#,85,80,50
        numberOfClients = 28
        queueSizes = [65535*4,65535*8, 18200*10, int(1820*20/math.sqrt(numberOfClients)), 1820*20] #in bits
        queueSizes = [1820*10]
    

        # assured.append(OrderedDict([('VIP', 96000), ('LVD',30576000), ('VID',47600000), ('FDO',11200000), ('SSH',50000),('cVP', 960000)]))
        # ceiling.append(OrderedDict([('VIP', 192000), ('LVD',45864000), ('VID',59500000), ('FDO',11400000), ('SSH',50000),('cVP', 1920000)]))
        for multiplier in multipliers:
            for queueSize in queueSizes:
                assuredSlice = []
                ceilingSlice = []
                assuredLeaf = []
                ceilingLeaf = []
                cfgNameNew = ""
                if (queueSize % 65535 == 0):
                    queueSize = queueSize * int(numberOfClients*100/multiplier)
                else:     
                    queueSize = queueSize * numberOfClients    
                print("Queue Size before quantization: ")
                print(queueSize)
                if (queueSize % (1499*8) !=0):
                    queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                print("------------------Queue size is: --------------------------")
                print(queueSize)
                print("-----multiplier is-------")
                print(multiplier)

                assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',50960000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',50960000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                #set GBR/MBR for QoS Flows/HTB leaves 
                hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                #set number of the leaves 
                hostNumbers = OrderedDict([('VIP', 0), ('LVD',round(numberOfClients*100/multiplier)), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                rate =  sum(assuredSlice[0].values())#in Mbps 
                baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                cfgNameNew = cfgName + str(queueSize) + "b" + "_GBR" + str(multiplier)
                print(cfgNameNew)
                generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="_gF_aVID": #3Mb_GBR100"
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*1120) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        queueSizesText = ["B","R2","R"]
        queueSizesText = ["5B","10B"]

        #additional runs
        queueSizesText = ["B","5B","10B","R"]


        for numCli in numberOfClients: 
            for tp in throughputs:
                queueSizes = [tp*20,65535*4,65535*8] #in bits
                queueSizes = [5*tp*20,10*tp*20]
                queueSizes = [tp*20,5*tp*20,10*tp*20,65535*8]
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    queueSize = queueSizeOriginal
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',numCli*tp*1000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',numCli*tp*1000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    #set GBR/MBR for QoS Flows/HTB leaves 
                    assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', tp*1000), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', tp*1000), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', numCli), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    
    elif cfgName=="_gS_aVID": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*1120) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        
        for numCli in numberOfClients: 
            if numCli!= 1:
                queueSizesText = ["T","B","R2","R"]
                #additional runs
                queueSizesText = ["T","B","5B","10B","R"]

            else: 
                queueSizesText = ["B","5B","10B","R"]
        

            for tp in throughputs:
                if numCli!= 1:
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,tp*20*5,tp*20*10,65535*8] #in bits
                else:
                    queueSizes = [tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20,tp*20*5,tp*20*10,65535*8]

                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    print("TP is")
                    print(tp)
                    queueSize = queueSizeOriginal*numCli
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',numCli*tp*1000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',numCli*tp*1000), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', numCli), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    print(numCli) 
                    print(cfgNameNew)  
                    generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="_gF_aLVD": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*1820) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        queueSizesText = ["B","R2","R"]
        queueSizesText = ["5B","10B"]
        #additional runs
        queueSizesText = ["B","5B","10B","R"]
        for numCli in numberOfClients: 
            for tp in throughputs:
                queueSizes = [tp*20,65535*4,65535*8] #in bits
                queueSizes = [5*tp*20,10*tp*20] #in bits
                queueSizes = [tp*20,5*tp*20,10*tp*20,65535*8]
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    queueSize = queueSizeOriginal
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',numCli*tp*1000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',numCli*tp*1000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    #set GBR/MBR for QoS Flows/HTB leaves 
                    assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', tp*1000), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', tp*1000), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', numCli), ('VID',0 ), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    
    elif cfgName=="_gS_aLVD": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*1820) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
        for numCli in numberOfClients: 
            if numCli!= 1:
                queueSizesText = ["T","B","R2","R"]
                queueSizesText = ["T","B","5B","10B","R"]
            else: 
                queueSizesText = ["B","R2","R"]
                queueSizesText = ["B","5B","10B","R"]
            
            
            for tp in throughputs:
                if numCli!= 1:
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,tp*20*5,tp*20*10,65535*8] #in bits
                else:
                    queueSizes = [tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20,tp*20*5,tp*20*10,65535*8] #in bits
            
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    print("TP is")
                    print(tp)
                    queueSize = queueSizeOriginal*numCli
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',numCli*tp*1000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',numCli*tp*1000), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', numCli), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    print(numCli) 
                    print(cfgNameNew)  
                    generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="_gF_aFDO": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        multipliers = [x for x in range(110,160,10)]
        #multipliers = [75,80,81]
        throughputs = [math.ceil((x/100)*2240) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
        #numberOfClients.extend([x for x in range(10,60,10)])
         
        queueSizesText = ["B","R2","R"]
        queueSizesText = ["5B","10B"]
        queueSizesText = ["B","5B","10B","R"]
        for numCli in numberOfClients: 
            for tp in throughputs:
                queueSizes = [tp*20,65535*4,65535*8] #in bits
                queueSizes = [tp*20,5*tp*20,10*tp*20,65535*8]
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    queueSize = queueSizeOriginal
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',numCli*tp*1000), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',numCli*tp*1000), ('SSH',0),('HVIP', 0)]))
                    #set GBR/MBR for QoS Flows/HTB leaves 
                    assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', tp*1000), ('SSH', 0),('HVIP', 0)]))
                    ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', tp*1000), ('SSH', 0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', numCli), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    
    elif cfgName=="_gS_aFDO": #3Mb_GBR100"
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*2240) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        
        for numCli in numberOfClients: 
            if numCli!= 1:
                queueSizesText = ["T","B","R2","R"]
                queueSizesText = ["T","B","5B","10B","R"]
            else: 
                queueSizesText = ["B","R2","R"]
                queueSizesText = ["B","5B","10B","R"]
         
            for tp in throughputs:
                if numCli!= 1:
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,tp*20*5,tp*20*10,65535*8] #in bits
                else:
                    queueSizes = [tp*20,65535*4,65535*8] #in bits
                    queueSizes = [tp*20,tp*20*5,tp*20*10,65535*8] #in bits
               
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    print("TP is")
                    print(tp)
                    queueSize = queueSizeOriginal*numCli
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',numCli*tp*1000), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',numCli*tp*1000), ('SSH',0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', numCli), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    print(numCli) 
                    print(cfgNameNew)  
                    generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="_gF_aVIP": #3Mb_GBR100"
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*30) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        queueSizesText = ["B","5B","10B"]
        queueSizesText = ["B","5B","10B"]
        
        for numCli in numberOfClients: 
            for tp in throughputs:
                queueSizes = [tp*20,tp*20*5,tp*20*10] #in bits
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    queueSize = queueSizeOriginal
                    #account for quantization of MSS in the queue
                    if (queueSize % (75*8) !=0):
                        queueSize = math.ceil(queueSize/(75 * 8))*75*8 #MSS = 1499B
                    assuredSlice.append(OrderedDict([('VIP', numCli*tp*1000), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', numCli*tp*1000), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    #set GBR/MBR for QoS Flows/HTB leaves 
                    assuredLeaf.append(OrderedDict([('VIP', tp*1000), ('LVD', 0), ('VID',0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    ceilingLeaf.append(OrderedDict([('VIP', tp*1000), ('LVD', 0), ('VID',0), ('FDO', 0), ('SSH', 0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', numCli), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    
    elif cfgName=="_gS_aVIP": #3Mb_GBR100"
        multipliers = [x for x in range(110,160,10)]
        throughputs = [math.ceil((x/100)*30) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
       
        for numCli in numberOfClients: 
            if numCli!= 1:
                queueSizesText = ["T","B","5B","10B"]
            else: 
                queueSizesText = ["B","5B","10B"]
            for tp in throughputs:
                if numCli!= 1:
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20, 5*tp*20, 10*tp*20] #in bits
                else:
                    queueSizes = [tp*20,5*tp*20, 10*tp*20] #in bits
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    print("TP is")
                    print(tp)
                    queueSize = queueSizeOriginal*numCli
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queue
                    if (queueSize % (75*8) !=0):
                        queueSize = math.ceil(queueSize/(75 * 8))*75*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', numCli*tp*1000), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', numCli*tp*1000), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',0),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', numCli), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', 0),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    print(numCli) 
                    print(cfgNameNew)  
                    generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
    elif cfgName=="_gF_aSSH": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        throughputs = [math.ceil((x/100)*10) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         
        queueSizesText = ["B","R2","R"]
        queueSizesText = ["5B","10B"]
        for numCli in numberOfClients: 
            for tp in throughputs:
                print(tp)
                queueSizes = [tp*20,65535*4,65535*8] #in bits
                queueSizes = [5*tp*20,10*tp*20]
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    queueSize = queueSizeOriginal
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',numCli*tp*1000),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',numCli*tp*1000),('HVIP', 0)]))
                    #set GBR/MBR for QoS Flows/HTB leaves 
                    assuredLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID',0), ('FDO', 0), ('SSH', tp*1000),('HVIP', 0)]))
                    ceilingLeaf.append(OrderedDict([('VIP', 0), ('LVD', 0), ('VID',0), ('FDO', 0), ('SSH', tp*1000),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', numCli),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    generate_all_config_files(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice, ceilingSlice,assuredLeaf,ceilingLeaf, rate, hostIPs, serverIPs, hostNumbers, queueSize, True)    
    
    elif cfgName=="_gS_aSSH": #3Mb_GBR100"
        multipliers = [x for x in range(50,110,10)]
        throughputs = [math.ceil((x/100)*10) for x in multipliers]
        numberOfClients = [1]
        numberOfClients.extend([x for x in range(10,110,10)])
         

        for numCli in numberOfClients: 
            if numCli!= 1:
                queueSizesText = ["T","B","R2","R"]
            else: 
                queueSizesText = ["B","R2","R"]
            queueSizesText = ["5B","10B"]
            for tp in throughputs:
                if numCli!= 1:
                    queueSizes = [tp*20/math.sqrt(numCli), tp*20,65535*4,65535*8] #in bits
                else:
                    queueSizes = [tp*20,65535*4,65535*8] #in bits
                queueSizes = [5*tp*20,10*tp*20]
                for queueSizeOriginal in queueSizes:
                    assuredSlice = []
                    ceilingSlice = []
                    assuredLeaf = []
                    ceilingLeaf = []
                    cfgNameNew = ""
                    print("TP is")
                    print(tp)
                    queueSize = queueSizeOriginal*numCli
                    print("Queue size pre-quanti is")
                    print(queueSize)
                    #account for quantization of MSS in the queueue
                    if (queueSize % (1499*8) !=0):
                        queueSize = math.ceil(queueSize/(1499 * 8))*1499*8 #MSS = 1499B
                    print("Queue size post-quanti is")
                    print(queueSize)
                    assuredSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',numCli*tp*1000),('HVIP', 0)]))
                    ceilingSlice.append(OrderedDict([('VIP', 0), ('LVD',0), ('VID',0), ('FDO',0), ('SSH',numCli*tp*1000),('HVIP', 0)]))
                    hostPrios = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0),('SSH', 0),('HVIP', 0)]) #all have the same priority
                    #set number of the leaves 
                    hostNumbers = OrderedDict([('VIP', 0), ('LVD', 0), ('VID', 0), ('FDO', 0), ('SSH', numCli),('HVIP', 0)])
                    rate = sum(assuredSlice[0].values())#in Mbps 
                    baseCfgName = 'liteCbaselineTestTokenQoS_base'  
                    
                    cfgNameNew = "n" + str(numCli) + "_q" + queueSizesText[queueSizes.index(queueSizeOriginal)] + "_tp" + str(multipliers[throughputs.index(tp)]) + cfgName
                    print(numCli) 
                    print(cfgNameNew)  
                    generate_all_config_files_ceil(cfgNameNew, baseCfgName, hostNumbers, hostPrios, hostIPs, serverIPs, assuredSlice,ceilingSlice,rate, queueSize,  useTwoLevelHTB)
      
        # Default.
    else:
        print('Config name %s not found - doing nothing.' % cfgName)
        return
    
    

    # # ini - vector of bwSplits
    # generate_ini(cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits)
    # generate_ini('%s' % cfgName, baseCfgName, hostNumbers, hostIPs, bwSplits, withoutHTB = True)
    # # routing.xml - skip types with number == 0?
    # generate_routing_xml(cfgName, hostNumbers, hostIPs, serverIPs)
    # # htb.xml (1 per bwSplit) - skip with number == 0
    # for bwSplit in bwSplits:
    #     longName = "%s_bw-%s" % (cfgName, "_".join(["%s_%02dk" % (k, round(v / 2)) for k, v in bwSplit.items()]))
    #     generate_htb_xml(longName, hostNumbers, hostPrios, bwSplit)


# cfgNames = [('myCfg-005', True), ('myCfg-006', False)]#, ('myCfg-005', True)]
# cfgNames = [('myCfg-007', True), ('myCfg-008', False)]
# cfgNames = [('cfg-voip-lvd-001', True), ('cfg-voip-lvd-002', False)]
# cfgNames = [('cfg-voip-vod-fdl-001', False)]
#cfgNames = [("Ddisaster2S", False),("DnoDisaster", False),("Ddisaster8S", False)]
#cfgNames = [("_gF_aVID", False),("_gS_aVID", False),("_gF_aLVD", False),("_gS_aLVD", False),("_gF_aFDO", False),("_gS_aFDO", False),("_gF_aVIP", False),("_gS_aVIP", False),("_gF_aSSH", False),("_gS_aSSH", False)]
#cfgNames = [("_gS_aVID", False),("_gS_aLVD", False),("_gS_aFDO", False),("_gS_aVIP", False),("_gS_aSSH", False)]
#cfgNames = [("_gF_aVID", False),("_gF_aLVD", False),("_gF_aFDO", False),("_gF_aVIP", False),("_gF_aSSH", False)]
#cfgNames = [("_gF_aSSH", False),("_gS_aSSH", False)]
#cfgNames = [("_gF_SSH", False),("_gS_aSSH", False)]


#cfgNames = [("_gF_aFDO", False),("_gS_aFDO", False),("_gF_aVIP", False),("_gS_aVIP", False)] #,("_gF_aLVD", False),("_gS_aLVD", False)
cfgNames = [("_gF_aFDO", False),("_gS_aFDO", False),("_gF_aVIP", False),("_gS_aVIP", False),("_gF_aLVD", False),("_gS_aLVD", False),("_gF_aVID", False),("_gS_aVID", False) ] #           

for cfgName in cfgNames:
    gen_cfg(cfgName[0], cfgName[1])

# TODO: add anarcho edition as well
# TODO: maybe also a flag for cleaning files with the same prefix (and potentially even sim results with the same prefix)