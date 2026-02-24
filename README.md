# Image_automation

## Live Application

The deployed application is available at:

**[Live Link](https://web-production-ab473.up.railway.app/)**

---

## Overview

Image_automation is a automated image processing pipeline.

The system allows a user to:

1. Enter a keyword  
2. Specify the number of images  
3. Provide an email address  

The application then:

- Downloads images 
- Resizes them to 256x256 pixels
- Converts them to grayscale
- Compresses them into a ZIP archive
- Sends the ZIP file to the user via SendGrid email API

The entire pipeline runs automatically in the background without blocking the web server.

---

## Technologies Used

- Python  
- Flask  
- Gunicorn (Production Server)  
- icrawler (Bing Image Crawler)  
- Pillow (Image Processing)  
- SendGrid Email API  
- Railway (Cloud Deployment)  
- python-dotenv (Environment Variable Management)

---

## Project Structure

```
Image_automation/
│
├── templates/
│   └── index.html
│
├── raw_data/          (Downloaded images)
├── final_images/      (Processed grayscale images)
├── archives/          (Generated ZIP files)
│
├── app.py
├── pipeline.py
├── Procfile
├── requirements.txt
├── .env
└── README.md
```

---

## How the Pipeline Works

1. The user submits:
   - Keyword  
   - Number of images  
   - Email address  

2. The backend starts a background thread that:
   - Creates required folders if not present
   - Clears previous data to prevent duplication
   - Downloads images using BingImageCrawler
   - Resizes each image to 256x256 pixels
   - Converts images to grayscale
   - Saves processed images into a separate folder
   - Compresses processed images into a ZIP file with a timestamp

3. The ZIP archive is Base64 encoded and attached to an email.

4. SendGrid API sends the processed images to the user's email address.

---

## Key Engineering Decisions

- Implemented background threading to prevent request blocking.
- Added automatic folder cleanup before each execution.
- Used environment variables to secure API keys.
- Generated timestamp-based ZIP filenames to avoid overwriting.
- Wrapped image processing in try-except blocks to handle corrupted images.
- Used Base64 encoding to attach ZIP files through SendGrid API.


---

## Future Improvements

- Implement a background task queue (Celery or RQ)
- Add real-time progress tracking
- Add user authentication system
- Add rate limiting
- Replace scraping with official image search APIs
- Add frontend status updates instead of static message

---

## Author

Daksh Jain  
B.Tech Student  
Third Year  
