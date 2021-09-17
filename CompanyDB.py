#!/usr/bin/python3

#------------------------------------------------------

# CompanyDB.py

# Python class defining access interface to the companies database.

# The database is held in SQLite.

# Companies database / tables:

# Companies
# ---------
# pkID (Integer Primary Key)
# id (Integer)                Unique ID for the company.
# companyName (Text)          Name of the company.
# description (TEXT)
# tagline (Text)
# companyEmail (Text)
# businessNumber (Text)
# restricted (Integer)        [0|1] representing [False|True]

#------------------------------------------------------

import apsw

from builtins import int


class CompanyDB:

    def __init__(self, database = "company.db3", table = "Company"):
        # Initialise the class with the database / table names.
        global connection
        global cursor

        self.database = database
        self.table = table
        self.totalcount = 0
        self.minkey = 0
        self.maxkey = 0

        connection=apsw.Connection(self.database)
        cursor=connection.cursor()


    def AddNewCompany(self, row):
        # Write the company to the database.
        # print("CompanyDB.AddNewCompany: row [%s]" % row)

        # Row is a dictionary of key / value pairs in any order:
        #     id, companyName, description, tagline, companyEmail, businessNumber, restricted

        sql = "INSERT INTO %s (id, companyName, description, tagline, companyEmail, businessNumber, restricted) " % self.table
        sql += "VALUES (?, ?, ?, ?, ?, ?, ?)"
        # print("Executing SQL statement [%s]" % sql)
        cursor.execute(sql, (row["id"], row["companyName"], row["description"], row["tagline"],
                             row["companyEmail"], row["businessNumber"], row["restricted"]) )


    def Close(self):
        # Close the database cleanly.
        connection.close(True)


    def CountRows(self):
        # Some basic statistics about the companies in the table.
        # Clear in case NULL values result.
        self.totalcount = 0
        self.minkey = 0
        self.maxkey = 0

        sql = 'SELECT count(*), min(id), max(id) FROM %s' % self.table
        # print("Executing SQL statement [%s]" % sql)
        for x in cursor.execute(sql):
            self.totalcount = int(x[0])
            if (self.totalcount):
                self.minkey = int(x[1])
                self.maxkey = int(x[2])

        # print('Rows: total [%d] keys: min [%d] max [%d]' % (self.totalcount, self.minkey, self.maxkey) )


    def GetCompanyById(self, id):
        # Get a specific company by id and return its details.
        # print("CompanyDB.GetCompanyById: id [%s]" % id)

        sql = "SELECT id, companyName, description, tagline, companyEmail, businessNumber, restricted"
        sql += " FROM %s" % self.table
        sql += " WHERE id = %s" % str(id)
        # print("Executing SQL statement [%s]" % sql)

        row = []
        for x in cursor.execute(sql):
            if x[0] != "":
                row = x
        # print("CompanyDB.GetCompanyById: row [%s]" % row)

        # Return the result.
        return row


    def GetCompanyList(self, offset, count = 100, restricted = None):
        # Get a list of companies:
        #     matching the restricted flag if supplied,
        #     starting at offset in the SQL query result,
        #     to a maximum of count companies.
        # restrict = "All" if restricted is None else str(restricted)
        # print("CompanyDB.GetCompanyList: offset [%s] count [%s] restrict [%s]" % (offset, count, restrict) )

        sql = "SELECT id, companyName, description, tagline, companyEmail, businessNumber, restricted"
        sql += " FROM %s" % self.table
        if restricted is not None:
            sql += " WHERE restricted = %s" % restricted
        sql += " ORDER BY id"
        sql += " LIMIT %s" % str(count)
        sql += " OFFSET %s" % str(offset)
        # print("Executing SQL statement [%s]" % sql)

        rows = {}
        for x in cursor.execute(sql):
            if x[0] != "":
                key = x[0]
                rows[key] = x
        # print("CompanyDB.GetCompanyList: rows [%s]" % rows)

        # Return the result.
        return rows


    def RecreateTable(self):
        # Drop the table if it already exists.
        sql = 'DROP TABLE IF EXISTS %s' % self.table
        cursor.execute(sql)
    
        # Create the table is not already existing.
        sql = 'CREATE TABLE IF NOT EXISTS %s ' % self.table
        sql += '(pkID INTEGER PRIMARY KEY'
        sql += ', id INTEGER UNIQUE NOT NULL'
        sql += ', companyName TEXT NOT NULL'
        sql += ', description TEXT'
        sql += ', tagline TEXT'
        sql += ', companyEmail TEXT'
        sql += ', businessNumber TEXT'
        sql += ', restricted INTEGER DEFAULT 0'
        sql += ')'
        # print("Executing SQL statement [%s]" % sql)
        cursor.execute(sql)
