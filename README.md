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

**CompanyAPI.py** will provide the web access to the database and return the results of any query / action in JSON.

It is envisaged that all company actions will occur via the *CompanyAPI* class, receiving an instance of the *CompanyDB* class on instantiation in order to access the company database excluding database / table creation.

The *CompanyAPI* class will provide the following functionality:
- provide a single point of data conversion between web and database
- add a new company
- include a result and [error|data] in the returned JSON
- get the details of a companies using its ID
- get a paged list of companies, with the minimum being the restricted companies

### Scripts

**create_db.py** will use the supplied fake companies CSV to create the database.

The intent is that the script will be used to:
- instantiate the *CompanyDB* class to automatically create the database if it does not exist
- instantiate the *CompanyAPI* class, passing in the *CompanyDB* class
- unless the *--nocreate* option is specified, create the company table by calling the *CompanyDB* class function  
- unless the *--noload* option is specified, load the CSV file contents, and call the *CompanyAPI* function to add the company to the database per entry
- optionally perform a few of executions of the *CompanyAPI* to access data from the company database:  
the results are saved to a *JSON* file which is passed directly to the default browser to display

**company_web_api** will handle the request / response process for the hosted web site.

The intent is that the script will be always on - listening on a port waiting for requests, and that:
- the home page will be automatically supplied on initial request
- services the end points as required by the home and subsequent page actions

### Files

**company.html** will provide the base web page definition including any code (JavaScript) to perform any actions.

Three sections will be provided on the web page:
- *search* container will provide the search fields / buttons, and hold any error response  
On requesting the details of a company, the *company list* container will be automatically hidden.  
On requesting a company list, the *company* container will be automatically hidden.
- *company* container will sit within the *search* container - initially hidden  
The container will be populated by any successful response and be made visible.  
- *company list* container will sit within the *search* container - initially hidden  
The container will be populated by any successful response and made visible.

**company.css** will provide the web page Cascading Style Sheet (CSS)

The CSS will be referenced by the HTML file, and describe any text, button, table formatting.

### Web API queries

Web API queries will be used to populate the displayed page with data or error responses.

##### Company by ID

Accessing a company by *id* will require passing the company ID to via the Web API query.
For example `<web address>/GetCompanyById?id=<id>`

##### Company list

Accessing a company list will be paged based on a *count* per page to display value.

The web page will keep track of where we are in the list - which page we are on.
This enables passing teo value via the Web API query: the current *offset* and the *count* of rows to return.
That is, the *offset* would be `(page - 1) * count`.

An optional parameter will be passed to indicate whether we want: restricted, non-restricted, or all companies.

For example:
- to return companies in the list irrespective of restriction status:  
```<web address>/GetCompanyList?id=<id>&count=<count>```
- to return companies based on restriction status:  
```<web address>/GetCompanyList?id=<id>&count=<count>&restricted=[0|1]```

### JSON data response

All data from the Web API will be returned via a JSON data structure, as:

```
{
  "result" : "ok|error",
  "error"  : "Error text if an error results",
  "data" : {
    [
      {
        "id' : "integer as a string",
        ... company details ...
      }
      ...
    ]
  }
}
```
The *data* aspect of the JSON structure will only be an array for the *company list* operation, regardless of how many results are returned.

### Python packages

The project uses **python3** and the followin Python modules to deliver the functionality:

**python3-apsw** provides the interface to **SQLite**

**python3-hug** provides a simple Web API server

## Testing

The application can be run from with its own directory, by checking out the repository and following the next steps.

To create the database and populate the table with the supplied fake company data:

```
./create_db.py
```
If you want to verify the **No data** error responses, just rerun the create script with the noload option as:

```
./create_db.py --noload
```

### Testing without a Web API

To test the result without starting the Web API server, use one of the above command and specify test as:

```
./create_db.py --test
./create_db.py --noload --test
```
which will open new tabs in your default browser with the JSON result per query.

### Testing with a Web API

Hug provides a nice simple interface for servicing Web API requests.

Start the server in a terminal window as:

```
hug -f ./companyWebAPI.py
```
and the terminal will indicate when it is ready with a message like:

```
Serving on :8000...
```

Testing is best server via pasting the following entries in a web browser:

```
http://localhost:8000/
http://localhost:8000/GetCompanyById?id=0
http://localhost:8000/GetCompanyById?id=9
http://localhost:8000/GetCompanyById?id=10
http://localhost:8000/GetCompanyList?offset=0&count=5
http://localhost:8000/GetCompanyList?offset=5&count=10&restricted=0
http://localhost:8000/GetCompanyList?offset=3&count=2&restricted=1
```
Testing of the above should also work as a **curl** command from the command line.
