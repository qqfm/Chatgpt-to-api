import requests
import time

def verify():
    url = "http://localhost:8000/v1/chat/completions"
    print(f"Testing connectivity to {url}...")
    
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "1+1=?"}]
    }
    
    print("Sending POST request (expecting quick response)...")
    try:
        start = time.time()
        # Set a shorter timeout first to fail fast if connection is dead, 
        # but long enough for a short answer
        # Increased to 90s to cover browser overhead
        response = requests.post(url, json=payload, timeout=90) 
        duration = time.time() - start
        
        print(f"Request finished in {duration:.2f} seconds.")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Reference Response:")
            print(data)
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"\nAnswer content: {content}")
            print("\n✅ Service is WORKING properly.")
        else:
            print("❌ Service returned an error.")
            print(response.text)

    except requests.exceptions.Timeout:
        print("❌ Request timed out (>45s). The browser might be stuck waiting for the 'Send' button to reappear.")
    except Exception as e:
        print(f"❌ Error during request: {e}")

if __name__ == "__main__":
    verify()
