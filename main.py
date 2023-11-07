import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

# Read the data from the CSV
df = pd.read_csv('Data/Input.xlsx - Sheet1.csv')

# Store the URL_IDs and URLs
col1 = "URL_ID"
col2 = "URL"
urlIDs = df[col1].tolist()
urls = df[col2].tolist()

# Function is everytime we have to get the content
def process_tag_contents(tag):
    if isinstance(tag, str):
        return tag.strip()
    else:
        paragraph_text = ""
        for child in tag.contents:
            if isinstance(child, str):
                paragraph_text += child
            elif child.name in {'strong', 'em', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'u'}:
                # Recursively process contents of specified tags
                paragraph_text += process_tag_contents(child)
            elif child.name == 'ul':
                for li_tag in child.find_all('li'):
                    paragraph_text += f"- {li_tag.get_text()}\n"
            elif child.name == 'img':
                # Skip processing of img tags
                pass
            else:
                paragraph_text += str(child)
        return paragraph_text.strip()


i = 0
for url in urls:
    paragraphs = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    t = soup.title.string
    title = t[:-23]
    print(title)


    # Check if the element with class "td-post-content tagdiv-type" exists
    element1 = soup.find(class_="td-post-content tagdiv-type")
    if element1:
        for tag in element1.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            paragraph_text = process_tag_contents(tag)
            paragraphs.append(paragraph_text)
            # Process any ul/li tags inside specified tags
            for ul_tag in tag.find_all('ul'):
                for li_tag in ul_tag.find_all('li'):
                    paragraph_text += f"- {li_tag.get_text()}\n"
                    paragraphs.append(paragraph_text)
    else:
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for tag in tags:
            paragraph_text = process_tag_contents(tag)
            paragraphs.append(paragraph_text)
            # Process any ul/li tags inside specified tags
            for ul_tag in tag.find_all('ul'):
                for li_tag in ul_tag.find_all('li'):
                    paragraph_text += f"- {li_tag.get_text()}\n"
                    paragraphs.append(paragraph_text)




    file_number = urlIDs[i]
    file_path = r'Data\Articles\{}.txt'.format(file_number)

    # with open("track.csv", mode="w") as csvfile:333
    #     fieldnames = ["URL_ID", "URL"]
    #     writer = csv.DictWriter(csvfile, fieldnames)
    #     writer.writeheader()
    #     writer.writerow({"URL_ID": file_number, "URL": url})

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(title)
        f.write("\n\n")

    for paragraph in paragraphs:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(paragraph)
            f.write("\n\n")
    i+=1
    print(i, " URL Done ")
