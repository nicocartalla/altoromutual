
from SqlInjection import SqlInjection
from Xss import Xss
import sys



def main():

    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    else:
        BASE_URL = "http://localhost:8080"

    total_output = ""
    total_tests  = 0
    tests_error  = 0

    # Login SQL Injection Test
    total_output += "***** Login - SQL Injection Test *****\n"
    url = BASE_URL+"/AltoroJ/doLogin"
    exit_code, output, tests = SqlInjection.doLoginSqlI(url)
    tests_error += exit_code
    total_tests += tests
    total_output += output + "\n"
    
    # Otros tests ...
    total_output += "***** Search - Cross Site Scripting Test  *****\n"
    url = BASE_URL+"/AltoroJ/search.jsp"
    exit_code, output,tests = Xss.search(url)
    tests_error += exit_code
    total_tests += tests
    total_output += output + "\n"
    

    # Write report
    total_output += f"Total tests passed: {total_tests-tests_error}/{total_tests}\n"
    print(f"Total tests passed: {total_tests-tests_error}/{total_tests}\n")
    with open('/tmp/dast-report.txt', 'w') as f:
        f.write(total_output)    
    if tests_error > 0:
        exit(1)

if __name__ == "__main__":
    main()