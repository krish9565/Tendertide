from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

def get_product_details(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    service = Service("C:\\chromedriver\\chromedriver")  # Update with correct path
    driver = webdriver.Chrome()#service=service, options=options)
    
    try:
        driver.get(url)
        
       
        try:
            product_name = driver.find_element(By.CSS_SELECTOR, "#pdp-item-title > div > div.MuiBox-root.pdp-css-176py26 > div.pdp-css-6a2w33 > h1").text.strip()
        except:
            product_name = "N/A"
        
        # Extracting price
        try:
            price = driver.find_element(By.CSS_SELECTOR, "#pdp-item-title > div > div.MuiBox-root.pdp-css-176py26 > div.pdp-css-25gq7h > div > span").text.strip()
        except:
            price = "N/A"
        
        # Extracting available variants
        color_variants=[]
        colors=driver.find_elements(By.CSS_SELECTOR, "#pdp-description-form > div.pdp-css-5e8q5w > div:nth-child(1) > div.pdp-css-ss1udt > div > button > img")
        for color in colors:
            color=color.get_attribute('title')
            color_variants.append(color)
        
        design_variant=[]
        designs=driver.find_elements(By.CSS_SELECTOR, "#pdp-page-layout > div.MuiGrid2-root.MuiGrid2-container.MuiGrid2-direction-xs-row.pdp-css-1d54pdp > div:nth-child(2) > div > div:nth-child(1) > div > div > div")
        for design in designs:
            design=design.find_element(By.CSS_SELECTOR,"a").text.strip()
            design_variant.append(design)
        
        
        product_data = {
            "product_name": product_name,
            "price": price,
            "color_cariant": color_variants,
            "design_variant":design_variant
        }
        
        return product_data
    
    finally:
        driver.quit()

if __name__ == "__main__":
    product_url = "https://www.next.co.uk/style/st443901/c15109"
    product_info = get_product_details(product_url)
    print(json.dumps(product_info, indent=4))
