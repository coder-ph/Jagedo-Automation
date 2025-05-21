import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the API
BASE_URL = 'http://localhost:5001/api'

def login(email, password):
    """Login and return the JWT token"""
    response = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()['data']['access_token']
    else:
        print(f"Login failed: {response.text}")
        return None

def select_winning_bid(job_id, token):
    """Select the winning bid for a job"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # First, get the bid scores to see the ranking
    response = requests.get(
        f"{BASE_URL}/projects/{job_id}/bid-scores",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"Failed to get bid scores: {response.text}")
        return None
    
    bid_scores = response.json()
    print("\n=== Bid Scores ===")
    print(json.dumps(bid_scores, indent=2))
    
    # Now select the winning bid
    response = requests.post(
        f"{BASE_URL}/projects/{job_id}/select-winner",
        headers=headers,
        json={}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n=== Winning Bid Selected ===")
        print(json.dumps(result, indent=2))
        return result
    else:
        print(f"Failed to select winning bid: {response.text}")
        return None

if __name__ == "__main__":
    import sys
    
    # Check if job ID is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python test_bid_selection.py <job_id>")
        sys.exit(1)
        
    job_id = sys.argv[1]
    
    # Get admin credentials from environment variables
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    
    if not admin_email or not admin_password:
        print("Please set ADMIN_EMAIL and ADMIN_PASSWORD in .env file")
        sys.exit(1)
    
    # Login as admin
    print(f"Logging in as {admin_email}...")
    token = login(admin_email, admin_password)
    if not token:
        print("Login failed. Exiting...")
        sys.exit(1)
    
    print(f"\nSelecting winning bid for job ID: {job_id}")
    # Select winning bid
    select_winning_bid(job_id, token)
