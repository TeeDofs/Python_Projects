import requests
from bs4 import BeautifulSoup
import time
import os
import boto3
import re
from pydub import AudioSegment

class Book:
    def __init__(self, title, chapterNumber, voiceId, url):
        self.title = title
        self.chapterNumber = chapterNumber
        self.voiceId = voiceId
        self.url = url

the_mech_touch = Book(
    "The Mech Touch", 
    5364, 
    "Joanna", 
    "https://bednovel.com/bednovel/the-mech-touch-89501/ch{}"
)

chaotic_sword_god = Book(
    "Chaotic Sword God", 
    3620, 
    "Joanna", 
    "https://bednovel.com/bednovel/chaotic-sword-god-47396/ch{}"
)

#Complete
another_worlds_versatile_crafting_master = Book(
    "Another World's Versatile Crafting Master", 
    1309, 
    "Joanna", 
    "https://bednovel.com/bednovel/another-worlds-versatile-crafting-master-80639/ch{}"
)

emperors_domination = Book(
    "Emperors Domination", 
    5432, 
    "Matthew", 
    "https://bednovel.com/bednovel/emperors-domination-44650/ch{}"
)

#Complete
warlock_of_the_magus_world = Book(
    "Warlock Of The Magus World", 
    1200, 
    "Emma", 
    "https://bednovel.com/bednovel/warlock-of-the-magus-world-100160/ch{}"
)

nine_star_hegemon_body_arts = Book(
    "Nine Star Hegemon Body Arts", 
    4274, 
    "Joanna", 
    "https://bednovel.com/bednovel/nine-star-hegemon-body-arts-33425/ch{}"
)

my_vampire_system = Book(
    "My Vampire System",
    2527,
    "Matthew",
    "https://bednovel.com/bednovel/my-vampire-system-37069/ch{}"
)

dragon_marked_war_god = Book(
    "Dragon Marked War God",
    3060,
    "Joanna",
    "https://bednovel.com/bednovel/dragon-marked-war-god-33782/ch{}"
)

coiling_dragon = Book(
    "Coiling Dragon",
    808,
    "Joanna",
    "https://bednovel.com/bednovel/coiling-dragon-64639/ch{}"
)

library_of_heavens_path = Book(
    "Library of Heaven's Path",
    2271,
    "Joanna",
    "https://bednovel.com/bednovel/library-of-heavens-path-8252/ch{}"
)

currentBook = library_of_heavens_path

def sanitize_filename(filename):
    # Sanitize filenames by removing or replacing problematic characters.
    invalid_chars = ['?', ':', '\\', '/', '>', '<', '*', '|', '"']
    for char in invalid_chars:
        filename = filename.replace(char, "")
    return filename

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

    return chapter_text, book_title, chapter_title

def split_text_at_fullstop(text, max_bytes):
    """Splits the text at the last full stop before max_bytes."""
    if len(text.encode('utf-8')) <= max_bytes:
        return text, ''

    substr = text[:max_bytes].rsplit('.', 1)[0] + '.'
    index = len(substr)
    return text[:index], text[index:]


def text_to_audio(chapter_text, book_title, chapter_title):
    print("Initializing Polly client...")
    polly_client = boto3.client('polly', region_name='us-east-1')
    part_number = 1

    script_directory = os.path.dirname(__file__)
    audio_books_directory = os.path.join(script_directory, "Audio Books")
    part_directory = os.path.join(audio_books_directory, book_title)
    ensure_directory_exists(part_directory)

    while chapter_text:
        text_chunk, chapter_text = split_text_at_fullstop(chapter_text, 2900)
        print(f"Synthesizing text of length {len(text_chunk.split())} words...")
        
        response = polly_client.synthesize_speech(
            Text=text_chunk,
            OutputFormat='mp3',
            VoiceId=currentBook.voiceId
        )
        
        part_file_name = f"{chapter_title}_Part{part_number}.mp3"
        part_file_path = os.path.join(part_directory, part_file_name)
        with open(part_file_path, 'wb') as f:
            f.write(response['AudioStream'].read())

        print(f"Saved {part_file_path}")
        part_number += 1

def combine_audio_files(book_title, chapter_title, num_parts):
    script_directory = os.path.dirname(__file__)
    audio_books_directory = os.path.join(script_directory, "Audio Books")
    part_directory = os.path.join(audio_books_directory, sanitize_filename(book_title))
    ensure_directory_exists(part_directory)  # Ensure the directory exists

    combined = AudioSegment.empty()
    for i in range(1, num_parts + 1):
        part_filename = f"{sanitize_filename(chapter_title)}_Part{i}.mp3"
        part_file_path = os.path.join(part_directory, part_filename)
        
        if os.path.exists(part_file_path):  # Check if the file exists before trying to open it
            print(f"Combining {part_filename}...")
            audio_part = AudioSegment.from_mp3(part_file_path)
            combined += audio_part

            print(f"Deleting {part_filename}...")  # Debug print
            os.remove(part_file_path)
        else:
            print(f"File not found: {part_file_path}")

    combined.export(os.path.join(part_directory, f"{sanitize_filename(chapter_title)}.mp3"), format="mp3")

def ensure_directory_exists(directory_path):
    # Check if the directory exists at the provided path and create it if it doesn't
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_latest_chapter_in_directory(book_title, starting_chapter):
    script_directory = os.path.dirname(__file__)
    audio_books_directory = os.path.join(script_directory, "Audio Books")
    book_directory = os.path.join(audio_books_directory, book_title)
    if not os.path.exists(book_directory):
        return starting_chapter - 1
    chapters = [f for f in os.listdir(book_directory) if f.endswith(".mp3")]
    if not chapters:
        return starting_chapter - 1
    chapters.sort()

    # Using regular expression to find the chapter number in the filename
    chapter_numbers = []
    for chapter in chapters:
        match = re.search(r'\d+', chapter)
        if match:
            chapter_number = int(match.group())
            chapter_numbers.append(chapter_number)

    if not chapter_numbers:
        return starting_chapter - 1

    return max(chapter_numbers)

def main():
    print("Starting main")
    starting_chapter = 1
    limit_chapter = currentBook.chapterNumber

    # Ensure book title is sanitized before use
    book_title = sanitize_filename(currentBook.title)
    latest_chapter = get_latest_chapter_in_directory(book_title, starting_chapter)
    starting_chapter = max(starting_chapter, latest_chapter + 1)

    chapter_number = starting_chapter

    while chapter_number <= limit_chapter:
        try:
            print(f"Processing chapter {chapter_number}...")
            chapter_content, _, chapter_title = scrape_chapter(chapter_number)
            chapter_title = sanitize_filename(chapter_title)

            if chapter_content:
                text_to_audio(chapter_content, book_title, chapter_title)
                book_directory = os.path.join(os.path.dirname(__file__), "Audio Books", book_title)
                num_parts = len([f for f in os.listdir(book_directory) if chapter_title in f and f.endswith(".mp3")])
                combine_audio_files(book_title, chapter_title, num_parts)
            else:
                print(f"Chapter {chapter_number} not found.")
            
            chapter_number += 1
            time.sleep(5)  # Avoid being banned from the website
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(10)


if __name__ == "__main__":
    main()
