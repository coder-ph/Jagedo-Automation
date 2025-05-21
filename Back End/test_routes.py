import requests
import json
from colorama import init, Fore, Style

init()

BASE_URL = "http://localhost:5000"

# Role-specific login credentials
LOGIN_CREDENTIALS = {
    "admin": {
        "email": "admin@admin.com",
        "password": "password123"
    },
    "professional": {
        "email": "ryan46@example.net",
        "password": "password123"
    },
    "customer": {
        "email": "richard60@example.com",
        "password": "password123"
    }
}

def print_response(description, response, expect_unauthorized=False):
    print(f"\n{Fore.CYAN}=== {description} ==={Style.RESET_ALL}")
    print(f"Status Code: {response.status_code}")
    
    # Determine if the request was successful
    is_success = (response.status_code >= 200 and response.status_code < 300) or \
                 (expect_unauthorized and response.status_code == 401)
    status_color = Fore.GREEN if is_success else Fore.RED
    status_text = "✓ SUCCESS" if is_success else "✗ FAILED"
    
    print(f"Status: {status_color}{status_text}{Style.RESET_ALL}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{Fore.CYAN}{'=' * (len(description) + 6)}{Style.RESET_ALL}")
    return is_success

def get_auth_headers(role):
    """Get authentication headers for a specific role"""
    credentials = LOGIN_CREDENTIALS[role]
    response = requests.post(
        f"{BASE_URL}/api/login",
        json=credentials
    )
    access_token = response.json().get('data', {}).get('access_token')
    return {'Authorization': f'Bearer {access_token}'} if access_token else {}

def run_common_tests():
    """Run tests that don't require authentication"""
    test_results = []
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/api/health")
    test_results.append(("Health Check", print_response("Health Check", response)))

    # Test basic endpoints
    response = requests.get(f"{BASE_URL}/api/test")
    test_results.append(("Test GET", print_response("Test GET", response)))

    test_data = {"test": "data"}
    response = requests.post(
        f"{BASE_URL}/api/test",
        json=test_data
    )
    test_results.append(("Test POST", print_response("Test POST", response)))

    # Test unauthorized access
    response = requests.get(f"{BASE_URL}/api/profile")
    is_unauthorized = response.status_code == 401 and "msg" in response.json()
    test_results.append(("Unauthorized Profile Access", print_response("Unauthorized Profile Access", response, expect_unauthorized=True) and is_unauthorized))

    return test_results

def run_auth_tests():
    """Run authentication-related tests"""
    test_results = []
    
    # Test valid logins for each role
    for role, credentials in LOGIN_CREDENTIALS.items():
        response = requests.post(
            f"{BASE_URL}/api/login",
            json=credentials
        )
        test_results.append((f"{role.capitalize()} Login", print_response(f"{role.capitalize()} Login", response)))

    # Test invalid login
    invalid_login_data = {
        "email": "invalid@email.com",
        "password": "wrongpassword"
    }
    response = requests.post(
        f"{BASE_URL}/api/login",
        json=invalid_login_data
    )
    is_invalid_login = response.status_code == 401 and "message" in response.json()
    test_results.append(("Invalid Login", print_response("Invalid Login", response, expect_unauthorized=True) and is_invalid_login))

    return test_results

def run_admin_tests():
    """Run tests specific to admin role"""
    test_results = []
    headers = get_auth_headers("admin")
    
    # Test admin dashboard
    response = requests.get(f"{BASE_URL}/api/admin/dashboard", headers=headers)
    test_results.append(("Admin Dashboard", print_response("Admin Dashboard", response)))
    
    # Test admin profile
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    test_results.append(("Admin Profile", print_response("Admin Profile", response)))
    
    return test_results

def run_professional_tests():
    """Run tests specific to professional role"""
    test_results = []
    headers = get_auth_headers("professional")
    
    # Test professional dashboard
    response = requests.get(f"{BASE_URL}/api/professional/dashboard", headers=headers)
    test_results.append(("Professional Dashboard", print_response("Professional Dashboard", response)))
    
    # Test professional profile
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    test_results.append(("Professional Profile", print_response("Professional Profile", response)))
    
    return test_results

def run_customer_tests():
    """Run tests specific to customer role"""
    test_results = []
    headers = get_auth_headers("customer")
    
    # Test customer dashboard
    response = requests.get(f"{BASE_URL}/api/customer/dashboard", headers=headers)
    test_results.append(("Customer Dashboard", print_response("Customer Dashboard", response)))
    
    # Test customer profile
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    test_results.append(("Customer Profile", print_response("Customer Profile", response)))
    
    return test_results

def run_tests():
    print(f"{Fore.YELLOW}Starting API Tests...{Style.RESET_ALL}\n")
    
    # Run common tests
    test_results = run_common_tests()
    
    # Run authentication tests
    auth_results = run_auth_tests()
    test_results.extend(auth_results)
    
    # Run role-specific tests
    admin_results = run_admin_tests()
    test_results.extend(admin_results)
    
    professional_results = run_professional_tests()
    test_results.extend(professional_results)
    
    customer_results = run_customer_tests()
    test_results.extend(customer_results)

    # Print summary
    print(f"\n{Fore.YELLOW}=== Test Summary ==={Style.RESET_ALL}")
    total_tests = len(test_results)
    successful_tests = sum(1 for _, success in test_results if success)
    failed_tests = total_tests - successful_tests

    print(f"Total Tests: {total_tests}")
    print(f"Successful: {Fore.GREEN}{successful_tests}{Style.RESET_ALL}")
    print(f"Failed: {Fore.RED}{failed_tests}{Style.RESET_ALL}")

    # Print detailed results
    print(f"\n{Fore.YELLOW}=== Detailed Results ==={Style.RESET_ALL}")
    for test_name, success in test_results:
        status_color = Fore.GREEN if success else Fore.RED
        status_text = "✓" if success else "✗"
        print(f"{status_color}{status_text}{Style.RESET_ALL} {test_name}")

if __name__ == "__main__":
    run_tests()