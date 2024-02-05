#!/bin/bash
#bash localsetting.sh

#pip installed in ensurepip, check update each time before using
echo "Updating pip..."
python -m pip install --upgrade pip

#basic packages
python -m pip install numpy;#array
python -m pip install pandas;#dataframe
python -m pip install pyarrow;#parquet
python -m pip install -U matplotlib;#plot

#https://camelot-py.readthedocs.io/en/master/user/install.html#install
python -m pip install "camelot-py[base]";#read table from pdf
#https://nbviewer.org/github/chezou/tabula-py/blob/master/examples/tabula_example.ipynb
python -m pip install tabula-py;#read table from pdf
python -m pip install JPype1;#dependencies

python -m pip install chardet;#test encoding 

# for java, https://stackoverflow.com/questions/25074017/java-version-and-javac-version-showing-different-versions
# On Windows: Set env Variable name to JAVA_HOME and the Variable value to Java installation path (i.e., C:\Program Files\Java\jdk-21\bin).
# run .bash_profile: source ~/.bash_profile

java -version;#verify java version

gswin64c.exe -version;#verify Ghostscript version

