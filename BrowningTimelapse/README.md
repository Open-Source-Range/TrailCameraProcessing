# Browning Camera Timelapse Plus Photo Processing
The Browning Strike Force cameras have two challenges when using them to collect timelapse photos.
1. The photos are stored as frames in a video file (that is "cleverly" disguised as a proprietary data format by Browning)
2. You can't (at least for the model of camera we have) get a straight timelapse - it also does motion detection.

The first challenge was adequately addressed by Saul Greenberg: https://saul.cpsc.ucalgary.ca/timelapse/pmwiki.php?n=Main.ExtractingTLSFiles

However, the proposed solution for assigning the date/times to the image files doesn't work well if there are motion-detection photos as well as timelapse photos.

The solution we came up with uses Google's Tesseract-OCR to convert the date/time stamp on the images to text, parse that text into an actual date/time and then assign it to the photo file.

### Dependencies
 - Python 3.x
 - Tesseract-OCR
 - pytesseract
 - PIL
 - Pandas
 - piexif


### Usage:
python BrowningTimelapseDateFix.py -p <path to images> -c <[crop coordinates]> {-o <output file>}

-p = path: directory pathway to the photos
-c = crop coordinates: image coordinates for a bounding box around the date/time information in the photo. This is in the format of left, top, right, bottom and is in number of pixels.
-o = output file: optional argument to write the date and time information for each image out to a CSV file. This file will be created in the same directory as the photos.

### Example:
python BrowningTimelapseDateFix.py -p C:\Users\jakal\Downloads\TIME0001 -c 700,1033,1500,1077 -o photo_dates.csv
