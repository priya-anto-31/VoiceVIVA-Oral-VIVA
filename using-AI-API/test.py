import requests
import speech_recognition as sr

api_key = 'AIzaSyAusVq_0b5B8laeNp_qDn3O2s59EnlnlQU'
api_key2 = 'AIzaSyCQNaWx9gQfHY1jK0avBb-ZbXhxLTz5CJM'
api_secret = 'AIzaSyAusVq_0b5B8laeNp_qDn3O2s59EnlnlQU'

# Define the base URL for Gemini API
base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key2

def make_gemini_request(prompt, method='POST'):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    url = base_url
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def ask_question_and_evaluate():
    try:
        while True:
            # Gemini asks a question
            question = make_gemini_request("Ask a question about data structures.")
        
            if not question or 'candidates' not in question:
                print("Error: Unable to generate question.")
                
            try:
                question_text = question['candidates'][0]['content']['parts'][0]['text']
            except IndexError:
    # Handle the case where the second element doesn't exist
                print("Error: Unable to access question text. Response structure might have changed.")
            print("Gemini Question:")
            print(question_text)

            # Get user's answer through voice input
            user_answer = record_text()
            print("Your Answer:", user_answer)

            # Evaluate the user's answer
            evaluation_response = make_gemini_request(f"Evaluate the following answer: {user_answer} for the question: {question}. Make a short response")
            evaluation_score = make_gemini_request(f"Generate a score for the following answer: {user_answer} for the question: {question}")
            if not evaluation_response or 'candidates' not in evaluation_response:
                print("Error: Unable to evaluate answer.")
                continue
            if not evaluation_score or 'candidates' not in evaluation_score:
                print("Error: Unable to evaluate answer.")
                continue

            score = evaluation_score['candidates'][0]['content']['parts'][0]['text']
            feedback = evaluation_response['candidates'][0]['content']['parts'][0]['text']
            print(f"Gemini Feedback:  {feedback},\n Score: {score}")

            # Ask if the user wants to continue
            continue_input = input("Do you want to ask another question? (y/n): ")
            if continue_input.lower() != 'y':
                break

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")

# Function to record user's voice input and convert it to text
def record_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Answer now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service.")
            return ""

# Call the function to start asking questions and evaluating answers
ask_question_and_evaluate()
