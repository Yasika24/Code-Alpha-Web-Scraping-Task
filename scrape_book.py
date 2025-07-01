import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
all_books = []

for page_num in range(1, 6):
    print(f"Scraping page {page_num}...")
    url = base_url.format(page_num)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        title = book.h3.a['title']

        # Fix encoding issue in price
        price_text = book.find('p', class_='price_color').text
        price_clean = price_text.encode('ascii', 'ignore').decode().replace('£', '').strip()

        availability = book.find('p', class_='instock availability').text.strip()

        all_books.append({
            'Title': title,
            'Price (£)': float(price_clean),
            'Availability': availability
        })

    time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_books)
df.to_csv('books_data.csv', index=False)

print("Scraping completed. Data saved to 'books_data.csv'.")
