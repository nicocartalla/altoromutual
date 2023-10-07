import requests
from urllib.parse import quote



payloads = [
    "<script>alert(document.cookie)</script>",
    "<script>alert('xss')</script>",
    "<img src=x onerror=alert('xss')>",
    "javascript:alert('xss')"
]

class Xss():

    @staticmethod
    def search(url):
        exit_code = 0
        output = ""
        for payload in payloads:
            encode_payload = quote(payload, safe='')
            target = f"{url}?query={encode_payload}"
            
            response = requests.get(target)
            if payload in response.text:
                output += f"[!] An XSS was detected in the URL: {target}\n"
                print(f"[!] An XSS was detected in the URL: {target}")
                exit_code += 1
            else:
                output += f"[*] No XSS was detected in the URL: {target}\n"
                print(f"[*] No XSS was detected in the URL: {target}")

        return exit_code, output, len(payloads)