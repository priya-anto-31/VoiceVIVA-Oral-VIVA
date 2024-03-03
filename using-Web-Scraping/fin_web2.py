import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

r = sr.Recognizer()
r.dynamic_energy_threshold = False

def send_message(text):
    # Function to display the question on the screen (replace with your implementation)
    print("Question:", text)

def scrape_specific_text(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extracting text from all <h3> tags inside an <article> tag
        article_tag = soup.find('article')  # Adjust the tag based on your website's HTML
        
        # Check if the 'article' tag is found
        if article_tag:
            h3_tags = article_tag.find_all('h3')
            
            # Check if there are any <h3> tags inside the 'article' tag
            if h3_tags:
                questions = [specific_h3_tag.get_text().strip() for specific_h3_tag in h3_tags]
                return questions
            else:
                print("No <h3> tags found inside 'article' tag.")
        else:
            print("Element 'article' not found on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def record_text():
    try:
        with sr.Microphone() as source:
            print("Answer Now...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10)  # Set a timeout of 10 seconds
            text = r.recognize_google(audio)
            print("Answer:", text)
            return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Time limit exceeded")

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")
    print("Next Question:")

def main():
    url = 'https://www.simplilearn.com/data-structure-interview-questions-and-answers-article'
    questions = scrape_specific_text(url)
    
    if questions:
        for question in questions:
            send_message(question)
            answer = record_text()
            if answer:
                output_text(answer)
            
            # Ask if the user wants to answer the next question
            next_question = input("Do you want to answer the next question? (yes/no): ")
            if next_question.lower() != 'yes':
                break  # Exit loop if user doesn't want to answer the next question

if __name__ == "__main__":
    main()