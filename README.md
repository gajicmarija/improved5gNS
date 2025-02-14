# improved5gNS
# Analysis of QoE-Aware Slice Configuration on Application Quality in Beyond 5G Networks
This git-repository is a code and data-set base corresponding to the paper titled Analysis of QoE-Aware Slice Configuration on Application Quality in Beyond 5G Networks, submitted for IEEE Transactions on Network and Service Management.

# Requirements: 
For installation, the following software environment is needed: 
- OMNeT++ version 6.0.0 or 6.1.0
- INET Framework version 4.4.0
- Python, version 3.7 (could potentially be compatible with other versions as well)

# Code base:
- File simulations/parameterStudyConfiguration.ini contains the configuration files for all simulations in OMNeT++. To generate configurations automaticaly, a script /algorithm/genConfImproved.py was used.
- To run a simulation successfully, files in simulations/config/htbTree and simulations/config/routing are needed for each configuration. 
- Bash script called simulations/runAndExportParameterStudy.sh runs the simulations and uses opp-scavetool to export the selcted data as .csv files.
- File simulations/runAllConfigurations.txt van be used for parallel running of the simulations, e.g. parallel --jobs 10 < runAllConfigurations.txt and shows syntax for how each configuration can be ran via terminal. 
- Python script analysis/code/plotFinalFigures.py is used to create plots from the exported data.

# Data-set:
- The outcomes can be found under analysis/exports/extracted/mos2, called data*.csv contaning both QoE and System Utilization outcome for each scenario evaluated.
- In the csv file, the following notation is used:
  - n = Number of clients,
  - q = Queue size(B= BDP, T = Tiny Buffers, R = Rcwnd),
  - tp = Link capacity [% of the Tp_reference],
  - g = Granularity of the resource allocation scheme (0 = per Flow, 1 = per Slice),
  - a = Application type (VID = Video-on-Demand, LVD = Live video, VIP = VoIP, FDO = File Download)
  - MOS = Mean Opinion Score, and
  - SU = System Utilization



