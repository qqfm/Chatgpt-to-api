import requests
import json
import time

def complex_test():
    url = "http://localhost:8000/v1/chat/completions"
    print(f"Testing connectivity to {url} with a complex prompt...")
    
    prompt = "Please write a short haiku about coding in Python, and then explain it briefly."
    
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    print(f"Sending prompt: '{prompt}'")
    print("This might take a while due to generation speed...")
    
    try:
        start = time.time()
        # Complex answers take longer, so we use a generous timeout
        response = requests.post(url, json=payload, timeout=180) 
        duration = time.time() - start
        
        print(f"Request finished in {duration:.2f} seconds.")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print("\n" + "="*50)
            print("🤖 ChatGPT Response:")
            print("="*50)
            print(content)
            print("="*50)
        else:
            print("❌ Service returned an error.")
            print(response.text)

    except requests.exceptions.Timeout:
        print("❌ Request timed out (>180s).")
    except Exception as e:
        print(f"❌ Error during request: {e}")

if __name__ == "__main__":
    complex_test()
