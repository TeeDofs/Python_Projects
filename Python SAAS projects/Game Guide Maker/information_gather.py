import requests
from bs4 import BeautifulSoup
import time
import re
import os
import spacy
import openai
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv() #Load the .env file

openai.api_key = os.getenv('OPEN_AI_API_KEY')

class Book:
    def __init__(self, title, chapterNumber, voiceId, url):
        self.title = title
        self.chapterNumber = chapterNumber
        self.voiceId = voiceId
        self.url = url

my_vampire_system = Book(
    "My Vampire System", 
    2000, 
    "Joanna", 
    "https://bednovel.com/bednovel/my-vampire-system-37069/ch{}"
)
currentBook = my_vampire_system
nlp = spacy.load("en_core_web_sm")
sentiment_analyzer = pipeline("sentiment-analysis")


def sanitize_filename(filename):
    # Sanitize filenames by removing or replacing problematic characters.
    invalid_chars = ['?', ':', '\\', '/', '>', '<', '*', '|', '"']
    for char in invalid_chars:
        filename = filename.replace(char, "")
    return filename

def clean_text(text):
    # Define a pattern to match variations of "bednovel.com", "bednovel.org", etc.
    pattern = re.compile(r'\bbednovel\.\w+\b', re.IGNORECASE)
    # Replace found occurrences with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def scrape_chapter(chapter_number):
    # Access the webpage
    url = currentBook.url.format(chapter_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the book title
    book_title_tag = soup.find("h1", class_="tit")
    book_title = book_title_tag.a["title"] if book_title_tag and book_title_tag.a else "Unknown Book"

    # Extract the chapter title
    chapter_title_tag = soup.find("span", class_="chapter")
    chapter_title = chapter_title_tag.get_text() if chapter_title_tag else f"Chapter {chapter_number}"

    # Extract chapter content
    chapter_content = soup.find('div', id='article')
    # Check if the chapter content was found
    if chapter_content is None:
        return None, book_title, chapter_title

    # Extract the paragraphs from the chapter content
    chapter_text = ""
    for paragraph in chapter_content.find_all('p'):
        chapter_text += paragraph.get_text() + '\n'

    # Remove potential unwanted text
    unwanted_promo = "Visit bednovel.com for the best novel reading experience"
    chapter_text = chapter_text.replace(unwanted_promo, "")
    chapter_text = clean_text(chapter_text)

    return chapter_text, book_title, chapter_title

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

def scrape_and_save_chapter(chapter_number):
    chapter_text, book_title, chapter_title = scrape_chapter(chapter_number)
    chapter_title = sanitize_filename(chapter_title) # Use sanitized chapter title

    book_title_clean = sanitize_filename(book_title)  # Clean the title to make it a valid folder name
    chapter_title_clean = sanitize_filename(chapter_title)
     # Get the directory of the current script
    script_folder = os.path.dirname(os.path.abspath(__file__))
    game_ideas_directory = os.path.join(script_folder, "Game Ideas")
    
    # Create paths for book and chapter inside the script's directory
    base_path = os.path.join(game_ideas_directory, book_title_clean, chapter_title_clean)
    
    # Create necessary directories
    os.makedirs(base_path, exist_ok=True)  
    
    # Save the chapter text to a file inside the chapter's directory
    chapter_filename = os.path.join(base_path, f"chapter_{chapter_number}_text.txt")
    save_to_file(chapter_filename, chapter_text)
    
    return chapter_text, book_title_clean, chapter_title_clean


def extract_information(text, book_title, chapter_title, chapter_number):
    
    # NLP processing to extract characters, locations, objects, and emotions
    doc = nlp(text)
    characters = []
    locations = []
    objects = []
    emotions = []
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            characters.append(ent.text)
        elif ent.label_ in ["LOC", "GPE"]:
            locations.append(ent.text)
    
    for token in doc:
        if "obj" in token.dep_:
            objects.append(token.text)
    
    sentences = [sent.text for sent in doc.sents]
    for sentence in sentences:
        response = openai.Completion.create(
            model="text-davinci-003",  # You can replace this with the appropriate model
            prompt=f"Analyze the following sentence for emotions: {sentence}",
            max_tokens=100  # Adjust as necessary
        )
        emotion = response.choices[0].text.strip()
        if emotion:
            emotions.append((sentence, emotion))

    # Call OpenAI's API to generate an image prompt based on the chapter text
    response = openai.Completion.create(
        model="text-davinci-003",  # You can replace this with the appropriate model
        prompt=f"Generate an image prompt based on the following text from a book chapter:\n{text}",
        max_tokens=100  # Adjust as necessary
    )
    
    image_prompt = response.choices[0].text.strip()
    
    # Save the generated prompt to a file
    script_folder = os.path.dirname(os.path.abspath(__file__))
    game_ideas_directory = os.path.join(script_folder, "Game Ideas")
    base_path = os.path.join(game_ideas_directory, book_title, chapter_title)
    os.makedirs(base_path, exist_ok=True)
    
    filename = os.path.join(base_path, f"generated_prompt_chapter_{chapter_number}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(image_prompt)
    
    extracted_info = {
        "characters": list(set(characters)),
        "locations": list(set(locations)),
        "emotions": emotions,
        "objects": list(set(objects))
    }
    
    return image_prompt, extracted_info

def generate_prompts(info, book_title, chapter_title, chapter_number):
    prompts = []
    
    # Generate prompts based on characters and emotions
    for character in info["characters"]:
        for emotion in info["emotions"]:
            prompts.append(f"Generate an image of {character} from {book_title}, {chapter_title}, feeling {emotion[1]} in the scene where they are {emotion[0]}.")
            
            # Adding location to the prompt if available
            if info["locations"]:
                for location in info["locations"]:
                    prompts.append(f"Generate an image of {character} from {book_title}, {chapter_title}, feeling {emotion[1]} in {location} where they are {emotion[0]}.")
                    
            # Adding objects to the prompt if available
            if info["objects"]:
                for obj in info["objects"]:
                    prompts.append(f"Generate an image of {character} from {book_title}, {chapter_title}, feeling {emotion[1]}, interacting with {obj} in the scene where they are {emotion[0]}.")
            
    # Generate prompts based on locations and objects
    for location in info["locations"]:
        for obj in info["objects"]:
            prompts.append(f"Generate an image of {location} from {book_title}, {chapter_title}, showcasing {obj}.")
    
    # Generate prompts based on objects
    for obj in info["objects"]:
        prompts.append(f"Generate an image of {obj} from {book_title}, {chapter_title}.")
        
    # Ensure all prompts are unique
    prompts = list(set(prompts))
    
    return prompts

def save_prompts_to_file(prompts, book_title, chapter_title, chapter_number):
    script_folder = os.path.dirname(os.path.abspath(__file__))
    game_ideas_directory = os.path.join(script_folder, "Game Ideas")
    base_path = os.path.join(game_ideas_directory, book_title, chapter_title)
    os.makedirs(base_path, exist_ok=True)
    
    filename = os.path.join(base_path, f"prompts_chapter_{chapter_number}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        for prompt in prompts:
            f.write(prompt + "\n")

# def extract_information(text, book_title, chapter_title, chapter_number):
#     doc = nlp(text)
#     characters = []
#     locations = []
#     emotions = []
#     objects = []
    
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             characters.append(ent.text)
#         elif ent.label_ in ["LOC", "GPE"]:
#             locations.append(ent.text)
            
#     for token in doc:
#         if "obj" in token.dep_:
#             objects.append(token.text)
    
#     sentences = [sent.text for sent in doc.sents]
#     for sentence in sentences:
#         result = sentiment_analyzer(sentence)[0]
#         if result['label'] in ["POSITIVE", "NEGATIVE"]:
#             emotions.append((sentence, result['label']))
    
#     # This is a very basic and rudimentary extraction, and it might not cover all cases.
#     info = {
#         "characters": list(set(characters)),
#         "locations": list(set(locations)),
#         "emotions": emotions,
#         "objects": list(set(objects))
#     }
    
#      # Create directories if they don't exist
#     script_folder = os.path.dirname(os.path.abspath(__file__))
#     base_path = os.path.join(script_folder, book_title, chapter_title)
#     os.makedirs(base_path, exist_ok=True)
    
#     # Path for the file to save extracted information
#     filename = os.path.join(base_path, f"extracted_info_chapter_{chapter_number}.txt")
    
#     # Save the extracted information to a file
#     save_descriptions_to_file(info, filename)
#     return info

# def save_descriptions_to_file(info, file_path):
#     with open(file_path, 'w', encoding='utf-8') as f:
#         f.write("Characters:\n")
#         for character in info["characters"]:
#             f.write(f"- {character}\n")
            
#         f.write("\nLocations:\n")
#         for location in info["locations"]:
#             f.write(f"- {location}\n")
        
#         f.write("\nEmotions and Context:\n")
#         for emotion in info["emotions"]:
#             f.write(f"- {emotion[1]}: {emotion[0]}\n")
            
#         f.write("\nObjects:\n")
#         for obj in info["objects"]:
#             f.write(f"- {obj}\n")




#EXECUTION

# scrape_and_save_chapter(1)

def main():
    chapter_number = 1

    # chapter_text, book_title, chapter_title = scrape_chapter(chapter_number)
    chapter_text, book_title, chapter_title = scrape_and_save_chapter(chapter_number)
    
    if chapter_text:
        book_title_clean = sanitize_filename(book_title)
        chapter_title_clean = sanitize_filename(chapter_title)
        print("Chapter Text scraped and saved successfully!")
        
        image_prompt, extracted_info = extract_information(chapter_text, book_title_clean, chapter_title_clean, chapter_number)
        print("Image prompt and extracted information saved successfully!")
        # print("Chapter Summary saved successfully!")
    else:
        print("Failed to scrape chapter content.")


if __name__ == "__main__":
    main()