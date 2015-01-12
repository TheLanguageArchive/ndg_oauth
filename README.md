# CLARIN OAUTH AS project #

This fork of the ndg_oauth project is aimed at enabling us to run the OAUTH Authorization Server (AS) behind an apache reverse proxy.
Some changes required for us and implemented by Willem van Engen have already been integrated in the main ndg_oauth project (https://github.com/cedadev/ndg_oauth).

## Requirements ##

* python 2.7
* openssl-dev 0.9.8f or later
* python virtualenv
* python easy_install

In Debian / Ubuntu:

```
sudo apt-get install build-essential openssl libssl-dev libffi-dev git python python-dev python-virtualenv
```

## Installation ##

[Work in progress]

This guide assumes installation of the AS in the /srv/OAuth

### Create Python 2 virtual environment for AS ###

```
virtualenv /srv/OAuth
```

### Switch to Python 2 venv ###

```
. /srv/OAuth/bin/activate
```

### Install pyopenssl package in the virtual environment ###
Ensure openssl-dev (and libffi-dev) is installed; then create the python openssl module:

```
easy_install pyOpenSSL
```

### install NDG AS ###
Fetch the source files from the Git repository into /srv/OAuth/src:

```
mkdir /srv/OAuth/src
cd /srv/OAuth/src
git clone https://github.com/TheLanguageArchive/ndg_oauth.git
easy_install /srv/OAuth/src/ndg_oauth/ndg_oauth_server/
```

Initialize the base server in /srv/OAuth/server:

```
mkdir -p /srv/OAuth/server
cp -r /srv/OAuth/src/ndg_oauth/ndg_oauth_server/ndg/oauth/server/examples/bearer_tok/* /srv/OAuth/server
rm /srv/OAuth/server/README /srv/OAuth/server/__init__.py
```

## OAuth AS configuration ##

### Server ###
After installation edit /srv/OAuth/server/bearer_tok_server_app.ini.

In order to start the AS with the paste http server, activate the virtual environment and start the server with the correct
configuration file:
```
. /srv/OAuth/bin/activate
cd /srv/OAuth/server
paster serve bearer_tok_server_app.ini start
```

### Clients ###

For each client you want to add to the AS you have to add a section in /srv/OAuth/server/client_register.ini

### Startup script ###

init.d script (oauthctl.sh):
```
#/bin/sh

case "$1" in
start)
    cd /srv/ndg-oath-as/ && \
    . /srv/python/2/venvs/OAuth/bin/activate && \
    paster serve bearer_tok_server_app.ini start
;;
stop)
    cd /srv/ndg-oath-as/ && \
    . /srv/python/2/venvs/OAuth/bin/activate && \
    paster serve bearer_tok_server_app.ini stop
;;
restart)
    cd /srv/ndg-oath-as/ && \
    . /srv/python/2/venvs/OAuth/bin/activate && \
    paster serve bearer_tok_server_app.ini restart
;;
*)
echo $"Usage: $0 {start|stop|restart}"
exit 1
esac
```

## Apache configuration ##

Configure and start the AS as described in the previous section. For this example we assume the AS is running at localhost
on port 8080.

We will define the reverse proxy mappings as follows:
```
https://your.server.com                       http://localhost:8080/
     /client_authorization/            --->       /client_authorization/

     /oauth-as/client_authorization/   --->       /client_authorization/
     /oauth-as/authorize               --->       /oauth-as/authorize


     /oauth-as/access_token            --->       /oauth-as/access_token
     /oauth-as/check_token             --->       /oauth-as/check_token
```

/client_authorization/ ---> /client_authorization/
```
<Location /client_authorization/>
    #Configure your authentication here

    RequestHeader set X_FORWARDED_USER %{REMOTE_USER}s
    ProxyPass https://localhost:8080/client_authorization/
    ProxyPassReverse https://localhost:8080/client_authorization/
    ProxyPassReverseCookiePath /client_authorization/ /client_authorization/
</Location>
```

/oauth-as/client_authorization/   --->       /client_authorization/
```
<Location /oauth-as/client_authorization/>
    #Configure your authentication here

    RequestHeader set X_FORWARDED_USER %{REMOTE_USER}s
    ProxyPass https://localhost:8080/client_authorization/
    ProxyPassReverse https://localhost:8080/client_authorization/
    ProxyPassReverseCookiePath /client_authorization/ /oauth-as/client_authorization/
</Location>
```

/oauth-as/authorize               --->       /oauth-as/authorize
```
<Location /oauth-as/authorize>
    #Configure your authentication here

    RequestHeader set X_FORWARDED_USER %{REMOTE_USER}s
    ProxyPass https://localhost:8080/oauth-as/authorize
    ProxyPassReverse htps://localhost:8080/oauth-as/authorize
    ProxyPassReverseCookiePath /oauth-as/authorize /oauth-as/authorize
</Location>
```

/oauth-as/access_token            --->       /oauth-as/access_token
```
<Location /oauth-as/access_token>
    ProxyPass https://localhost:8080/oauth-as/access_token
    ProxyPassReverse htps://localhost:8080/oauth-as/access_token
</Location>
```

/oauth-as/check_token             --->       /oauth-as/check_token
```
<Location /oauth-as/check_token>
    ProxyPass https://localhost:8080/oauth-as/check_token
    ProxyPassReverse htps://localhost:8080/oauth-as/check_token
</Location>
```

# Original ndg_oauth documentation #

ndg_oauth
=========
Python OAuth 2.0 Implementation including client and server packages:
 * ndg_oauth_client
 * ndg_oauth_server

These include WSGI wrappers for easy integration with Python frameworks such as Pylons/Pyramid or Django.

Both are available on PyPI e.g.
```
$ pip install ndg_oauth_client ndg_oauth_server
```

Latest release is version 0.5.0.
