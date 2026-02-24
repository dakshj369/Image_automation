import os
import shutil
import base64
from datetime import datetime
from icrawler.builtin import BingImageCrawler
from PIL import Image
import resend
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from dotenv import load_dotenv
load_dotenv()

# ===================================
# Folder Configuration
# ===================================

RAW_FOLDER = "raw_data"
FINAL_FOLDER = "final_images"
ARCHIVE_FOLDER = "archives"


# ===================================
# Folder Management
# ===================================

def create_folders():
    os.makedirs(RAW_FOLDER, exist_ok=True)
    os.makedirs(FINAL_FOLDER, exist_ok=True)
    os.makedirs(ARCHIVE_FOLDER, exist_ok=True)


def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)


# ===================================
# Download Images
# ===================================

def download_images(keyword, num_images):

    crawler = BingImageCrawler(
        downloader_threads=4,
        storage={'root_dir': RAW_FOLDER}
    )

    crawler.crawl(
        keyword=keyword,
        max_num=num_images,
        file_idx_offset=0
    )

# ===================================
# Process Images
# ===================================

def process_images():

    for filename in os.listdir(RAW_FOLDER):

        input_path = os.path.join(RAW_FOLDER, filename)

        try:
            with Image.open(input_path) as img:

                # Resize to fixed dimension (different from friend’s 50%)
                resized_img = img.resize((256, 256))

                # Convert to grayscale
                gray_img = resized_img.convert("L")

                output_path = os.path.join(FINAL_FOLDER, filename)
                gray_img.save(output_path)

        except Exception as e:
            print(f"Skipping {filename} due to error: {e}")


# ===================================
# Zip Images
# ===================================

def zip_images():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"image_bundle_{timestamp}"

    zip_path = os.path.join(ARCHIVE_FOLDER, zip_name)

    shutil.make_archive(zip_path, 'zip', FINAL_FOLDER)

    return zip_path + ".zip"


## ===================================
# Send Email via SendGrid
# ===================================

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

# 🔥 Put your SendGrid API key here
import os
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def send_email(receiver_email, zip_path):

    with open(zip_path, "rb") as f:
        data = f.read()

    encoded_file = base64.b64encode(data).decode()

    message = Mail(
        from_email="jaindaksh2090@gmail.com",
        to_emails=receiver_email,
        subject="Your Image Processing Results",
        html_content="<strong>Your processed images are attached.</strong>"
    )

    attachment = Attachment(
        FileContent(encoded_file),
        FileName("processed_images.zip"),
        FileType("application/zip"),
        Disposition("attachment")
    )

    message.attachment = attachment

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print("Email sent successfully.")
    except Exception as e:
        print("SendGrid Error:", e)