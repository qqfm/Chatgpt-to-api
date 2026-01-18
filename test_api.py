import requests
import json
import time

def test_chatgpt_api():
    url = "http://localhost:8000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello, simply reply with 'Service is working!'"}],
        "stream": False
    }

    print(f"Sending request to {url}...")
    try:
        start_time = time.time()
        response = requests.post(url, headers=headers, json=data, timeout=120) # Long timeout for browser gen
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"\n✅ Success! Response received in {end_time - start_time:.2f}s:")
            print("-" * 50)
            print(content)
            print("-" * 50)
        else:
            print(f"\n❌ API Error: Status {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\n❌ Connection refused. Is the server running?")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")

if __name__ == "__main__":
    test_chatgpt_api()
