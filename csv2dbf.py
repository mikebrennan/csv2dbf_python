#!/usr/bin/env python
# encoding: utf-8
"""
csv2dbf.py

this script coverts CSV files to DBF
requirements:
    Header.csv - this contains the DBF definition (required names ==> FIELDNAME,TYPE,LENGTH)
                 1 FIELDNAME,TYPE,LENGTH
                 2 STAFF,N,10
                 3 STAFF_NAME,C,101
                 4 DATEIN,D,
                 5

    Body.csv   - this contians your db info based on you header FIELDNAME definitions
                 1 STAFF,STAFF_NAME,DATEIN
                 2 1234,joe smith,20130925
                 3 1235,jill smith,20130925
                 4

    dbfpy directory - This contains the library for dbf apis.  this directory needs to be in the same directory as this script.
                      Downloaded from : http://dbfpy.sourceforge.net/

resources:
    http://www.tutorialspoint.com/python/python_basic_syntax.htm
    http://dbfpy.sourceforge.net/
    http://docs.python.org/2.6/library/csv.html
    http://www.gadzmo.com/python/reading-and-writing-csv-files-with-python-dictreader-and-dictwriter/
    https://github.com/fitnr/census2dbf/blob/master/census2dbf.py
"""

import sys
import csv
import re
import struct
import datetime
import itertools
import datetime
from dbfpy import dbf

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def new_file_ending(filename, new):
    try:
        k = filename.rindex('.')
        return filename[0:k] + new
    except:
        return filename + new

def get_field_type(header, field_name):
    for line in header:
        if line['FIELDNAME'] == field_name:
            return line['TYPE']


def main(argv=None):
    
    ####################################
    # requires two argument:
    # 1. input header (csv file) path/name
    # 2. input body   (csv file) path/name
    # 3. optional output file    path/name
    ####################################

    if (len(sys.argv) <= 2):
        print 'file name require, syntax: csv2dbf.py file_path'
        return 1

    header_file = sys.argv[1]
    body_file = sys.argv[2]
    
    if (len(sys.argv) == 4):
        output_file = sys.argv[3]
    else:
        output_file = None

    print 'header file ==> ' + header_file
    print 'body file   ==> ' + body_file

    if output_file is None:
        output_file = new_file_ending(body_file, '.dbf')

    print 'output file ==> ' + output_file

    ##############################
    #open the DBF file
    ##############################
    db = dbf.Dbf(output_file, new=True)

    ##############################
    #add the header info to the DBF
    ##############################
    header = csv.DictReader(open(header_file, 'rb'), delimiter=',')    
    for line in header:
        #print line['FIELDNAME'] + "," + line['TYPE'] + "," + line['LENGTH']
        if (line['TYPE'] == 'D'):
            db.addField((line['FIELDNAME'],line['TYPE']))
        else:    
            db.addField((line['FIELDNAME'],line['TYPE'],line['LENGTH']))

    ##############################
    # run through the body
    # add to the DB
    ##############################
    print "working with body-------------"
    body = csv.DictReader(open(body_file, 'rb'), delimiter=',', quotechar='"')    
    for line in body:
        rec = db.newRecord()
        #note: you need to reset the dict everytime
        header = csv.DictReader(open(header_file, 'rb'), delimiter=',')    
        for item in header:
            #print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            if (item['TYPE']=='D'):
                rec[item['FIELDNAME']] = line[item['FIELDNAME']]
            elif (item['TYPE']=='N'):
                rec[item['FIELDNAME']] = int(line[item['FIELDNAME']])
            else:    
                rec[item['FIELDNAME']] = line[item['FIELDNAME']]
        rec.store()

    print db
    db.close()
    print
    print '  *******success!*******'
    print
    return 0

if __name__ == "__main__":
    sys.exit(main())