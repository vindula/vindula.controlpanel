

Doc: https://pypi.python.org/pypi/plone.session#Single Sign On with IIS

Python on IIS
Install Python: 2.6.6
Install Lib: pywin32-218.win-amd64-py2.6
Place a copy of tktauth.py into: "C:\Python26\Lib\site-packages\"




IIS Site
Anonymous Authentication: Disable
Windows Authentication: Enable
Properties - > Security: add Group of menbers to access 
Copy folde wwwroot to site root


Configuration
You need to modify the SECRET constant found in the login.asp to the same shared secret set on plone.session's Manage secrets tab.
Modify the ALLOWED_SITES constant in login.asp to include the URLs of your Plone sites.
Modify the DEFAULT_NEXT constant in login.asp to refer the the URL of logged_in on one of your Plone sites.