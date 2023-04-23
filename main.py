import requests, os, yaml
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Read the configuration from the YAML file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

with open("result.yaml", "r") as f:
    result = yaml.safe_load(f)

# Extract the list of URLs and class names from the configuration
urls = config["urls"]
places = config["places"]

change = True

# Loop over the list of URLs and class names
for url, place in zip(urls, places):
    # Send a GET request to the URL and get the HTML response
    response = requests.get(url)

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div with the specified class name
    div = soup.find("div", {"class": "next_available"})

    # Extract the text content of the div
    text = div.get_text()
    new_text = " ".join(text.strip().split(' ')[-4:])

    # Print old result
    old = result[place]
    if new_text != old:
        result[place] = new_text
        change = True

    # Print the extracted text
    print(f"Place: {place} Service date: {new_text}")

output = ""
for key in result:
    output += f"{key}: {result[key]}\n"

if change:
    # Set the webhook URL and message payload
    webhook_url = os.environ.get('MATTERMOST_URL')
    webhook_url = 'https://mattermost.rodvand.net/hooks/pmezdxc5s3ywdq3ite6gh6p5yw'
    message_payload = {"channel": "@rodvand", "text": f"{output}"}

    # Send the message using a POST request to the webhook URL
    response = requests.post(webhook_url, json=message_payload)

    # Check the response status code
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message: {response.text}")

    with open("result.yaml", "w") as f:
        yaml.safe_dump(result, f)