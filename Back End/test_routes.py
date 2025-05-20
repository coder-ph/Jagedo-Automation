import requests
import json
from colorama import init, Fore, Style

init()

BASE_URL = "http://localhost:5000"

def print_response(description, response):
    print(f"\n{Fore.CYAN}=== {description} ==={Style.RESET_ALL}")
    print(f"Status Code: {response.status_code}")
    
    # Determine if the request was successful
    is_success = response.status_code >= 200 and response.status_code < 300
    status_color = Fore.GREEN if is_success else Fore.RED
    status_text = "✓ SUCCESS" if is_success else "✗ FAILED"
    
    print(f"Status: {status_color}{status_text}{Style.RESET_ALL}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{Fore.CYAN}{'=' * (len(description) + 6)}{Style.RESET_ALL}")
    return is_success

def run_tests():
    print(f"{Fore.YELLOW}Starting API Tests...{Style.RESET_ALL}\n")
    
    # Track test results
    test_results = []
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/api/health")
    test_results.append(("Health Check", print_response("Health Check", response)))

    # Test login
    login_data = {
        "email": "admin@admin.com",
        "password": "password123"
    }
    response = requests.post(
        f"{BASE_URL}/api/login",
        json=login_data
    )
    test_results.append(("Login", print_response("Login", response)))

    # Store the access token for authenticated requests
    access_token = response.json().get('data', {}).get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}

    # Test profile endpoint (requires authentication)
    response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
    test_results.append(("Profile", print_response("Profile", response)))

    # Test admin dashboard (requires admin role)
    response = requests.get(f"{BASE_URL}/api/admin/dashboard", headers=headers)
    test_results.append(("Admin Dashboard", print_response("Admin Dashboard", response)))

    # Test professional dashboard (requires professional role)
    response = requests.get(f"{BASE_URL}/api/professional/dashboard", headers=headers)
    test_results.append(("Professional Dashboard", print_response("Professional Dashboard", response)))

    # Test customer dashboard (requires customer role)
    response = requests.get(f"{BASE_URL}/api/customer/dashboard", headers=headers)
    test_results.append(("Customer Dashboard", print_response("Customer Dashboard", response)))

    # Test basic endpoints
    response = requests.get(f"{BASE_URL}/api/test")
    test_results.append(("Test GET", print_response("Test GET", response)))

    test_data = {"test": "data"}
    response = requests.post(
        f"{BASE_URL}/api/test",
        json=test_data
    )
    test_results.append(("Test POST", print_response("Test POST", response)))

    # Test error handling with invalid data
    invalid_login_data = {
        "email": "invalid@email.com",
        "password": "wrongpassword"
    }
    response = requests.post(
        f"{BASE_URL}/api/login",
        json=invalid_login_data
    )
    test_results.append(("Invalid Login", print_response("Invalid Login", response)))

    # Test unauthorized access
    response = requests.get(f"{BASE_URL}/api/profile")
    test_results.append(("Unauthorized Profile Access", print_response("Unauthorized Profile Access", response)))

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