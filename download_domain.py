# Basic script to crawl a url and download all it's assets. 

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, unquote

def download_website(url, output_directory, visited_urls=set()):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor and img tags
        anchor_tags = soup.find_all('a')
        img_tags = soup.find_all('img')

        # Combine anchor and img tags into a single list
        tags = anchor_tags + img_tags

        for tag in tags:
            # Check if the tag is an anchor or img tag
            if tag.name == 'a':
                href = tag.get('href')
            elif tag.name == 'img':
                href = tag.get('src')

            if href:
                # Construct the absolute URL
                absolute_url = urljoin(url, href)

                # Parse the absolute URL
                parsed_url = urlparse(absolute_url)

                # Download the file if it belongs to the same domain and hasn't been visited
                if parsed_url.netloc == urlparse(url).netloc and absolute_url not in visited_urls:
                    visited_urls.add(absolute_url)

                    # Get the relative path from the URL
                    relative_path = unquote(parsed_url.path)
                    if relative_path.endswith('/'):
                        relative_path += 'index.html'

                    # Construct the output file path
                    output_path = os.path.join(output_directory, relative_path[1:])

                    # Create the directory for the file if it doesn't exist
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    # Download the file content
                    file_response = requests.get(absolute_url)
                    if file_response.status_code == 200:
                        file_content = file_response.content

                        # Save the file content to a file
                        with open(output_path, 'wb') as file:
                            file.write(file_content)

                        print(f"Downloaded: {absolute_url} => {output_path}")

                        # Recursively crawl and download pages
                        if output_path.endswith(('.html', '.htm')):
                            if website_url in absolute_url:
                                try:.intro
                                    download_website(absolute_url, output_directory, visited_urls)
                                except:
                                    print("Failed to download: ", absolute_url)
    else:
        print(f"Failed to retrieve the website: {url}")


# Specify the URL of the website to crawl and download
website_url = "https://waltergordy.com"

# Specify the output directory to save the downloaded files
output_directory = "./waltergordy/"

# Call the function to crawl and download the website
download_website(website_url, output_directory)
