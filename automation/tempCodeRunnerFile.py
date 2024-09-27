import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Load environment variables from a specific file
load_dotenv('api.env')

# Fetch environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
linkedin_email = os.getenv('LINKEDIN_EMAIL')
linkedin_password = os.getenv('LINKEDIN_PASSWORD')

# Debugging: Print environment variables to verify they are loaded correctly
print("OpenAI API Key:", openai_api_key)
print("LinkedIn Email:", linkedin_email)
print("LinkedIn Password:", linkedin_password)

# Verify if environment variables are loaded
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")
if not linkedin_email:
    raise ValueError("LinkedIn email not found. Please set it in the .env file.")
if not linkedin_password:
    raise ValueError("LinkedIn password not found. Please set it in the .env file.")

# Set OpenAI API key
openai.api_key = openai_api_keyf generate_post_prompt(topic):
    try:z
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a LinkedIn post about {topic}."}
            ]
        )
        post_content = response.choices[0].message['content'].strip()
        print(f"Generated Post Content: {post_content}")  # Debugging: Print the generated post content
        return post_content
    except Exception as e:
        print(f"An error occurred while generating the post content: {str(e)}")
        return None

def linkedin_login_and_post(email, password, topic):
    try:
        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        # Uncomment the following line to run in headless mode
        # options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("Chrome driver initialized.")

        # Open LinkedIn
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        print("Navigated to LinkedIn login page.")

        # Find and fill the email field
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)
        print("Email entered.")

        # Find and fill the password field
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        print("Password entered.")

        # Submit the login form
        password_field.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.share-box-feed-entry__trigger')))
        print("Login form submitted.")

        # Navigate to LinkedIn home page
        driver.get("https://www.linkedin.com/feed/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.share-box-feed-entry__trigger')))
        print("Navigated to LinkedIn feed.")

        # Click on the start post button
        start_post_button = driver.find_element(By.CSS_SELECTOR, 'button.share-box-feed-entry__trigger')
        start_post_button.click()
        print("Clicked on start post button.")

        # Wait until the post text area is visible
        post_text_area = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ql-editor')))
        print("Post text area is visible.")

        # Generate post content using AI
        post_content = generate_post_prompt(topic)
        if post_content:
            print(f"Generated Post Content: {post_content}")

            # Find the text area and enter the post content
            post_text_area.click()
            post_text_area.send_keys(post_content)
            print("Entered post content.")

            # Click on the post button
            post_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-control-name="sharebox_footer_share_button"]')))
            post_button.click()
            print("Clicked on post button.")

            # Wait for the post to be submitted
            time.sleep(5)
            print("Post submitted successfully!")
        else:
            print("Failed to generate post content. Aborting post submission.")

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        # Close the browser
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    # Ensure the .env file contains your API key and LinkedIn credentials
    email = linkedin_email
    password = linkedin_password
    topic = "the benefits of using AI in business"

    linkedin_login_and_post(email, password, topic)
  