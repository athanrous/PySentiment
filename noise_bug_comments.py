#!/usr/bin/env python
import datetime
import MySQLdb
import operator, time, string
import sys
import os
import calendar
import fileinput
import matplotlib.pyplot as plt
import matplotlib
import nltk.data
import difflib
import hashlib
import itertools
from collections import defaultdict
from os import listdir
from os.path import isfile, join
from calendar import monthrange
  
#To mine the bugzilla data use Bicho https://github.com/MetricsGrimoire/Bicho
#This file is based on Noise.py tool for removing noise from mailing lists messages (by using MLStats). 
#More info about the tool (upon request) : https://bitbucket.org/ilias_r/serg-research-soft/src/8986633cc6ae/sentiment_analysis/

#Install nltk package by following the official installation instructions. More : http://nltk.org/install.html

#Install the packages difflib,hashlib

# In Gnu-Linux version replace gsed with sed
# For running the script you should install the following packages (tested in Mac 10.9.1) :  
# 1) Homebrew package manager (http://brew.sh/)
# 2) After installing Homebrew package manager open your terminal and type : 
#       i) brew doctor 
#       ii) echo export PATH='/usr/local/bin:$PATH' >> ~/.bash_profile
#       iii) brew install coreutils findutils gnu-tar gnu-sed gawk gnutls gnu-indent gnu-getopt


class RemoveNoise:
    
    year = sys.argv[1]
    month = sys.argv[2]
    id = sys.argv[3]
    path = sys.argv[4]
    db_name = sys.argv[5]

    
    def __init__(self,year,month,id,path,db_name):
        
        self.year = year
        self.month = month
        self.id = id
        self.path = path
        self.db_name = db_name 
        
        
    def connect_extract(self,extra_path):
            
        os.chdir(extra_path)
        year = int(self.year)
        month = int(self.month)
        rank = monthrange(year, month)
        l = rank[1]
        mylist = range(0,l)
    
        for i in range(len(mylist)):
            cr_input_file = open("data%d.txt" % i, "w")  
    
        mydaterange = range(1,l+1)
        date_list= []
    
        for p in mydaterange:
    
            date_test = datetime.date(year,month,p)
            date_list.append(date_test)
                
        db = MySQLdb.connect("localhost","root","root","%s" % (self.db_name)) 
        cursor = db.cursor()
        
        for date in date_list:
            date_pos = date_list.index(date)        
            cursor.execute("SELECT cm.text FROM comments cm WHERE DATE(cm.submitted_on)='%s' AND cm.submitted_by='%s';" % (date_list[date_pos],self.id) ) # nikos: ekana ta tria dyo!!! dld ekana triple quotes, double quotes
            output = cursor.fetchall() 
            
            data = ""
    
            for record in output:
                for entry in record:
                        input_file = open("data%d.txt" % date_pos, "w")
                        data = data + "\n" + str(entry)
                        data= data + "\n"
                        
                        input_file.writelines(data)
                input_file.close()
        db.close()
        
        
    def create_folders(self):
        
        os.chdir(self.path)
        subpath = '%s/%s/%s' % (self.id,self.year,self.month)
    
        if not os.path.exists(subpath):
        
    
            os.makedirs(subpath)
            finalpath = self.path + subpath
            os.chdir(finalpath)
            k_path = os.getcwd()
            return k_path;
        else :
            final_path = self.path + subpath
            os.chdir(final_path)
            l_path = os.getcwd()
            return l_path
            
            
    def clear_files(self):
    
        os.chdir(self.path)
        subpath = "%s/%s/%s" % (self.id,self.year,self.month)
        fpath = self.path + subpath
        os.chdir(fpath)
        list_path = os.listdir(fpath)
        tmp_file_name = open("/tmp/foo.txt","w")
        tmp_file_name.close()
        tmp_path = "/tmp/foo.txt"
        
        onlyfiles = [ f for f in listdir(fpath) if isfile(join(fpath,f)) ]
        num_files = len([ f for f in listdir(fpath) if isfile(join(fpath,f)) ])
         
                      
        for k in range(num_files):
        
            file_size = os.path.getsize(onlyfiles[k])
            
            
            if file_size > 0 : # Finds the file with size greater than 0
                cmd_01 = "gsed -f /Users/ilias/Repos/sentistrength-serg-version/scripts.sed '%s' > '%s'" % (onlyfiles[k],tmp_path)         
                cmd_02 = "mv %s %s" % (tmp_path,onlyfiles[k])
                os.system(cmd_01)
                os.system(cmd_02)
 
        
        
     
    def CreateDB(self,db):
               
        dbc = MySQLdb.connect("localhost","root","root") 
        cursor = dbc.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS %s " %(db))
        cursor.execute("USE %s " %(db))
        cursor.execute("CREATE TABLE IF NOT EXISTS developer ( id INT NOT NULL,PRIMARY KEY (id) ) ENGINE=INNODB;")
        cursor.execute("CREATE TABLE IF NOT EXISTS sentiment_score (sub_on date NOT NULL,pos_score int(11) NOT NULL,neg_score int(11) NOT NULL,neu_score int(11) NOT NULL,parent_id INT, INDEX par_ind (parent_id),FOREIGN KEY (parent_id) REFERENCES developer(id) ON DELETE CASCADE ) ENGINE=INNODB;")
        dbc.commit()
        cursor.close()
        
        
    def PlotDB(self,db_aux,id_aux):
        
        #Add folder for plot extraction    
        
        con = MySQLdb.connect('localhost', 'root', 'root', '%s' %(db_aux))
        cursor = con.cursor()
    
        query_dates = "select sub_on from sentiment_score where parent_id = '%s'" %(id_aux)
        cursor.execute(query_dates)
        dates = [item[0] for item in cursor.fetchall()]


        query_pos ="select pos_score from sentiment_score where parent_id = '%s'" %(id_aux)
        cursor.execute(query_pos)
        pos_score = [item[0] for item in cursor.fetchall()]

        query_neg ="select neg_score from sentiment_score where parent_id = '%s'" %(id_aux)
        cursor.execute(query_neg)
        neg_score = [item[0] for item in cursor.fetchall()]


        query_neu ="select neu_score from sentiment_score where parent_id = '%s'" %(id_aux)
        cursor.execute(query_neu)
        neu_score = [item[0] for item in cursor.fetchall()]
        
        
        query_act_dates = "select changed_on FROM actic where changed_by='6';"
        cursor.execute(query_act_dates)
        act_dates = [item[0] for item in cursor.fetchall()]
        
        query_act = "SELECT count(cm.id) as cmt, cm.changed_on FROM activ cm WHERE cm.changed_by = '6' and year(cm.changed_on)>='2011' and month(cm.changed_on) >='01' and day(cm.changed_on) >= '01' GROUP BY year(cm.changed_on), month(cm.changed_on), day(cm.changed_on) ORDER BY cm.changed_on desc;"
        cursor.execute(query_act)
        act = [item[0] for item in cursor.fetchall()]
        
        plt.plot_date(dates, pos_score, linestyle='-', xdate=True, ydate=False,color='g')
        plt.plot_date(dates, neg_score, linestyle='-', xdate=True, ydate=False,color='r')
        plt.plot_date(dates, neu_score, linestyle='-', xdate=True, ydate=False,color='b')
        plt.plot_date(act_dates, act, linestyle='-', xdate=True, ydate=False,color='y')
        
        return plt.show() 

    def RemoveZeros(self,db_aux):
        
        
        db = MySQLdb.connect("localhost","root","root","%s" % (db_aux))
        cursor = db.cursor()
        cursor.execute("USE %s " %(db_aux))    
        cursor.execute("DELETE FROM developer WHERE id NOT IN (SELECT parent_id FROM sentiment_score);")
        db.commit()
        db.close()
        
        
    def InsertIDs(self,db_aux,id_aux):
        
        db = MySQLdb.connect("localhost","root","root","%s" % (db_aux))
        cursor = db.cursor()
        results = cursor.execute("""SELECT id from developer where developer.id = '%s';""" % (id_aux))
        if not results:
            print "This table is empty!"
            cursor.execute("INSERT INTO developer (id) VALUES ('%s');" % (id_aux))
            db.commit()

        db.close()
       

    def HashDuplicates(self,file_in):
        '''
        This function removes all the duplicated sentences inside a text file by using hashing of the sentences and Set theory.
        '''
        
        tmp = open("/tmp/da.txt","w")
        tmp.close()
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        os.system("cat %s | LC_CTYPE=C tr -d '\n' > /tmp/da.txt " %file_in) 
        file_rt_k = open("/tmp/da.txt").read()                    
        k = sent_detector.tokenize(file_rt_k.strip())
        p = list(set(k))
        hash_code = []
        leng = []
        for w in range(len(k)):    
            hash_code.append(hashlib.md5(k[w]).hexdigest())
            leng.append(len(k[w]))


        print hash_code
        C = defaultdict(list)
        for i,item in enumerate(hash_code):
    
            C[item].append(i)
        C = {k:v for k,v in C.items() if len(v)>1}
        hashes = C.values()
        dub_hash = [x for h in hashes for x in h]
        D = defaultdict(list)
        for i,item in enumerate(leng):
            D[item].append(i)
        D = {k:v for k,v in D.items() if len(v)>1}
        lens = D.values()
        dub_lens = [x for h in lens for x in h]
        uni = list(set(dub_hash) & set(dub_lens))   
        dub_list = []
        for i in uni:
            while i < len(k) - 1:
    
                del k[i]
                dub_list.append(k[i])
                
        fin = list(set(k) - set(dub_list))
        fin_union = list(set(fin) | set(dub_list))
        fin_str = ''.join(fin_union)
        file_rt_k = open("/tmp/da.txt").close()    
        f = open("/tmp/hash.txt" ,"w")
        f.write(fin_str) 
        f.close()
        cmd = "mv /tmp/hash.txt %s" %file_in 
        os.system(cmd)
 
        return dub_list
    
    
    
    def GetCommitAct(self,db_aux,id_aux,email_aux):
        
        db = MySQLdb.connect("localhost","root","root","%s" % (db_aux))
        cursor = db.cursor()
        results = cursor.execute("""SELECT id from developer where developer.id = '%s';""" % (id_aux))
        if not results:
            print "This table" +db_aux+ " is empty!"
            
            
        else :
          commits = cursor.execute("""SELECT count(s.id) from scmlog s,people p where s.committer_id=p.id and p.email= %s';""" % (email_aux))
          print "The table" +db_aux+ "has this number of commits :" + commits
        db.close()
        
    
    
    
   
        
        
        
        
       

        
        
        
        
        
            
        
