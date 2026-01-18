import requests
import time

def test_remote_server():
    # Target IP provided by the user
    target_ip = "192.168.254.208"
    port = "8000"
    url = f"http://{target_ip}:{port}/v1/chat/completions"
    
    print(f"Testing remote connection to: {url}")
    
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello! Are you working remotely?"}]
    }
    
    try:
        start_time = time.time()
        print("Sending request... (Timeout 10s for connection check)")
        
        # Short timeout for connection, but execution might take longer. 
        # If we connect but it hangs, that means the server is UP but busy/slow.
        # If we time out immediately or get Connection Refused, it's a network/firewall issue.
        response = requests.post(url, json=payload, timeout=60)
        
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"\n✅ Connection SUCCESSFUL! (Time: {duration:.2f}s)")
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print("-" * 50)
            print("Response from server:")
            print(content)
            print("-" * 50)
        else:
            print(f"\n❌ Server reachable, but returned error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Connection Refused or Host Unreachable.")
        print("Possible causes:")
        print("1. The service is not running on the remote machine.")
        print("2. The IP address is incorrect.")
        print("3. Windows Firewall (or other firewall) on 192.168.254.208 is blocking port 8000.")
        print("   (Try running 'New-NetFirewallRule -DisplayName \"WebGPT\" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow' on the remote machine)")
    except requests.exceptions.Timeout:
        print("\n❌ Request Timed Out.")
        print("Server might be running but hanged, or network is extremely slow.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_remote_server()
