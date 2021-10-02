#!/usr/bin/python3

#------------------------------------------------------

# CompanyAPI.py

# Python class defining API access to the Companies database.

# The class provides the functions for the Web API to access the database and
# build the HTML (including CSS) representation of the data, which is returned
# back to the caller.

#------------------------------------------------------

from CompanyDB import CompanyDB


class CompanyAPI:

    def __init__(self, companyDB):
        # Initialise the class with an instance of the CompanyDB class.

        self.companyDB = companyDB


    def AddNewCompany(self, row):
        # Write the company to the database.

        # Row is a dictionary of key / value pairs in any order:
        #     id, companyName, description, tagline, companyEmail, businessNumber, restricted

        # Convert string for 'restricted' back to an integer boolean.
        row["restricted"] = "0" if row["restricted"].lower() == "no" else "1"
        # print("CompanyAPI.AddNewCompany: row [%s]" % row)

        self.companyDB.AddNewCompany(row)


    def FormatTupleAsDict(self, row):
        # Converts the return DB row as a dictionary.
        restricted = "No" if row[6] == 0 else "Yes"

        rowDict = {}
        rowDict["id"] = row[0]
        rowDict["companyName"] = row[1]
        rowDict["description"] = row[2]
        rowDict["tagline"] = row[3]
        rowDict["companyEmail"] = row[4]
        rowDict["businessNumber"] = row[5]
        rowDict["restricted"] = restricted

        # print("CompanyAPI.FormatTupleAsDict: row [%s] rowDict [%s]" % (row, rowDict) )
        return rowDict


    def GetCompanyById(self, id):
        # Get a specific company by id and return its details.
        # print("CompanyAPI.GetCompanyById: id [%s]" % id)

        jsonStr = ""

        # Make sure we have digits and nothing more.
        if id.isdigit() == False:
            error = "Company ID [%s] is not valid" % id
            respDict = { "result" : "error", "error" : error}
            print("CompanyAPI.GetCompanyById: response [%s]" % respDict)
            return respDict

        # Get the company details.
        row = []
        row = self.companyDB.GetCompanyById(id)

        # Check for no result.
        if len(row) == 0:
            error = "No company found with ID [%s]" % id
            respDict = { "result" : "error", "error" : error}
            print("CompanyAPI.GetCompanyById: response [%s]" % respDict)
            return respDict

        else:
            # Must have a result.
            rowDict = self.FormatTupleAsDict(row)
            respDict = { "result" : "ok", "data" : rowDict}
            print("CompanyAPI.GetCompanyById: response [%s]" % respDict)
            return respDict


    def GetCompanyList(self, offset, count = 100, restricted = None):
        # Get a list of companies:
        #     matching the restricted flag if supplied,
        #     starting at offset in the SQL query result,
        #     to a maximum of count companies.
        # restrict = "All" if restricted is None else str(restricted)
        # print("CompanyAPI.GetCompanyList: offset [%s] count [%s] restrict [%s]" % (offset, count, restrict) )

        # Make sure we only have valid values.
        error = ""
        if offset.isdigit() == False:
            error = "Get Company List input parameter 'offset' [%s] is not valid" % offset
        elif (count.isdigit() and (int(count) > 0)) == False:
            error = "Get Company List input parameter 'count' [%s] must be greater than zero" % count
        elif (restricted is None) == False:
            if ( (restricted.isdigit()) == False) or ( (int(restricted) < 0) or (int(restricted) > 1) ) == True:
                error = "Get Company List input parameter 'restricted' [%s] must be [0 or 1]" % restricted
        if error != "":
            respDict = { "result" : "error", "error" : error}
            print("CompanyAPI.GetCompanyList: response [%s]" % respDict)
            return respDict

        # Get the company list.
        rows = self.companyDB.GetCompanyList(offset, count, restricted)

        # Check for no result.
        if len(rows) == 0:
            restrict = "" if restricted is None else " Restricted" if restricted == "1" else " Not restricted"
            error = "No companies matching search criteria -%s with offset [%s] in the result set" % (restrict, offset)
            respDict = { "result" : "error", "error" : error}
            print("CompanyAPI.GetCompanyList: response [%s]" % respDict)
            return respDict

        else:
            # Must have a result.
            rowList = []

            # Loop through the returned rows.
            for id, row in rows.items():
                rowDict = self.FormatTupleAsDict(row)
                rowList.append(rowDict)

            respDict = { "result" : "ok", "data" : rowList}
            print("CompanyAPI.GetCompanyList: response [%s]" % respDict)
            return respDict
