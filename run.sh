#!/bin/sh
echo "Instal required libs"
apt-get install python
apt-get install python-tk
apt-get install python-pygame
cd ./PyGraphics-2.1
python setup.py install --record file.txt
cd ../
cd ./ampy-1.2.3
python setup.py install --record file.txt
cd ../
cd ./Code
echo "Start program"
python treemap.py
