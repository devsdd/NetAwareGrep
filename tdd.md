## Test Cases

The code for the tests is contained in the files **test_weblog_helper.py** and a helper file **conftest.py** (which enables testing with real life command-line arguments.

These are the test cases as of this writing

* is there a function in the code to parse command-line arguments?
* does command-line args parsing work?
* does it return a CIDR string?
* is the command-line argument a valid CIDR address?
* is there a flag identifying if the command-line argument is a single host or a subnet?
* if subnet, can we get a list of all IP's from that subnet?
* can we extract strings for common subnets (/8, /16 and /24) to speed up execution of our program?
* is the configfile present and accessible?
* can we parse logfile path out of configfile?
* is there a function to grep for a single IP in log?
