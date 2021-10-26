# Browning Camera Timelapse Plus Photo Processing
We had the misfortune of using some Browning Strike Force cameras for a timelapse application. The Browning Strike Force cameras have two challenges when using them to collect timelapse photos.
1. The photos are stored as frames in a video file (that is "cleverly" disguised as a proprietary data format by Browning, but is really a standard .AVI file).
2. You can't (at least for the model of camera we have) get a straight timelapse - it also does motion detection. So when you get extract the photos from the .AVI file, you have a combination of timelapse and motion-detect photos that have no image metadata (e.g., date/time photo was taken).

The first challenge was adequately addressed by Saul Greenberg: https://saul.cpsc.ucalgary.ca/timelapse/pmwiki.php?n=Main.ExtractingTLSFiles

However, the proposed solution for assigning the date/times to the image files doesn't work if there are motion-detection photos as well as timelapse photos.

The solution we came up with uses Google's Tesseract-OCR to convert the date/time stamp on the images to text, parse that text into an actual date/time and then assign it to the photo file.

### Requirements
 - Python 3.9 or higher
 - pip 18.x or higher
 - Tesseract-OCR 5.x
 - pytesseract 0.3.8
 - PIL 8.2.x or higher
 - Pandas 1.3.1 or higher
 - piexif 1.1.3

### Usage:
`python BrowningTimelapseDateFix.py -p <path to images> -c <[crop coordinates]> {-o <output file>}`

-p = path: directory pathway to the photos
-c = crop coordinates: image coordinates for a bounding box around the date/time information in the photo. This is in the format of left, top, right, bottom and is in number of pixels.
-o = output file: optional argument to write the date and time information for each image out to a CSV file. This file will be created in the same directory as the photos.

### Example:
`python BrowningTimelapseDateFix.py -p C:\Users\jakal\Downloads\TIME0001 -c 700,1033,1500,1077 -o photo_dates.csv`

Photos in the ../TestPhotos/BrowningTimelapse directory are examples processed with this script.

### Installation
The Google Tesseract-OCR engine must be installed for this script to work. the pytesseract library is a wrapper for Tesseract-OCR, but does not include the engine itself. Binaries/installers for Tesseract-OCR are available from https://tesseract-ocr.github.io/tessdoc/Home.html#binaries.

This script assumes you are running Windows and that Tesseract-OCR is installed in the default location: C:/Program Files/Tesseract-OCR/tesseract. If you've installed it in a different location, you can edit the script accordingly.

A conda environment file is included in this repo. From the Conda command line window, you can create a Conda environment with all the required dependencies from the following:

`conda env create -f BrowningTimelapse.yml`

The conda environment is activated by:

`conda activate browning-timelapse`
