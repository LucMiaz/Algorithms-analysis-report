import sys
import os,pathlib
import itertools
import json
import math

def extract_for_R(filespath,listofspec=['BPR'],outputname='Datamaous'):
    """constructs a list of elements for use in R"""
    ## insert folder path
    if not isinstance(filespath,pathlib.Path):
        filespath=pathlib.Path(filespath)
    parentfilepath=filespath.parent
    
    ## insert possible algorithm specific values (like BPR for Z2)
    listofspec=['BPR']#insert
    #import of the following values
    datamaous=[]
    keys=['mic', 'mID', 'location', 'author','quality', 'time', 'disc', 'NoiseT', 'Alg', 'AlgProp']
    
    qualitydict={'good':3,'medium':2,'bad':1,'NA':0}
    
    for file in filespath.iterdir():
        if file.match("**.json"):#checks if file is a json
            with filespath.joinpath(file).open("r+") as istream:#opens file
                dictio=json.load(istream)#loads json file
            Rdata=dictio['R']#takes the dedicated dictionnary for R
            for datum in Rdata:#iterates over input data
                ckey=None
                for sp in listofspec:
                    if sp in datum.keys():
                        ckey=sp
                        break
                if not ckey:
                    break
                else:
                    if not math.isnan(float(datum.get(ckey,'NaN'))):
                        row={}
                        row['spec']=datum[ckey]
                        for key in keys:
                            if key=='quality':
                                row[key]=qualitydict[datum[key]]
                            else:
                                row[key]=datum[key]
                        datamaous.append(row)
    try:
        os.remove(parentfilepath.joinpath(str(outputname)+'.json'))
    except:
        pass
    with parentfilepath.joinpath(str(outputname)+'.json').open("w+") as ostream:
        json.dump(datamaous,ostream)
if __name__=="__main__":
    extract_for_R("C:/lucmiaz/Algorithm_Report/results")