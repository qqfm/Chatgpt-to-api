import requests
import os
import time

def test_car_review():
    url = "http://localhost:8000/v1/chat/completions"
    
    # Prepare absolute paths for the images - utilizing the real PNG files
    cwd = os.getcwd() # Should be d:\webgpt
    images = [
        os.path.join(cwd, "car1.PNG"),
        os.path.join(cwd, "car2.PNG"),
        os.path.join(cwd, "car3.PNG"),
        os.path.join(cwd, "car4.PNG")
    ]
    
    # Verify files exist
    for img in images:
        if not os.path.exists(img):
            print(f"❌ Error: Image not found: {img}")
            return

    prompt_text = """
    Please analyze these images of a 2016 Toyota Prius C and the following description:
    
    2016 Toyota Prius C
    US$ 12,500
    2016 Toyota Prius C — 89K Miles — Clean Title — CarPlay + Backup Camera
    
    Is this a good deal? What are the pros and cons based on the visible condition and description?
    """
    
    # Construct OpenAI-compatible multimodal message
    content = [{"type": "text", "text": prompt_text}]
    for img_path in images:
        content.append({
            "type": "image_url", 
            "image_url": {"url": f"file://{img_path}"} # Sending local path file scheme
        })

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [{"role": "user", "content": content}]
    }
    
    print("-" * 50)
    print("Sending Car Review Request with 4 images...")
    print(f"Images: {images}")
    print("-" * 50)
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=240) # Long timeout for uploading images and analysis
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis Result (Time: {duration:.2f}s):")
            print("-" * 50)
            content = result['choices'][0]['message']['content']
            print(content)
            print("-" * 50)
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_car_review()
