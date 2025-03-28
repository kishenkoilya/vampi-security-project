import requests
import json
import os
from dotenv import load_dotenv

# Choose either username or email here
def acquire_token(username: str="", password: str=""):
    # Define endpoint that is used to login
    url = "http://localhost:5002/users/v1/login"

    # Define POST payload data field to login
    payload = json.dumps({
        "username": username,
        "password": password
    })

    # Clarfiy headers used to login
    #   - Content-Type header probably is the default one
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Specify aquire_token.log path
    with open(os.path.join("/home/ilya/restler-fuzzer/build/restler", "Test", "acquire_token.log"), "a+") as f:
        # Try to send login requrest
        rsp = requests.request("POST", url, headers=headers, data=payload)
        # Verify error code
        if rsp.status_code == 200:
            # In the most cases, we have to parse response body to extract token
            rsp_data = rsp.json()
            print(f"Authentication attempt registred:\n  - data={rsp_data}\n  - headers={rsp.headers}\n\n", file=f)

            # Extract token: from response body, from response header, from cookie-file, ...
            token = rsp_data["auth_token"]

            return f'Authorization: bearer {token}'

        print(f"Authentication failed\n\n", file=f)
        # Something invalid
        return "Authorization: Negotiate"


# This is necessary string to let RESTler know about authentication
# metadata = "{u'first_token': {u'username':u'name1'}}"
metadata = "{u'first_token': {u'username':u'admin'}, u'second_token': {u'username':'name1'}}"
load_dotenv()
lgn1 = os.getenv("login1")
pswd1 = os.getenv("password1")
lgn2 = os.getenv("login2")
pswd2 = os.getenv("password2")

# Printing is necessary
print(metadata)
print(acquire_token(lgn1,pswd1))
print(acquire_token(lgn2,pswd2))
# print(acquire_token(username="name1", password="pass1"))
