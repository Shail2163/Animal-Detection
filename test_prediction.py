import requests
import json

def test_prediction():
    # Path to the image
    image_path = "backend/storage/uploads/hel.webp"

    # API endpoint
    url = "http://localhost:8000/predict"

    try:
        # Open the image file
        with open(image_path, 'rb') as f:
            # Create the files dictionary for multipart form data
            files = {'file': ('hel.webp', f, 'image/webp')}

            # Make the POST request
            response = requests.post(url, files=files)

            # Print the response
            print("Status Code:", response.status_code)
            print("Response:", response.json())

    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prediction()
