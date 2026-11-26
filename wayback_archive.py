import requests

url = "https://peisctehran.com/index.php/gallery/"

response = requests.get(url, timeout=30)

print("HTTP status:", response.status_code)

print("\nResponse headers:")
for key, value in response.headers.items():
    print(f"{key}: {value}")

if response.status_code == 429:
    print("\nRate limit exceeded.")
    print("Retry-After:", response.headers.get("Retry-After"))
    print(response.text)
