# Weather CLI project notes
https://realpython.com/build-a-python-weather-app-cli/#step-1-get-access-to-a-suitable-weather-api

## API and code
- keep API user info secure
-- use a .gitignore file to protect this info
- seperate out the tasks in public and private functions
-- this project seperated out building and sending the query
- important modules:
-- urllib and configparser

### accessing an api in a project
- important to protect information, so do not add the api key to the code, but to a seperate config file 
- INI is a file that can help organize config data to be easily accessed
-- INI files can be organized via sections [section name] with key=value pairs
- ConfigParser module helps to read a config file
-- ConfigParse is able to access the INI file using the section and key values, similar to a dictionary object
-- access the INI file in a private function

### building an API query
- read the API documentation to see how the information is queried and returned
- use formatting strings to enter the data to the right format
- use urllib module parse.quote_plus to format input for HTTPS requests when necessary
- seperate the base url and the query strings into variables
-- this project uses a global variable for the base url, and uses a function to build the query

### getting and returning API query information
- read documentation to see what type of data is expected
- use urllib.request to send the api query
- because it is over the internet, the data might come not be accessible
-- prepare for this by using try:except:
-- give users some context for errors, not just error codes
-- use sys.exit() with a message parameter to gracefully end a program and give info to the user
- in this project, the data is returned as a JSON
- JSON can be parsed into a python object using the json.loads() function
-- the data returned by the api query might be corrupt, use a try:except:
-- if there is an error, make sure to give the user a clean message

## getting command line arguments
- use the argparse module
- give the user info in -h via the description parameter for the ArgumentParser object, and the help parameter of the add_argument() function
- positional arguments don't need a dash, optional arguments do
- action parameter of add_argument() can give defaults for arguments
- nargs can give the number of arguments for the user to pass
- CLI arguments are returned by ArgumentParser.parse_args() as a namespace object
-- the individual arguments are accessed via dot notation
-- example: namespace_var.arg_name
-- example: user_args.city

## formatting and styling output
- use a function to organize styling and printing the output
- this program also uses a seperate style.py file to hold constants
- using padding in text output can make it more readable
- colors can be used to convey information about the text

# unanswered questions
- which is better: an INI file or a env.py file?
- how to order the functions within the program code?
- when to seperate out constants into a seperate file?
-- style.py makes weather.py easier to read, but there are not that many constants
- in a project w/o classes, how to decide when a function in private or not?
- why use the if __main__=='__name__' code block to control flow and not a main() function?

# ideas to expand the program
- allow a default city
-- is this best used in the INI file? or could it be set by the user via a CLI arg?
- access more information via options
-- such as: forecast, multiple cities, 'long' output with more info