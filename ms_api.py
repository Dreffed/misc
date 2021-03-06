import json
import getpass 

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions

url = "https://rockymountaineer.sharepoint.com"
s_url = "https://rockymountaineer.sharepoint.com/sites/GE/Shared%20Documents/Forms/AllItems.aspx"
u = "dgloyncox"

try: 
    p = getpass.getpass()
except Exception as error: 
	print('ERROR', error) 

ctx_auth = AuthenticationContext(url)
if ctx_auth.acquire_token_for_user(u, p):
    request = ClientRequest(ctx_auth)
    options = RequestOptions("{0}/_api/web/".format(url))
    options.set_header('Accept', 'application/json')
    options.set_header('Content-Type', 'application/json')
    data = request.execute_request_direct(options)
    s = json.loads(data.content)
    web_title = s['Title']
    print("Web title: " + web_title)
    
else:
    print(ctx_auth.get_last_error())