"""
need requests, jsonify
use flask and mysql for backend

html front end
python backend

user inputs a url into the frontend, this is processed to the url shortener and then given back to the user

make sure new urls are unique and can't be overwritten
-------------------------------------------------------
the api needs to be able to create a shortened url
still have access to the old url
update an existing shortened url
delete an existing shortened url
get the number of times it was accessed.
-------------------------------------------------------
the front end needs to provide
a way for the user to plug in their full url
a way to retrieve the shortened one
-------------------------------------------------------
the data base needs to be able to hold this data
an id number
the original url
the shortened string
when it was created
when it was last updated


Operation should go as:
Frontend html page
process through rest api
write to database


"""




