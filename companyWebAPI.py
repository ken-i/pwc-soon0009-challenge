#!/usr/bin/python3

#------------------------------------------------------

# companyWebAPI.py

# Python script to provide the Web API functions.

# The script receives the HTTP requests via a 'hug' server and calls the
# relevant CompanyAPI class function to perform the operation.

# CompanyAPI provides the interface to access the database and format the
# returned data to HTML.
# This is the only access the Web API will use.

# CompanyDB provides the interface to the Companies database.

# This script does not use the CompanyDB interface directly for anything - it
# merely instantiates the object and passes it to the CompanyAPI class so it
# can access the company database.

#------------------------------------------------------


import hug

from CompanyAPI import CompanyAPI
from CompanyDB import CompanyDB

# from optparse import OptionParser


@hug.get('/')
def home():
    # Returns the home (root) page data for the Web API.
    return "Home page"


@hug.get()
def GetCompanyById(id: hug.types.text):
    # Returns the company data.
    # id    is the company id to fetch.
    # print("companyWebAPI.GetCompanyById: id [%s]" % id)
    return companyAPI.GetCompanyById(id)


@hug.get()
def GetCompanyList(offset: hug.types.text, count: hug.types.text, restricted: hug.types.text = None):
    # Returns a list of companies.
    # offset        is the offset into the result to start returning rows.
    # count         is the maximum number of companies to return in the list.
    # restricted    is an optional boolean integer [0|1] indicating the subset of companies to return.
    # restrict = "All" if restricted is None else str(restricted)
    # print("companyWebAPI.GetCompanyList: offset [%s] count [%s] restrict [%s]" % (offset, count, restrict) )
    return companyAPI.GetCompanyList(offset, count, restricted)


# Main code to initialise the classes etc.

# global companyDB
# global companyAPI
#
# # Parse the command line options.
# parser = OptionParser(
#     description="Accepts HTML requests and generated HTML responses for the company Web API.",
#     epilog="The default values prevent the need to carry any overrides to downstream process equivalent options.")
#
# parser.add_option("--css", dest="cssFile", metavar="FILE", default="company.css",
#                   help="name of the CSS file to format the HTML output. Default: [company.css]")
# parser.add_option("--db", dest="database", default="company",
#                   help="name of the database. Default: [companyDB]")
# parser.add_option("--table", dest="dbTable", metavar="TABLE", default="Company",
#                   help="name of the table. Default: [Restricted]")
#
# (options, args) = parser.parse_args()
#
# # Instantiate the database interface.
# companyDB = CompanyDB(options.database + ".db3", options.dbTable)
#
# # Instantiate the Company Web API interface.
# companyAPI = CompanyAPI(company, options.cssFile)

# Instantiate the database interface.
companyDB = CompanyDB()

# Instantiate the Company Web API interface.
companyAPI = CompanyAPI(companyDB)
