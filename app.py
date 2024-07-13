import logging
from logging.handlers import RotatingFileHandler
from model import MyTranscript
from model import GeminiTranscript
from rich.console import Console
from rich.markdown import Markdown
import os

os.system('cls')
handler = RotatingFileHandler(
    'app.log',
    maxBytes=5*1024*1024,
    backupCount=5,
    encoding='utf-8'
)

# Định dạng và mức độ log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

console = Console(color_system='256')


def get_key(path):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
            private_key_lines = [line.strip() for line in lines
                                    if not line.startswith('-----')]
            key = ''.join(private_key_lines)
    except FileNotFoundError as e:
        logger.error(e)
        print(f"File '{path}' not found.")
    except Exception as e:
        logger.error(e)
        print(f"Error reading file '{path}': {e}")
    return key

def check_url(url):
    formats = [
    # Định dạng âm thanh
    ".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".alac", ".aiff", ".aif",
    # Định dạng video
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg", ".mpg", ".webm", ".3gp"]
    return url[-4::] in formats

def input_language():
    language_choice = '# Input language of your video.' + '''\n 1. English (en) \n 2. Vietnamese (vi)'''
    console.print(Markdown(language_choice))
    lang = input().lower()
    while lang not in ('vi', 'en', '1', '2', 'vietnamese', 'english', 'tiếng việt', 'Tiếng anh'):
        retry_message = '# Please retype your language!'
        console.print(Markdown(retry_message))
        logger.info(retry_message)
        console.print(Markdown(language_choice))
        logger.info(language_choice)
        lang = input().lower()
    if lang in ('2', 'vi', 'vietnamese', 'tiếng việt'):
        return 'vi'
    return 'en'

# Path to your file that contain your API KEY    
gemini_key = get_key('keys/gemini.key') 
assemblyai_key = get_key('keys/assemblyai.key')

first_chat = '''# Hello! I\'m Grizmo\' Transcript model!. I will trnascipt a video for you'''
temp = 'Plese enter a video url on the internet or on your computer. Enter a link that end with media file type (Such as: .mp3 or .mp4...)'
console.print(Markdown(first_chat))
console.print(Markdown('# Plese enter a video url on the internet or on your computer. Enter a link that end with media file type (Such as: .mp3 or .mp4...)'))
logger.info(first_chat)
logger.info(temp)

url = input()
while not check_url(url):
    retype_message = '# Please retype your URL! Only enter a link that end with media file type (Such as: .mp3 or .mp4...)'
    console.print(Markdown(retype_message))
    logger.info(retype_message)
    url = input()

lang = input_language()

console.print(Markdown('# Please wait while AI is transcripting!'))
logger.info('# Please wait while AI is transcripting!')
try:
    transcript = MyTranscript(lang, assemblyai_key)
    gemini = GeminiTranscript(key=gemini_key)
    transcripted_text = gemini.respone(transcript.transcript(url))
    console.print(Markdown(transcripted_text))
    logger.info(transcripted_text)
except Exception as e:
    error_message = f'# Some thing gone wrong with model! Please try again later!\n Error: {e}'
    console.print(Markdown(error_message))
    logger.info(error_message)
    logger.error(e)