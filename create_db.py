#!/usr/bin/python3

#------------------------------------------------------

# create_db.py

# Python script to create the companies database and validate its operation
# via the API.

# CompanyAPI provides the interface to access the database and format the
# returned data to JSON.
# This is the only access the Web API will use.

# CompanyDB provides the interface to the Companies database.

# This script uses the CompanyDB interface for creating the database /
# table, otherwise all access is via the CompanyAPI interface.

# The table is created from a supplied CSV file of entries defined as:
#
# CSV heading row is used to set the field names for a CSV DictReader:
#   id, fake-company-name, description, tagline, company-email, business number, Restricted

# Heading are translated before calling the CompanyAPI.AddNewCompany function to:
#   id, companyName, description, tagline, companyEmail, businessNumber, companyDB

# Data rows have no quotes, and therefore expect no commas within fields, as:
#   1,Bergstrom PLC,Reactive Content-Based Complexity,Drive Leading-Edge Architectures,becker.jeremie@nikolaus.com,682216138,No
#   6,"Bins, Kohler and Kuhlman",Enterprise-Wide Optimal Matrices,Drive B2C Models,dstokes@west.com,88-3175292,No
#   10,"Leuschke, Stamm and Green",User-Friendly Global Encryption,Synergize Holistic Portals,berenice64@krajcik.com,441172968,Yes
# Notes:
# 1. The 'id' field will be used to search for a company by ID, and will also prevents insertion order causing corruption.
# 2. The 'business number' may include non-digit characters, and is therefore held as Text.
# 3. The 'Restricted' value is supplied in the CSV as [Yes|No], and is converted to an integer boolean [1|0] in the database

#------------------------------------------------------


import csv
import json
import os
import webbrowser

from CompanyAPI import CompanyAPI
from CompanyDB import CompanyDB

from optparse import OptionParser
from time import sleep


def CreateDBTable(csvFile):
    # Create the Company companyDB database with the contents from the filename.
    companyDB.RecreateTable()

    # Record starting statics.
    companyDB.CountRows()
    print("Recreate DB statistics: total [%d] keys: min [%s] max [%s]" % (companyDB.totalcount, companyDB.minkey, companyDB.maxkey) )


def LoadCSVFile(csvFile):
    # Open the CSV file and sniff out the dialect / format used.
    with open(csvFile, newline='') as csvFile:
        dialect = csv.Sniffer().sniff(csvFile.read(1024))
        csvFile.seek(0)
        # Assume the CSV file has the heading to be the dictionary keys.
        # reader = csv.DictReader(csvFile, dialect, restkey="REST")
        reader = csv.DictReader(csvFile, restkey="REST")
        for row in reader:
            # for key in row.keys():
            #     print("CSV file row: key [%s] value [%s]" % (key, row[key]) )
            SaveRow(row)

    companyDB.CountRows()
    print("LoadCSVFile statistics: total [%d] keys: min [%s] max [%s]" % (companyDB.totalcount, companyDB.minkey, companyDB.maxkey) )


def SaveRow(row):
    # Save the read row to the database.
    # Need to translate the row key names to the equivalent database column names.
    newRow = dict({"id"             : row["id"],
                   "companyName"    : row["fake-company-name"],
                   "description"    : row["description"],
                   "tagline"        : row["tagline"],
                   "companyEmail"   : row["company-email"],
                   "businessNumber" : row["business number"],
                   "restricted"     : row["Restricted"] })
    companyAPI.AddNewCompany(newRow)


def TestAPI():
    # Test the company database api access.

    # Get specific company.
    TestAPI_GetCompanyByID(0)
    sleep(1)
    TestAPI_GetCompanyByID(9)
    sleep(1)
    TestAPI_GetCompanyByID(10)

    # Get a small list of companies.
    TestAPI_GetCompanyList(7)
    sleep(1)
    TestAPI_GetCompanyList(3, 2, 1)
    sleep(1)
    TestAPI_GetCompanyList(5, 10, 0)


def TestAPI_GetCompanyByID(id):
    # Test the GetCompanyByID via the API.
    # print("TestAPI_GetCompanyByID: id [%s]" % id)

    companyDict = companyAPI.GetCompanyById(id)
    jsonStr = json.dumps(companyDict)

    fi = open('company.json','w')
    fi.write(jsonStr)
    fi.close()

    webbrowser.open('company.json')


def TestAPI_GetCompanyList(id, count = 5, restricted = None):
    # Test the GetCompanyList via the API.
    # restrict = "All" if restricted is None else str(restricted)
    # print("TestAPI_GetCompanyList: id [%s] count [%s] restricted [%s]" % (id, count, restrict) )

    companyDict = companyAPI.GetCompanyList(id, count, restricted)
    jsonStr = json.dumps(companyDict)
    
    fi = open('company_list.json','w')
    fi.write(jsonStr)
    fi.close()
    
    webbrowser.open('company_list.json')


def main():
    global companyDB
    global companyAPI

    # Parse the command line options.
    parser = OptionParser(
        description="Create / Recreate a relational database and optionally load the table from a CSV file.",
        epilog="The default values prevent the need to carry any overrides to downstream process equivalent options.")

    parser.add_option("--csv", dest="csvFile", metavar="FILE", default="faux_id_fake_companies.csv",
                      help="name of the existing CSV file holding the company list. Default: [faux_id_fake_companies.csv]")
    parser.add_option("--db", dest="database", default="company",
                      help="name of the database. Default: [companyDB]")
    parser.add_option("--table", dest="dbTable", metavar="TABLE", default="Company",
                      help="name of the table. Default: [Restricted]")
    parser.add_option("--nocreate", dest="createDBTable", action="store_false", default=True,
                      help="stops the create / recreate of the database table. Default is to create the table.")
    parser.add_option("--noload", dest="loadDB", action="store_false", default=True,
                      help="stops the loading of data into the database table. Default is to load the data.")
    parser.add_option("--test", dest="testAPI", action="store_true", default=False,
                      help="determines if a quick test of the API occurs. Default: [False]")

    (options, args) = parser.parse_args()

    # Instantiate the database interface.
    companyDB = CompanyDB(options.database + ".db3", options.dbTable)

    # Instantiate the Company Web API interface.
    companyAPI = CompanyAPI(companyDB)

    if options.createDBTable:
        CreateDBTable(options.csvFile)

    if options.loadDB:
        if os.path.isfile(options.csvFile):
            LoadCSVFile(options.csvFile)
        else:
            print("ERROR: File [%s] does not exist\n" % options.csvFile, file=sys.stderr)
            # parser.parse_args(args=["-h"])
            parser.print_help()
            return

    # Check if we want to test the API access.
    if options.testAPI:
        TestAPI()

    # Cleanly close.
    companyDB.Close


if __name__ == '__main__':
    main()
