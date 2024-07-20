from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def get_video_links(channel_url):
    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for no GUI
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    driver.get(channel_url)
    
    # Scroll to bottom of page to load all videos
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        driver.implicitly_wait(3)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Get page source after scrolling
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Close driver
    driver.quit()
    
    video_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/watch?v=' in href:
            full_link = f"https://www.youtube.com{href}"
            if full_link not in video_links:
                video_links.append(full_link)
    
    return video_links

# Example usage
channel_url = "https://www.youtube.com/@youtubechannel/videos"
video_links = get_video_links(channel_url)

for link in video_links:
    print(link)