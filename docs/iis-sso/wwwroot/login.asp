<%@ Language = "Python" %>
<%
#########################################
# Configuration constants
SECRET = 'XXXXXX'
ALLOWED_SITES = [
    'http://localhost:8080/Plone',
]
DEFAULT_NEXT = 'http://localhost:8080/Plone/logged_in'
MOD_AUTH_TKT = False
#########################################
import tktauth
import binascii
import string
from urlparse import urlparse

Response.CacheControl = "no-cache"
Response.AddHeader("Pragma", "no-cache")
Response.Expires = -1
Response.AddHeader("Content-Type", "text/html; charset=utf-8")

CAME_FROM_NAME = 'came_from'
TICKET_NAME = '__ac'

next_url = DEFAULT_NEXT
next = Request.QueryString('next')

userid = str(Request.ServerVariables("REMOTE_USER"))
if not userid:
    # Don't process any further without credentials
    raise ValueError("You must not allow anonymous access to this page.")

if '\\' in userid:
    # if we get a domain for the user ignore it
    userid = userid.split('\\')[-1]

ticket = tktauth.createTicket(SECRET, userid, mod_auth_tkt=MOD_AUTH_TKT)
ticket = binascii.b2a_base64(ticket).rstrip()

came_from = Request.QueryString(CAME_FROM_NAME)
if not came_from or str(came_from) == 'None':
    came_from = ''

target = Request.QueryString('target')
if target in ('_parent', '_top', '_blank', '_self'):
    target_attr = 'target="%s"' % target
else:
    target_attr = ''

# An automatic form post is used to prevent the ticket being stored in the
# browser's history.

FORM = string.Template('''
<form action="$action" method="post" name="external_login_form"$target_attr id="external_login_form">
<!-- userid: $userid -->
<input type="hidden" name="$ticket_name" value="$ticket" />
<input type="hidden" name="$came_from_name" value="$came_from" />

Voc&ecirc; n&atilde;o tem JavaScript habilitado. Pressione o bot&atildeo para iniciar sess&atildeo:
<input type="submit" name="login" value="Login" class="button small radius" />
</form>
''')
form_html = FORM.substitute(
    action=next_url,
    target_attr=target_attr,
    ticket_name=TICKET_NAME,
    ticket=ticket,
    came_from_name=CAME_FROM_NAME,
    came_from=came_from,
    userid=userid,
    )

%>
<!doctype html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vindula SSO Login</title>
    <link rel="stylesheet" href="/css/foundation.css" />
    <script src="js/vendor/jquery.js"></script>
    <script src="js/vendor/modernizr.js"></script>

  </head>
  <body>
    <div class="row">
      <div class="large-12 columns">
        <center>
          <div class="logo"><img src="/img/logo.png"></div>
          <h1>Login</h1>
        </center>
      </div>
    </div>
    
    <div class="row">
      <div class="large-12 columns">
        <div class="panel radius">

            <p>Aguarde enquanto você está sendo logado na intranet</p>
<%
Response.write(form_html)
%>
            <script type="text/javascript">
                var external_login_form = document.getElementById('external_login_form');
                external_login_form.className = 'hide';
                external_login_form.submit();
            </script>
        </div>
                
      </div>
    </div>
  </body>
</html>