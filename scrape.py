from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

class ScrapeZara:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.menWearsDetails = []
        self.womenWearsDetails = []

    def scrapeWears(self, website):
        self.driver.get(website)

        wearsLinks = self.driver.find_elements(By.XPATH, "//div/a[@class='product-link _item product-grid-product-info__name link']")
        hrefs = [wearsHref.get_attribute("href") for wearsHref in wearsLinks]
        
        details = []
        
        for href in hrefs:
            self.driver.get(href)
            try:
                # itemID = self.driver.find_element(By.XPATH, "//div[@class='product-detail-info__actions']").text.split("|")[1].strip()
                # itemColor = self.driver.find_element(By.XPATH, "//div[@class='product-detail-info__actions']").text.split("|")[0].replace("Color: ", "").strip()
                items = self.driver.find_element(By.XPATH, "//div[@class='product-detail-info__header-content']/h1").text
                wearDescription = self.driver.find_element(By.XPATH, "//div[@class='expandable-text__inner-content']/p").text
                PercentageDiscount = self.driver.find_element(By.XPATH, "//span[@class='price-current__discount-percentage']").text
                realPrice = self.driver.find_element(By.XPATH, "//span[@class='price-old__amount price__amount price__amount-old']/div").text
                itemPrice = self.driver.find_element(By.XPATH, "//span[@class='price-current__amount']/div").text
                
                imgElements = self.driver.find_elements(By.XPATH, "//img[@class='media-image__image media__wrapper--media']")
                images = [img.get_attribute("src") for img in imgElements if not img.get_attribute("src").lower().endswith(".png")]
                
                allWears = {
                    "Items": items, "Description": wearDescription,
                    "Real Price": realPrice, "% Discount": PercentageDiscount, 
                    "Discounted Price": itemPrice, "Images": images
                }
                details.append(allWears)
            except NoSuchElementException as e:
                print(f"Error scraping {href}: {e}")
        
        return pd.DataFrame(details)

    def zaraWomenWears(self, website):
        self.womenWearsDetails = self.scrapeWears(website)
        return self.womenWearsDetails

    def zaraMenWears(self, website):
        self.menWearsDetails = self.scrapeWears(website)
        return self.menWearsDetails
        
    def concatenateWears(self, men_url, women_url):
        menWears = self.zaraMenWears(men_url)
        womenWears = self.zaraWomenWears(women_url)
        
        combinedWears = pd.concat([menWears, womenWears], ignore_index=True, axis=0)
        combinedWears.to_csv("zara_wears.csv", index=False)
        
        return combinedWears
    
    def close(self):
        self.driver.quit()

# URLs
womenWears = "https://www.zara.com/us/en/woman-dresses-l1066.html?v1=2417457"
menWears = "https://www.zara.com/us/en/man-sale-l7139.html?v1=2439352"

# Create a scraper instance
scraper = ScrapeZara()

# Scrape and print results
# women_results = scraper.zaraWomenWears(womenWears)
# print(women_results)

# men_results = scraper.zaraMenWears(menWears)
# print(men_results)

# Concatenate and save results
all_wears = scraper.concatenateWears(menWears, womenWears)
print(all_wears)

# Close the scraper
scraper.close()
