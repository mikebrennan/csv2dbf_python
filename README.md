csv2dbf_python
==============

Creates a legacy dbf file from csv files using python dbf lib

This script converts CSV files to DBF

R:equirements:
    Header.csv - this contains the DBF definition (required names ==> FIELDNAME,TYPE,LENGTH)
                 1 FIELDNAME,TYPE,LENGTH
                 2 STAFF,N,10
                 3 STAFF_NAME,C,101
                 4 DATEIN,D,
                 5

    Body.csv   - this contains your db info based on you header FIELDNAME definitions
                 1 STAFF,STAFF_NAME,DATEIN
                 2 1234,joe smith,20130925
                 3 1235,jill smith,20130925
                 4

    dbfpy directory - This contains the library for dbf apis.  this directory needs to be in the same directory as this script.
                      Downloaded from : http://dbfpy.sourceforge.net/

Note: I have not tested this with DBF TYPE 'L' TRUE/FALSE.
