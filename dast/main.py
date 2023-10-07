
from SqlInjection import SqlInjection
from Xss import Xss
import sys



def main():

    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    else:
        BASE_URL = "http://localhost:8080"

    total_exit_codes = 0
    total_output = ""
    total_tests = 2
    tests_passed = 0

    # Login SQL Injection Test
    total_output += "***** Login - SQL Injection Test *****\n"
    url = BASE_URL+"/doLogin"
    exit_code, output = SqlInjection.doLoginSqlI(url)
    total_exit_codes += exit_code
    total_output += output + "\n"
    if exit_code == 0:
        tests_passed += 1
    
    # Otros tests ...
    total_output += "***** Search - Cross Site Scripting Test  *****\n"
    url = BASE_URL+"/search.jsp"
    exit_code, output = Xss.search(url)
    total_exit_codes += exit_code
    total_output += output + "\n"
    if exit_code == 0:
        tests_passed += 1

    # Write report
    total_output += f"Total tests passed: {tests_passed}/{total_tests}\n"
    print(f"Total tests passed: {tests_passed}/{total_tests}\n")
    with open('/tmp/dast-report.txt', 'w') as f:
        f.write(total_output)    
    if total_exit_codes > 0:
        exit(1)

if __name__ == "__main__":
    main()