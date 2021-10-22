try:
    import sys, getopt
    import pandas as pd
    import pytesseract
    import os, glob
    from PIL import Image, ImageOps
    import piexif
    from datetime import datetime
except ImportError as error:
    print("Error encountered importing a library. Please make sure the following is installed")
    print(error.msg)

# set pathway for tesseract (if not already in system PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'    

def main(argv):
    
    # Parse arguments
    path = ''
    crop_coords = []
    outfile = ''
    try:
        opts, args=getopt.getopt(argv,"hp:c:o:",["path=","crop_coords=","outfile="])
    except getopt.GetoptError:
        print('Usage: python BrowningTimelapseDateFix.py -p <path to images> -c <[crop coordinates]> {-o <output file>}')
        sys.exit(2)
    for opt, arg in opts:
        if opt=='-h':
            print('Usage: python BrowningTimelapseDateFix.py -p <path to images> -c <[crop coordinates]> {-o <output file>}')
            sys.exit()
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-c", "--crop_coords"):
            crop_coords = list(map(int,arg.split(",")))
        elif opt in ("-o", "--outfile"):
            outfile = arg

    # Manually set environment parameters if not given as arguments
    if path=='':
        path = 'C:\\Users\\jakal\\OneDrive - University of Idaho\\UIEF\\TrailCameraPhotos\\Umberger Road Camera\\Extracted Time_Series Photos\\TIMEL0001'
    if crop_coords==[]:
        crop_coords = [700,1033,1500,1077]
        
    print("Processing photos from "+path)
    print("Cropping photos to "+str(crop_coords))
    if outfile!="":
        print("Writing dates/times out to "+outfile)
        
        
        
    # Get list of files
    files = glob.glob(os.path.join(path, "*.jpg"))
    
    out_df = []
    
    #file = 'images-0013.jpg'
    for file in files:
        print("Running file: "+file)
        
        # Open the image, crop it to the date/time portion, and invert it
        im = Image.open(os.path.join(path,file)).convert('L')
        im = im.crop((crop_coords[0],crop_coords[1],crop_coords[2],crop_coords[3]))
        im_invert = ImageOps.invert(im)
        #im_invert.save(os.path.join(path,"test.png"))
        
        # Run tesseract-OCR on the cropped, inverted image
        metadata = pytesseract.image_to_data(im_invert, config='--psm 7', output_type='data.frame')
        
        # Return the metadata as a dictionary and append to the running list (for export)
        metadata = metadata[metadata.conf>50]
        d = {
            'image' : file,
            'date' : metadata['text'][4],
            'time' : metadata['text'][5],
            'camera' : metadata['text'][6]    
        }
        out_df.append(d)
        
        # Read the image EXIF metadata
        exif_dict = piexif.load(file)
        
        # Construct a datetime object from the OCR, format it for writing to EXIF header
        dt = datetime.strptime(metadata['text'][4] + " " + metadata['text'][5], '%m/%d/%Y %I:%M%p')
        new_date = dt.strftime("%Y:%m:%d %H:%M:%S")
        
        # insert date into EXIF and write back out to the image
        exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, os.path.join(path,file))    
    
    # convert output list to pandas dataframe    
    my_df = pd.DataFrame(out_df)
    
    # export pandas dataframe as CSV
    if outfile!='':
        my_df.to_csv(os.path.join(path,outfile))
        print("Output summary written to "+outfile)
    
    print("Finished!!")
        
if __name__ == "__main__":
    main(sys.argv[1:])