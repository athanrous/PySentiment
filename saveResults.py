import subprocess
import shlex
import datetime
import MySQLdb
import operator, time, string
import sys
import os
import calendar
import fileinput
from natsort import natsorted
from os import listdir
from os.path import isfile, join
from calendar import monthrange
from nltk.stem import WordNetLemmatizer

class GetSentiment:
        
    def SentimentText(self,sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
        p = subprocess.Popen(shlex.split("java -jar SentiStrength.jar stdin sentidata /Users/ilias/Repos/sentistrength-serg-version/SentiStrength/SentStrength_Data/ binary"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
        stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+"))
    #remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
        stdout_text = stdout_text.rstrip().replace("\t","")
        return stdout_text


class ScoreFiles:
    
    
    path = sys.argv[1]
    tmp = sys.argv[2]
    
    def __init__(self,path,tmp):
        
        self.path = path
        self.tmp = tmp
            
    def GetScore(self):
        
        
        file_out = open("%s" %self.tmp,'w')
        file_out.close() 
        rpath = self.path + '/'
        o = map(lambda f:rpath +f,os.listdir(rpath))
        new_sort = natsorted(o) # Sort directory files by numerical way
        for file in new_sort:
            
            file_size = os.path.getsize(file)
            if file.startswith(".DS_"):  #This is an auto generated file in Mac OS. More info see at http://en.wikipedia.org/wiki/.DS_Store 
                os.remove(kfile)
            
            
            with open(file) as f:
                     
                contents = f.read() #Read file contents
                new_contents = contents.replace('\n', '')
                kapa = GetSentiment()
                loi = kapa.SentimentText(new_contents)
                print loi
                               
        
  
    
        
if __name__ == '__main__':
    
    lpath = sys.argv[1]
    tmp = sys.argv[2]
    o = ScoreFiles(lpath,tmp)
    o.GetScore()
