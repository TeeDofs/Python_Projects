import requests
from bs4 import BeautifulSoup
import time
import os
import boto3
from pydub import AudioSegment

# Specify the base URL for the chapters you want to scrape
# BASE_URL = "https://bednovel.com/bednovel/the-mech-touch-89501/ch{}" #Link for The Mech Touch
# BASE_URL = "https://bednovel.com/bednovel/chaotic-sword-god-47396/ch{}" #Link for Chaotic Sword God
# BASE_URL = "https://bednovel.com/bednovel/another-worlds-versatile-crafting-master-80639/ch{}" #Link for Another World's Versatile Crafting Master
# BASE_URL = "https://bednovel.com/bednovel/emperors-domination-44650/ch{}" #Link for Emperor Dominion
# BASE_URL = "https://bednovel.com/bednovel/warlock-of-the-magus-world-100160/ch{}" # Link for Warlock of the magus world 
BASE_URL = "https://bednovel.com/bednovel/nine-star-hegemon-body-arts-33425/ch{}"

class Book:
    def __init__(self, title, chapterNumber, voiceId, url):
        self.title = title
        self.chapterNumber = chapterNumber
        self.voiceId = voiceId
        self.url = url

mech_touch = Book(
    "The Mech Touch", 
    5334, 
    "Joanna", 
    "https://bednovel.com/bednovel/the-mech-touch-89501/ch{}"
)

chaotic_sword_god = Book(
    "Chaotic Sword God", 
    3613, 
    "Joanna", 
    "https://bednovel.com/bednovel/chaotic-sword-god-47396/ch{}"
)

another_worlds_versatile_crafting_master = Book(
    "Another World's Versatile Crafting Master", 
    1309, 
    "Joanna", 
    "https://bednovel.com/bednovel/another-worlds-versatile-crafting-master-80639/ch{}"
)

emperors_domination = Book(
    "Emperors Domination", 
    5432, 
    "Mathew", 
    "https://bednovel.com/bednovel/emperors-domination-44650/ch{}"
)

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

currentBook = my_vampire_system

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

    while chapter_text:
        text_chunk, chapter_text = split_text_at_fullstop(chapter_text, 2900)
        print(f"Synthesizing text of length {len(text_chunk.split())} words...")
        
        response = polly_client.synthesize_speech(
            Text=text_chunk,
            OutputFormat='mp3',
            VoiceId=currentBook.voiceId
            # VoiceId='Matthew'
            # VoiceId='Joanna'
        )
        
        part_file_name = os.path.join(book_title, f"{chapter_title}_Part{part_number}.mp3")
        with open(part_file_name, 'wb') as f:
            f.write(response['AudioStream'].read())

        print(f"Saved {part_file_name}")
        part_number += 1

def combine_audio_files(book_title, chapter_title, num_parts):
    combined = AudioSegment.empty()
    for i in range(1, num_parts + 1):
        part_filename = os.path.join(book_title, f"{chapter_title}_Part{i}.mp3")
        print(f"Combining {part_filename}...")
        audio_part = AudioSegment.from_mp3(part_filename)
        combined += audio_part
        print(f"Deleting {part_filename}...")  # Debug print
        os.remove(part_filename)
    combined.export(os.path.join(book_title, f"{chapter_title}.mp3"), format="mp3")

def ensure_directory_exists(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def get_latest_chapter_in_directory(book_title, starting_chapter):
    if not os.path.exists(book_title):
        return starting_chapter - 1
    chapters = [f for f in os.listdir(book_title) if f.endswith(".mp3")]
    if not chapters:
        return starting_chapter - 1
    chapters.sort()
    latest_chapter = int(chapters[-1].split('_')[0].split()[-1])
    return latest_chapter


def main():
    print("Starting main")
    starting_chapter = 1
    limit_chapter = currentBook.chapterNumber

    book_title = "Unknown Book"
    latest_chapter = get_latest_chapter_in_directory(book_title, starting_chapter)
    starting_chapter = max(starting_chapter, latest_chapter + 1)  # Start from the next chapter after the latest
    
    chapter_number = starting_chapter
    while chapter_number <= limit_chapter:
        try:
            print(f"Processing chapter {chapter_number}...")
            chapter_content, book_title, chapter_title = scrape_chapter(chapter_number)
            chapter_title = sanitize_filename(chapter_title) # Use sanitized chapter title
            if not chapter_content:
                print(f"Failed to scrape chapter {chapter_number}.")
                chapter_number += 1
                continue

            ensure_directory_exists(book_title)

            base_file_name = f"{chapter_title}"
            text_to_audio(chapter_content, book_title, base_file_name)

            num_parts = len([f for f in os.listdir(book_title) if f.startswith(f"{chapter_title}_Part")])
            if num_parts > 1:
                combine_audio_files(book_title, chapter_title, num_parts)

            chapter_number += 1
            time.sleep(5)
        except Exception as e:
            print(f"Error processing chapter {chapter_number}: {e}")
            break

if __name__ == "__main__":
    main()

# #Test the code out
# chapter_content, book_title, chapter_title = scrape_chapter(1)
# if not chapter_content:
#     print("Failed to scrape the content.")

# ensure_directory_exists(book_title)
# file_name = os.path.join(book_title, f"{chapter_title}.mp3")
# text_to_audio(chapter_content, file_name)
# print(f"Saved {file_name}")