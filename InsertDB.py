#!/usr/bin/env python
import datetime
import MySQLdb
import operator, time, string
import sys
import os
import subprocess
import shlex
import calendar
import hashlib
import matplotlib.pyplot as plt
import matplotlib
from os import listdir
from os.path import isfile, join
from calendar import monthrange
from noise_bug_comments import RemoveNoise
from saveResults import *

myclass = RemoveNoise(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
db_out = sys.argv[6]
myclass.CreateDB(db_out) 
p = myclass.create_folders()
o = myclass.connect_extract(p)
myclass.clear_files()


year = sys.argv[1]
month = sys.argv[2]
id = sys.argv[3]
path = sys.argv[4]
db_name = sys.argv[5]


os.chdir(path)
subpath = "%s/%s/%s" % (id,year,month)
fpath = path + subpath
os.chdir(fpath)
list_path = os.listdir(fpath)
print list_path
    

onlyfiles = [ f for f in listdir(fpath) if isfile(join(fpath,f)) ]
num_files = len([ f for f in listdir(fpath) if isfile(join(fpath,f)) ])
         
                      
for k in range(num_files):
    file_size = os.path.getsize(onlyfiles[k])
    if file_size > 0 :
        pfile = os.path.abspath(onlyfiles[k])
        print "This is the file:" ,pfile
        phash = hashlib.md5(open('%s' %pfile).read()).hexdigest()
        print "This is the file hash: " ,phash
        print "This is the dub sentences hash:"  ,list(myclass.HashDuplicates(onlyfiles[k]))
       





dir_path = "/tmp/%s/" %id
print dir_path
d = os.path.dirname(dir_path)
if not os.path.exists(d):
        os.makedirs(d)
        

file_list = []
for i in range(12):
    
    cr_input_file = open("/tmp/%s/data%d.txt" %(id,i), "w")
    r = os.path.abspath("/tmp/%s/data%d.txt" %(id,i))
    file_list.append(r)


print file_list
final_path = path + "%s/%s/%s" %(id,year,month)
print final_path
os.chdir("/Users/ilias/Repos/sentistrength-serg-version/")
os.system("python saveResults.py %s %s/data%s.txt > %s/data%s.txt" %(final_path,dir_path,month,dir_path,month))
Names = []
for line in open('%s/data%s.txt' %(dir_path,month),'r').readlines():
    Names.append(line.strip())



print Names
x = [i.split() for i in Names]
x = [[int(j) for j in i] for i in x] #This works under GNU/Linux OS
o = list(enumerate(x))
print o

myclass.InsertIDs(db_out,id)


tmp_sub_list = []
for i in range(len(x)):
        tmp_sub_list = o[i][1]
        status = len(tmp_sub_list)
        dbc = MySQLdb.connect("localhost","root","root","%s" % (db_out))
        if (status > 0) :
                cursor = dbc.cursor() 
                pos_score = tmp_sub_list[0] 
                neg_score = tmp_sub_list[1]  
                neu_score = tmp_sub_list[2] 
                day = i + 1
                sub_on = "%s-%s-%s" % (year,month,day) #Example
                cursor.execute("INSERT INTO sentiment_score (sub_on,pos_score,neg_score,neu_score,parent_id) VALUES ('%s','%s','%s','%s','%s') ;" % (sub_on,pos_score,neg_score,neu_score,id))
                dbc.commit()
                print sub_on
                print "The day is :", day , "The positive score is:" , pos_score 
                print "The day is :", day , "The negative score is :",neg_score
                print "The day is :", day , "The neutral score is :",neu_score

dbc.close()


myclass.RemoveZeros(db_out)







