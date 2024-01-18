from PIL import Image, ImageDraw, ImageFont
import requests
from threading import Thread
import io
import textwrap
from instabot import Bot
import schedule
import time
import json
import os
api = 'https://api.quotable.io/random'
contents = []
authors = []
content_number = 0
author_number = 0
image_number = 0
def preload_quotes():
    global contents
    global authors
    for i in range(4):
        random_quote = requests.get(api).json()
        content = random_quote['content']
        author = random_quote['author']
        contents.append(content) 
        authors.append(author)

preload_quotes()

def add_black_overlay(image, transparency):
    image_copy = image.copy()
    overlay = Image.new("RGBA", image.size, (0, 0, 0, int(255 * transparency)))
    image_copy.paste(overlay, (0, 0), overlay)
    return image_copy

def add_text_to_image(img, text,text2, font_size=50, text_color=(255, 255, 255)):
    W,H = img.width, img.height
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype('D:/Lato2OFLWeb/Lato2OFLWeb/LatoLatin/fonts/LatoLatin-Heavy.ttf', font_size)
    font2 = ImageFont.truetype('D:/Lato2OFLWeb/Lato2OFLWeb/LatoLatin/fonts/LatoLatin-Heavy.ttf', 50)
    wrapped_text = textwrap.fill(text, width=40)
    text_bbox1 = draw.textbbox((0,0), text2, font=font2)
    lines = wrapped_text.split('\n')  
    for i, line in enumerate(lines):
        text_bbox = draw.textbbox((0, 0), line, font=font1)
        text_position = ((W - text_bbox[2]) // 2, ((H - text_bbox[3]) // 2)-400 + i*font_size)
        shadow_position = (((W - text_bbox[2]) // 2) + 5, (((H - text_bbox[3]) // 2)-400 + i*font_size) + 5)
        draw.text(shadow_position, line, font=font1, fill=(0,0,0,128))
        draw.text(text_position, line, font=font1, fill=text_color)
    draw.text((((W - text_bbox1[2]) // 2)+5,(H - text_bbox1[3])-95), text2, font=font2, fill=(0,0,0,128))
    draw.text((((W - text_bbox1[2]) // 2),(H - text_bbox1[3])-100), text2, font=font2, fill=text_color)

def display_image():
    global contents
    global authors
    global content_number
    global author_number
    global image_number
    global imgno
    for i in range(3):
        url = 'https://api.unsplash.com/photos/random?query=explore&client_id=nv-lPnJs3mE5UX3IXOT6eV9gg70rChrvQQRBnyk16dw'
        try:
            data = requests.get(url).json()
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            continue
        image_data = requests.get(data['urls']['regular']).content

        with Image.open(io.BytesIO(image_data)) as img:
            text1 = contents[content_number]
            text2 = authors[author_number]
            content_number = content_number + 1
            author_number = author_number + 1
            transparency = 0.3
            image = add_black_overlay(img,transparency)
            image1 = image.resize((1080,1080))
            add_text_to_image(image1, text1,text2)
            image1.save(f'random_image{i}.jpeg')
            if content_number == 2:
                thread = Thread(target=preload_quotes)
                thread.start()
        image_number+=1
display_image()

def post_to_instagram():
    caption = "Embark on a journey of self-discovery through daily reflections and profound wisdom 🌟✨ Consider joining our community for a consistent source of inspiration, positive vibes, and thoughtful moments. Let's explore the depths of insight together. 🚀💖 #Quoteflections #InspirationJourney"
    bot = Bot()
    image_path = 'random_image0.jpeg'
    bot.login(username='quoteflections', password='Dailyquotes2005')
    for i in range(3):
        path = f'random_image{i}.jpeg.REMOVE_ME' 
        if os.path.exists(path):
            os.remove(path)
        image_path = f'random_image{i}.jpeg'
        bot.upload_photo(image_path, caption=caption)
post_to_instagram()