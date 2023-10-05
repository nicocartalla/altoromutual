
from SqlInjection import SqlInjection

BASE_URL = "http://localhost:8080"
def main():
    total_exit_codes = 0
    total_output = ""

    # Login SQL Injection Test
    total_output += "***** Login SQL Injection Test *****\n"
    url = BASE_URL+"/doLogin"
    exit_code, output = SqlInjection.doLoginSqlI(url)
    total_exit_codes += exit_code
    total_output += output + "\n"
    
    # Otros tests ...
    
    # Write report
    with open('/mnt/dast-report.txt', 'w') as f:
        f.write(total_output)    
    if total_exit_codes == 1:
        exit(1)

if __name__ == "__main__":
    main()