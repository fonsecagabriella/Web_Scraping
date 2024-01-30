import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import os


def main():
    # Set URL to scrap
    url = "https://www.vegansociety.com/news/news"

    #print the return
    #print(scrape_website(url))

    data = scrape_website(url)

    # find all the sections with specifid class name
    # the attributes below will depend on the page you're scraping
    cards_data = data.find_all("div", attrs={"class", "views-row"} )

    #print total number of cards
    print("Total cards found: ", len(cards_data))

    # save cards to csv file
    save_cards_csv(cards_data)

    # save images from cards
    save_images_cards(cards_data)




def save_cards_csv(soup):
    scraped_data = []

    for card in soup:
        # initialise the dictionary to save the data
        news_item = {}

        # retrieve title and date published and save in the dictionary
        news_item["news_title"] = card.find("h2", attrs={"class", "block-list__title"}).text
        news_item["news_published"] = card.find("span", attrs={"class", "date-display-single"}).text

        scraped_data.append(news_item)

    # create a data frame from the list of dictionaries
    df = pd.DataFrame.from_dict(scraped_data)

    # save the scraped data as CSV file
    try:
        df.to_csv("vegan_news.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
        print("File saved sucessfully")
    except Exception:
        print("There was a problem saving your file")

def save_images_cards(soup):
    images = []
    
    #find all the images in the soup
    for card in soup:

        image = {}

        image["image_desc"] = card.find("img", src=True)["alt"]
        image["image_src"] = card.find("img", src=True)["src"]

        images.append(image)

    print ("You have a total of ", len(images), " images.")

    # temp_count to save the image name
    temp_count = 1

    # Ensure that the "img" folder exists
    if not os.path.exists("scraped_images"):
        os.makedirs("scraped_images")

    for img in images:

        #create file name for the image to be scraped and save
        file_name = "img_card_"+str(temp_count)+".jpg"

        # create file path within the scraped_images folder
        file_path = os.path.join("scraped_images", file_name)

        with open(file_path, "wb") as file:
            res = requests.get(img["image_src"])
            file.write(res.content)

        print(f"Image saved: {file_path}")

        # increase the temp count
        temp_count += 1

def scrape_website(url):
    # Define headers
    # this can avoid issues with some websites such as being blocked by security measures or firewalls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Make a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def find_links(soup):
    # Extract information by navigating the HTML structure
    # For example, find all the links on the page
    links = soup.find_all('a')

    # Print the extracted information
    for link in links:
        print(link.get('href'))


if __name__ == "__main__":
    main()