# improved5gNS

This git-repository is a code base corresponding to the paper titled QoE-Aware Resource Allocation in Beyond 5G networks.

# Requirements: 
For installation, the following software environment is needed: 
- OMNeT++ version 6.0.0 or 6.1.0
- INET Framework version 4.4.0
- Python, version 3.7 (could potentially be compatible with other versions as well)

# Code base:
- File simulation/parameterStudyConfiguration.ini contains the configuration files for all simulations in OMNeT++.
- To run a simulation successfully, files in simulation/config/htbTree and simulation/config/routing are needed for each configuration. 
- Bash script called runAndExportParameterStudy.sh runs the simulations and uses opp-scavetool to export the selcted data as .csv files.
- File runAllConfigurations.txt van be used for parallel running of the simulations, e.g. parallel --jobs 10 < runAllConfigurations.txt and shows syntax for how each configuration can be ran via terminal. 
- File dataComplete.csv is the summarized output file with results of the evaluations, including MOS and System Utilization
- Python script plotResults.py is used to create plots from the exported data.



