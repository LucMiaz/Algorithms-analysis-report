import sys
import os, pathlib
import numpy as np
import itertools
from kg.detect import MicSignal
from kg.algorithm import *
from kg.algorithm import Case
from kg.widgets import *
from kg.measurement_values import measuredValues, read_MBBM_tables
from kg.measurement_signal import measuredSignal
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#get case from .mat file
def case_to_analyse(ID, mic, matPath,table, givenauthor=None):
    """setup the analysed cases from MBBM
    called by load_cases
    """
    # read the signal
    caseDict={}
    mesPath=matPath.parent.parent
    # initiate  MicSignal
    micSn,micval = load_micSn(ID,mic,matPath)
    # test if signal is clipped, skipü it if True
    if micSn.clippedtest():
        clipped.add((ID,mic))
        print('clipped')
    # create Wav and add path to caseDict
    caseDict['wavPath'] = str(micSn.export_to_Wav(mesPath, relative=False))
    # initialize empty Case with None author
    caseDict['case']=Case(micval['location'], micval['measurement'],ID, mic,micval['micValues']['Tb'], micval['micValues']['Te'], givenauthor)
    #add tmin tmax
    caseDict['tmin'] = float(micval['t'].min())
    caseDict['tmax'] = float(micval['t'].max())
    caseDict['micSn']=micSn
    # Add data to plot ; key:[t,y] , #key is label of plot
    caseDict['plotData'] = {}
    caseDict['micSn']=micSn
    caseDict['micval']
    # first plot prms
    micval['y'],micval['t'],_ = micval['mS'].get_signal('prms' + str(mic))
    caseDict['plotData']['LAfast']=[micval['t'].tolist(),(20*np.log10(micval['y']/(2e-5))).tolist()]
    # second plot prms
    # todo: plot stft band
    # append Case Dict to  dict
    table.insert(caseDict)
# connecting to a SQLite database
Paths=[]
Paths.append(pathlib.Path('E:/ZugVormessung'))
Paths.append(pathlib.Path('E:/Biel1Vormessung'))
# Insert a new record.

db_engine = create_engine('algdb.db', echo=True)
Base=declarative_base(bind=db_engine)
class SQLInterval(Base):
    xmin=Column(Float)
    xmax=Column(Float)
class SQLSetOfIntervals(Base):
    id=Column(String)
    
class SQLMicSignal
    
class SQLCases(Base):
    id=Column(Integer)
    
class SQLAuthors(Base):
    __tablename__='authors'
    id = Column(String, primary_key=True)
    name=Column(String)
    first_name=Column(String)
    AC_id=Column(Integer)#analysed cases ID
Base.metadata.create_all()
Session=sessionmaker(bind=db_engine)
s=Session()
counter=0
for path in Paths:
    for file in path.joinpath('raw_signals').iterdir():
        if file.match('**.mat'):
            counter+=1
            filename=file.name
            stripped=file.strip('_')
            mic=stripped[-1]
            ID='m_'+stripped[-2]
            case_to_analyse(ID,mic,file,table)
        if counter>10:
            break
    if counter>10:
        break
            
