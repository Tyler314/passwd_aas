Passwd as a Service

# Installation

passwd_aas reqires python 3.7 or newer

to install,
1) clone this directory
2) python setup.py install
```bash
$ git clone git@github.com:Tyler314/passwd_aas.git
$ cd passwd_aas
$ python setup.py install
```

# CLI

Once installed, you can use the service on the command line with the command `passwd-aas`

The following arguments are available:

-r, --run:
> Runs the application. Required to run.

-p, --passwd:
> Specify the full file path to the passwd file. This is optional, default is `/etc/passwd`.

-g, --group:
> Specify the full path to the group file. This is optional, default is `/etc/group`.

-v, --version:
> Display the version number.

--port:
> Specify the port to run the application on, on localhost. This is optional, default is port 8080.

For example, running `passwd-aas --run` will run the application, using `/etc/passwd` and `/etc/group, and run on 
`http://localhost:8080`

# Within Web Browser

Once the application is running, you can use the following HTTP request methods on your local host, at the port you
specified (8080 if you did not specify a port).

GET /users:
> Returns a list of all users on the system, as defined in the passwd file.

GET
/users/query\[?name=\<nq>]\[&uid=\<uq>]\[&gid=\<gq>]\[&comment=\<cq>]\[&home=\<hq>]\[&shell=\<sq>]
> Returns a list of users matching all of the specified query fields. The brackets indicate that any of the queries may
be supplied.

GET /users/\<uid>
> Returns a single user with \<uid>. Return 404 if \<uid> is not found.

GET /users/\<uid>/groups
> Returns all the groups for a given user.

GET /groups
> Returns a list of all groups on the system, as defined by the group file.

GET /groups/query\[?name=\<nq>]\[&gid=\<gq>]\[&member=\<mq1>\[&member=\<mq2>]\[&...]]
> Returns a list of groups matching all of the specified query fields. The brackets indicate that any of the queries may
be supplied.

GET /groups/<gid>
> Return a single group with \<gid>. Return 404 if \<gid> is not found.

# Within Python

The application is also able to run within a Python environment. The business logic is separated from networking logic, 
within `get.py` and `app.py` respectively. To use the business logic, create a Get object, and use its api.

```python
import passwd_aas
getter = passwd_aas.Get()
```

The Get api has the following:

set\_passwd\_path(path):
    
> Set the full path to the passwd file

set\_group\_path(path):

> Set the full path to the group file

users(name, uid, gid, comment, home, shell):

> Return list of user dictionaries. Optional keyword arguments used to filter users of interest. If no arguments specified, returns all users from the specified passwd file. If no user is found based on search criteria, return an empty list.

groups(name, gid, members):

> Return list of dictionaries. Optional keyword arguments used to filter groups of interest. If no arguments specified, returns all groups from the specified group file. If no group is found based on search criteria, return an empty list.

groups\_by\_uid(uid):
> Return list of dictionaries. Special case, look up group based on required argument uid. If no group exists with specified uid, return an empty list.

