import requests
import json

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000"
TEST_QUESTION = "What is the primary protocol for the G2 glasses?"

def main():
    """
    Sends a hardcoded test query to the backend's /query endpoint
    and prints the formatted JSON response.
    """
    print("--- Shadow OS Brain Test ---")
    print(f"Sending query to backend at: {BACKEND_URL}")
    print(f"Test Question: '{TEST_QUESTION}'")
    
    try:
        # The request body must match the Pydantic model in the backend.
        payload = {"question": TEST_QUESTION}
        
        # Send the POST request to the /query endpoint.
        response = requests.post(f"{BACKEND_URL}/query/", json=payload)
        
        # Check for a successful response.
        if response.status_code == 200:
            print("\n--- [SUCCESS] ---")
            # Pretty-print the JSON response from the backend.
            response_data = response.json()
            print(json.dumps(response_data, indent=2))
        else:
            print(f"\n--- [ERROR] ---")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("\n--- [CONNECTION ERROR] ---")
        print("Could not connect to the backend. Is it running?")
        print("Start the backend with: uvicorn backend.main:app --reload")
    except Exception as e:
        print(f"\n--- [UNEXPECTED ERROR] ---")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

