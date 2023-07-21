from pathlib import Path


#define static configuration text for each application
configCommon ="network = baselineTestV3 \n"
configCommon +="output-vector-file = \"${resultdir}/${configname}/${configname}-${runnumber}.vec\"\n"
configCommon +="output-scalar-file = \"${resultdir}/${configname}/${configname}-${runnumber}.sca\"\n\n"
configCommon +="**.crcMode = \"computed\" \n\n"
configCommon += "**.dataCapacity = ${q=$TP*40}b \n\n"

#SSH
configSSH = "*.nVID = 0 # Number of video clients \n"
configSSH += "*.nLVD = 0 # Number of live video clients \n"
configSSH += "*.nFDO = 0 # Number of file download clients \n"
configSSH += "*.nVIP = 0 # Number of VoIP clients\n"
configSSH += "*.nHVIP = 0 # Number of haptic VoIP clients\n\n"
configSSH += "# Remote Shell Client\n"
configSSH += "**.hostSSH[*].numApps = 1\n"
configSSH += "**.hostSSH[*].app[0].typename = \"TcpSimpleSshAppV2lite\"\n"
configSSH += "**.hostSSH[*].app[0].localAddress = \"\" # local address or empty (\"\") \n"
configSSH += "**.hostSSH[*].app[0].localPort = -1 # local port number \n"
configSSH += "**.hostSSH[*].app[0].connectAddress = \"serverSSH\" # server address (may be symbolic)\n"
configSSH += "**.hostSSH[*].app[0].connectPort = 22  # port number to connect to \n"
configSSH += "**.hostSSH[*].app[0].startTime = 0.01s # time first session begins \n"
configSSH += "**.hostSSH[*].app[0].stopTime = 100s # time of finishing sending, negative values mean forever \n"
configSSH += "**.hostSSH[*].app[0].numCommands = 1 # user types this many commands in a session \n"
configSSH += "**.hostSSH[*].app[0].commandLength = 10B # commands are this many characters (plus Enter) \n"
configSSH += "**.hostSSH[*].app[0].keyPressDelay = 0.05s # delay between keypresses \n"
configSSH += "**.hostSSH[*].app[0].commandOutputLength = 500B # commands produce this much output \n"
configSSH += "**.hostSSH[*].app[0].thinkTime = 1s # user waits this much before starting to type new command\n"
configSSH += "**.hostSSH[*].app[0].idleInterval = 100s # time gap between sessions \n"
configSSH += "**.hostSSH[*].app[0].reconnectInterval = 1s # if connection breaks, user waits this much before trying to reconnect \n"
configSSH += "**.hostSSH[*].app[0].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"
configSSH += "**.hostSSH[*].app[0].stopOperationTimeout = 2s # timeout value for lifecycle stop operation \n\n"
configSSH += "# SSH server \n"
configSSH += "*.serverSSH.numApps = 1 \n"
configSSH += "*.serverSSH.app[*].typename = \"TcpGenericServerApp\"\n"
configSSH += "*.serverSSH.app[*].localAddress = \"\" # local address; may be left empty (\"\") \n"
configSSH += "*.serverSSH.app[*].localPort = 22 # localPort number to listen on \n"
configSSH += "*.serverSSH.app[*].replyDelay = 0s \n"
configSSH += "*.serverSSH.app[*].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"
configSSH += "*.serverSSH.app[*].stopOperationTimeout  = 2s # timeout value for lifecycle stop operation \n"

#VoD
configVID = "*.nSSH = 0 # Number of SSH clients \n"
configVID += "*.nLVD = 0 # Number of live video clients \n"
configVID += "*.nFDO = 0 # Number of file download clients \n"
configVID += "*.nVIP = 0 # Number of VoIP clients\n"
configVID += "*.nHVIP = 0 # Number of haptic VoIP clients\n\n"
configVID += "**.hostVID[*].numApps = 1 \n"
configVID +="# Video client \n"
configVID +="**.hostVID[*].app[0].typename = \"TCPVideoStreamCliAppV2lite\"\n"
configVID +="**.hostVID[*].app[0].localAddress = \"\" # may be left empty (\"\") \n"
configVID +="**.hostVID[*].app[0].localPort = -1 # port number to listen on \n"
configVID +="**.hostVID[*].app[0].connectAddress = \"serverVID\" # server address (may be symbolic) \n"
configVID +="**.hostVID[*].app[0].connectPort = 1042 # port number to connect to \n"
configVID +="**.hostVID[*].app[0].dataTransferMode = \"object\" \n"
configVID +="**.hostVID[*].app[0].startTime = 0.01s # time first session begins \n"
configVID +="**.hostVID[*].app[0].stopTime = -1s # time of finish sending, 0 means infinity \n"
configVID +="**.hostVID[*].app[0].idleInterval = 1000s\n"
configVID +="**.hostVID[*].app[0].requestLength = 200B # length of a request \n"
configVID +="**.hostVID[*].app[0].reconnectInterval = 1s # if connection breaks, waits this much before trying to reconnect \n"
configVID +="**.hostVID[*].app[0].numRequestsPerSession = 1 # number of requests sent per session \n"
configVID +="**.hostVID[*].app[0].thinkTime = 1000s # time gap between requests \n"
configVID +="**.hostVID[*].app[0].video_resolution = \"360 480 720 1080\" \n"
configVID +="**.hostVID[*].app[0].manifest_size = 100000 \n"
configVID +="**.hostVID[*].app[0].video_buffer_max_length = 40s # buffer max length in seconds \n"
configVID +="**.hostVID[*].app[0].video_duration = 300s # video length in seconds\n"
configVID +="**.hostVID[*].app[0].segment_length = 5s # video segment length in seconds\n"
configVID +="**.hostVID[*].app[0].useFlexibleBitrate = \"flexible\" \n\n"
configVID +="# Video server \n"
configVID +="*.serverVID.numApps = 1\n" 
configVID +="*.serverVID.app[0].typename = \"TcpGenericServerApp\" \n"
configVID +="*.serverVID.app[0].localAddress = \"\" # local address; may be left empty (\"\") \n"
configVID +="*.serverVID.app[0].localPort = 1042 # localPort number to listen on \n"
configVID +="*.serverVID.app[0].replyDelay = 0s # \n"
configVID +="*.serverVID.app[0].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"

#LVD
configLVD = "*.nSSH = 0 # Number of SSH clients \n"
configLVD += "*.nFDO = 0 # Number of file download clients \n"
configLVD += "*.nVIP = 0 # Number of VoIP clients\n"
configLVD += "*.nHVIP = 0 # Number of haptic VoIP clients\n"
configLVD += "*.nVID = 0 # Number of video clients \n\n"
configLVD += "**.hostLVD[*].numApps = 1 \n"
configLVD +="#Live video client \n"
configLVD +="**.hostLVD[*].app[0].typename = \"TCPLiveVideoStreamCliAppLite\" \n"
configLVD +="**.hostLVD[*].app[0].localAddress = \"\" # may be left empty (\"\") \n"
configLVD +="**.hostLVD[*].app[0].localPort = -1 # port number to listen on \n"
configLVD +="**.hostLVD[*].app[0].connectAddress = \"serverVID\" # server address (may be symbolic) \n"
configLVD +="**.hostLVD[*].app[0].connectPort = 1042 # port number to connect to \n"
configLVD +="**.hostLVD[*].app[0].dataTransferMode = \"object\" \n"
configLVD +="**.hostLVD[*].app[0].startTime = 0.01s # time first session begins \n"
configLVD +="**.hostLVD[*].app[0].stopTime = -1s # time of finish sending, 0 means infinity \n"
configLVD +="**.hostLVD[*].app[0].idleInterval = 1000s \n"
configLVD +="**.hostLVD[*].app[0].requestLength = 200B # length of a request \n"
configLVD +="**.hostLVD[*].app[0].reconnectInterval = 1s # if connection breaks, waits this much before trying to reconnect \n"
configLVD +="**.hostLVD[*].app[0].numRequestsPerSession = 1 # number of requests sent per session \n"
configLVD +="**.hostLVD[*].app[0].thinkTime = 1000s # time gap between requests \n"
configLVD +="**.hostLVD[*].app[0].video_resolution = \"240 360 480 720 1080\" # how many kbits are required for 1 second of video for each representation (quality levels) \n"
configLVD +="**.hostLVD[*].app[0].manifest_size = 100000 \n"
configLVD +="**.hostLVD[*].app[0].video_buffer_max_length = 6s # buffer max length in seconds \n"
configLVD +="**.hostLVD[*].app[0].video_duration = 70s # video length in seconds \n"
configLVD += "**.hostLVD[*].app[0].useFlexibleBitrate = \"flexible\" \n"
configLVD += "**.hostLVD[*].app[0].video_type = \"live\" \n"
configLVD += "**.hostLVD[*].app[0].delay_threshold = 4 \n"
configLVD += "**.hostLVD[*].app[0].speedup_rate = 1.05 \n\n"
configLVD += "# Video server \n"
configLVD += "*.serverLVD.numApps = 1 \n"
configLVD += "*.serverLVD.app[0].typename = \"TcpGenericServerApp\" \n"
configLVD += "*.serverLVD.app[0].localAddress = \"\" # local address; may be left empty (\"\")\n"
configLVD += "*.serverLVD.app[0].localPort = 1042 # localPort number to listen on\n"
configLVD += "*.serverLVD.app[0].replyDelay = 0s # \n"
configLVD += "*.serverLVD.app[0].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"
configLVD += "*.serverLVD.app[0].stopOperationTimeout  = 2s # timeout value for lifecycle stop operation \n"

#FD
configFD = "*.nSSH = 0 # Number of SSH clients \n"
configFD += "*.nLVD = 0 # Number of live video clients \n"
configFD += "*.nVID = 0 # Number of video clients \n"
configFD += "*.nVIP = 0 # Number of VoIP clients\n"
configFD += "*.nHVIP = 0 # Number of haptic VoIP clients\n\n"
configFD += "**.hostFDO[*].numApps = 1 \n"
configFD += "# File download client \n"
configFD += "*.hostFDO[*].app[0].typename = \"TcpFileDownloadApp\" \n"
configFD += "*.hostFDO[*].app[0].localAddress = \"\" \n"
configFD += "*.hostFDO[*].app[0].localPort = -1 # port number to listen on \n"
configFD += "*.hostFDO[*].app[0].connectAddress = \"serverFDO\" # server address (may be symbolic) \n"
configFD += "*.hostFDO[*].app[0].connectPort = 1042 # port number to connect to \n"
configFD += "*.hostFDO[*].app[0].startTime = 0.01s # time first session begins \n"
configFD += "*.hostFDO[*].app[0].stopTime = -1s # time of finishing sending, negative values mean forever \n"
configFD += "*.hostFDO[*].app[0].numRequestsPerSession = 1 # number of requests sent per session \n"
configFD += "*.hostFDO[*].app[0].requestLength = 800B # length of a request \n"
configFD += "*.hostFDO[*].app[0].replyLength = 10000KiB # length of a reply \n"
configFD += "*.hostFDO[*].app[0].thinkTime = 0.01s # time gap between requests \n"
configFD += "*.hostFDO[*].app[0].idleInterval = 1000s # time gap between sessions \n"
configFD += "*.hostFDO[*].app[0].reconnectInterval = 1s # if connection breaks, waits this much before trying to reconnect \n"
configFD += "*.hostFDO[*].app[0].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"
configFD += "*.hostFDO[*].app[0].stopOperationTimeout = 2s # timeout value for lifecycle stop operation \n\n"
configFD += "# File download server \n"
configFD += "*.serverFDO.numApps = 1 \n"
configFD += "*.serverFDO.app[0].typename = \"TcpGenericServerApp\" \n"
configFD += "*.serverFDO.app[0].localAddress = \"\" # local address; may be left empty (\"\") \n"
configFD += "*.serverFDO.app[0].localPort = 1042 # localPort number to listen on \n"
configFD += "*.serverFDO.app[0].replyDelay = 0s # \n"
configFD += "*.serverFDO.app[0].stopOperationExtraTime = -1s # extra time after lifecycle stop operation finished \n"
configFD += "*.serverFDO.app[0].stopOperationTimeout  = 2s # timeout value for lifecycle stop operation \n"

#VIP
configVIP = "*.nSSH = 0 # Number of SSH clients \n"
configVIP += "*.nLVD = 0 # Number of live video clients \n"
configVIP += "*.nVID = 0 # Number of video clients \n"
configVIP += "*.nFDO = 0 # Number of VoIP clients\n"
configVIP += "*.nHVIP = 0 # Number of haptic VoIP clients\n\n"
configVIP += "# VoIP receiver \n"
configVIP += "**.hostVIP[*].numApps = 1 \n"
configVIP += "**.hostVIP[*].app[0].typename = \"SimpleVoipReceiver\" \n"
configVIP += "**.hostVIP[*].app[0].localPort = 2000 \n"
configVIP += "**.hostVIP[*].app[0].emodelIe = 5 # Equipment impairment factor \n"
configVIP += "**.hostVIP[*].app[0].emodelBpl = 10 # Packet-loss robustness factor \n"
configVIP += "**.hostVIP[*].app[0].emodelA = 5 # Advantage factor \n"
configVIP += "**.hostVIP[*].app[0].emodelRo = 93.2 # Basic signal-to-noise ratio \n"
configVIP += "**.hostVIP[*].app[0].playoutDelay = 200ms # initial delay for beginning playout after receiving the first packet \n"
configVIP += "**.hostVIP[*].app[0].adaptivePlayoutDelay = false # if true, adjust playoutDelay after each talkspurt \n"
configVIP += "**.hostVIP[*].app[0].bufferSpace = 20 # buffer size in packets \n"
configVIP += "**.hostVIP[*].app[0].mosSpareTime = 1s # spare time before calculating MOS (after calculated playout time of last packet) \n\n"
configVIP += "# VoIP sender \n"
configVIP += "**.serverVIP.numApps = parent.nVIP \n"
configVIP += "**.serverVIP.app[*].typename = \"SimpleVoipSender\" \n"
configVIP += "**.serverVIP.app[*].localPort = -1 \n"
configVIP += "**.serverVIP.app[*].destPort = 2000 \n"
configVIP += "**.serverVIP.app[*].destAddress = \"hostVIP[\" + string(index) + \"]\" \n"
configVIP += "**.serverVIP.app[*].talkPacketSize = 40B # size of talk packets in bytes \n"
configVIP += "**.serverVIP.app[*].talkspurtDuration = weibull(1.423s, 0.824s) \n"
configVIP += "**.serverVIP.app[*].silenceDuration = weibull(0.899s, 1.089s) \n"
configVIP += "**.serverVIP.app[*].packetizationInterval = 20ms # interval between sending voice packets \n"
configVIP += "**.serverVIP.app[*].startTime = 0.01s \n"
configVIP += "**.serverVIP.app[*].stopTime = -1s # time of end of sending, -1 means forever \n"




def addConfig(clientType, numberOfClients):
    
    if clientType == "SSH":
        configText = "[Config heatMapTestSSH_scale%i]\n" %numberOfClients 
        configText += configCommon
        configText += "sim-time-limit=400s \n\n"
        configText += "*.nSSH = %i # Number of SSH clients \n"  %numberOfClients
        configText += configSSH
        configText += "*.server*.numApps = 0 \n"
        configText +="*.host*.numApps = 0 \n \n"
        configText +="**.conn1.datarate = ${TP=" + str(5*numberOfClients) + ".." + str(10*numberOfClients) +  " step " + str(1*numberOfClients) + "}kbps \n"
        configText +="**.conn1.delay = ${del=20}ms \n\n"
    if clientType == "VID":
        configText = "[Config heatMapTestVID_scale%i]\n" %numberOfClients 
        configText += configCommon
        configText += "sim-time-limit=800s \n\n"
        configText += "*.nVID = %i # Number of video clients \n"  %numberOfClients
        configText += configVID
        configText += "*.server*.numApps = 0 \n"
        configText +="*.host*.numApps = 0 \n \n"
        configText +="**.conn1.datarate = ${TP=" + str(100*numberOfClients) + ".." + str(1500*numberOfClients) +  " step " + str(20*numberOfClients) + "}kbps \n"
        configText +="**.conn1.delay = ${del=20}ms \n\n"
    if clientType == "FDO":
        configText = "[Config heatMapTestFDO_scale%i]\n" %numberOfClients 
        configText += configCommon
        configText += "sim-time-limit=400s \n\n"
        configText += "*.nFDO = %i # Number of video clients \n"  %numberOfClients
        configText += configFD
        configText += "*.server*.numApps = 0 \n"
        configText +="*.host*.numApps = 0 \n \n"
        configText +="**.conn1.datarate = ${TP=" + str(100*numberOfClients) + ".." + str(2800*numberOfClients) +  " step " + str(20*numberOfClients) + "}kbps \n"
        configText +="**.conn1.delay = ${del=20}ms \n\n"
    if clientType == "LVD":
        configText = "[Config heatMapTestLVD_scale%i]\n" %numberOfClients 
        configText += configCommon
        configText += "sim-time-limit=400s \n\n"
        configText += "*.nLVD = %i # Number of video clients \n"  %numberOfClients
        configText += configLVD
        configText += "*.server*.numApps = 0 \n"
        configText +="*.host*.numApps = 0 \n \n"
        configText +="**.conn1.datarate = ${TP=" + str(100*numberOfClients) + ".." + str(1900*numberOfClients) +  " step " + str(20*numberOfClients) + "}kbps \n"
        configText +="**.conn1.delay = ${del=20}ms \n\n"
    if clientType == "VIP":
        configText = "[Config heatMapTestVIP_scale%i]\n" %numberOfClients 
        configText += configCommon
        configText += "sim-time-limit=80s \n\n"
        configText += "*.nVIP = %i # Number of SSH clients \n"  %numberOfClients
        configText += configVIP
        configText += "*.server*.numApps = 0 \n"
        configText +="*.host*.numApps = 0 \n \n"
        configText +="**.conn1.datarate = ${TP=" + str(5*numberOfClients) + ".." + str(30*numberOfClients) +  " step " + str(1*numberOfClients) + "}kbps \n"
        configText +="**.conn1.delay = ${del=20}ms \n\n"


    print(configText)

    myfile= open("/Users/marijagajic/omnetpp-6.0/improved5gNS/simulations/omnetpp.ini", "a")
    myfile.write(configText)
    myfile.close()

applications = ["SSH","VID","FDO","LVD","VIP"]
numberOfClients = [1, 5, 10, 50, 100, 200]

for app in applications: 
    for numCli in numberOfClients:
        myfile= open("/Users/marijagajic/omnetpp-6.0/improved5gNS/simulations/runScalabilityStudies.txt", "a")
        myfile.write("./runAndExportHeatMaps.sh -i omnetpp.ini -c heatMapTest"+ app + "_scale" + str(numCli) + " -s 1 -n 60 \n")
        myfile.close()
        addConfig(app,numCli)