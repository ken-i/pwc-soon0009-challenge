# pwc-soon0009-challenge

Companies Web API project in Python

## Purpose

Create a process that keeps a list of companies restricted and unrestricted status up to date.

Fetch the list of companies and load the companies into a relational database.

Build a RESTful Web API with a light weight web interface that can query the database to fulfill the following users stories.


### User Stories

Check company restriction:

> As a user I want to search by business number so that I can know if the company is restricted.

> Acceptance criteria:

>> business numbers should only compose of numbers  
>> seaching business numbers should only return results for an exact match

List restricted companies:

> As a user I want to list all restricted companies so I know all the restricted companies in the system.

> Acceptance criteria:

>> Results should be paginated at 100 items

### List of companies

A list of fake companies used for the database can be found at: [https://storage.googleapis.com/snappy-recruitment-test/faux_id_fake_companies.csv](https://storage.googleapis.com/snappy-recruitment-test/)

### Overall acceptance criteria

> Implementation must use Python in the backend with a simple html and css frotend

> Host your solution and provide us a URL e.g. Azure, Google Cloud or AWS

> Provide Github access to the code

## Design

The initial design is to provide two Classes and two scripts.

### Classes

**CompanyDB.py** will provide the access to the companies database, including creation, and supply function to: add a company, get a company by ID, and get a list of companies in pages.

The database will be handled using SQLite, with the class on instantiation automatically creating the *company* database if it does not exist, and provide functionality to:
- recreate the table in that it will drop the existing table and then create the table afresh
- add a new company to the database
- supply a count of the table rows, the minimum and maximum company ID
- get a companies details using its ID
- get a paged list of companies, with the minimum being the restricted companies

**CompanyAPI.py** will provide the web access to the database and return the results of any query / action in HTML / CSS.

It is envisaged that all company actions will occur via the *CompanyAPI* class, receiving an instance of the *CompanyDB* class on instantiation in order to access the company database excluding database / table creation.

The *CompanyAPI* class will provide the following functionality:
- load the CSS file on instantiation if one is provided and exists
- provide a single point of data conversion between web and database
- add a new company
- include the CSS in the returned HTML
- provide the home page for the Web API
- get a companies details using its ID
- get a paged list of companies, with the minimum being the restricted companies

### Scripts

**create_db.py** will use the supplied fake companies CSV to create the database.

The intent is that the script will be used to:
- instantiate the *CompanyDB* class to automatically create the database if it does not exist
- instantiate the *CompanyAPI* class, passing in the *CompanyDB* class
- unless the *--nocreate* option is specified, and the CSV file exists:  
create the company table by calling the *CompanyDB* class function  
read the CSV file contents, and call the *CompanyAPI* function to add the company to the database per entry
- optionally perform a few of executions of the *CompanyAPI* to access data from the company database:  
the results are saved to a *html* file which is passed directly to the default browser to display

**company_web_api** will handle the request / response process for the hosted web site.

The intent is that the script will be always on - listening on a port waiting for requests, and that:
- the home page will be automatically supplied on initial request
- services the end points as required by the home and subsequent page actions
