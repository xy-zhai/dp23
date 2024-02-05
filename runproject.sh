#!/bin/bash

#install r packages
#Rscript /home/xzhai/dataproc2023/myproject/installrpkg.R

#run the project
echo "start reading data ..."
python3 /home/xzhai/dataproc2023/myproject/readdata.py
echo "data cleaning is done, new data is saved in /home/xzhai/dataproc2023/myproject"

echo "start plotting ..."
python3 /home/xzhai/dataproc2023/myproject/plot.py
echo "plotting is done, figure1 2 3 are saved in /home/xzhai/dataproc2023/myproject"

echo "start mapping ..."
Rscript /home/xzhai/dataproc2023/myproject/map.R
echo "mapping is done, figure4 is saved in /home/xzhai/dataproc2023/myproject"

echo "ALL FINISHED!"