# CLARIN OAUTH AS project #

This fork of the ndg_oauth project is aimed at enabling us to run the OAUTH AS behind an apache reverse proxy.
Some changes required for us and implemented by Willem van Engen have already been integrated in the main ndg_oauth project.

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
