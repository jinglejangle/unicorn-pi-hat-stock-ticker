#!/usr/bin/env python
# This is basically the pimoroni rainbow-text example but mashed up to show the stock prices 
# For details of that script go here: https://github.com/pimoroni/unicorn-hat-hd

import yfinance as yf
from pprint import pprint
import colorsys
import time
from sys import exit
import pandas as pd
import os
try:
    import unicornhathd
except ImportError:
    exit('This script requires the unicornhathd module\nInstall with: sudo pip install unicornhat, more details here: https://github.com/pimoroni/unicorn-hat')

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit('This script requires the pillow module\nInstall with: sudo pip install pillow')


unicornhathd.rotation(180)
unicornhathd.brightness(0.6)
width, height = unicornhathd.get_shape()

toggle = True; 
TEXT2 = "" 
TEXT = "" 
count = 0
refreshCache = True
cacheUpdateLoop  = 20

tickerIdx=0

while True: 


    
    count = count + 1; 
    if(count > cacheUpdateLoop):
        print ("Updating ticker cache" )
        toggle = True
        count = 1



    if tickerIdx == 0: 
        ticker_yahoo = yf.Ticker('GME')
        data = ticker_yahoo.history()
        last_quote = (round(data.tail(1)['Close'].iloc[0],2))
        last_open = (round(data.tail(1)['Open'].iloc[0],2))
        TEXT = "G M E"
        TEXT2 =  str(int(last_quote))

        toggle= not toggle

    elif tickerIdx == 1:

        ticker_amc = yf.Ticker('AMC')
        data = ticker_amc.history()
        last_quote = (round(data.tail(1)['Close'].iloc[0],2))
        last_open = (round(data.tail(1)['Open'].iloc[0],2))
        TEXT = "A M C" 
        TEXT2 = str((last_quote))
 
    elif tickerIdx == 2:
        ticker_bb = yf.Ticker('BB')
        dataBB = ticker_bb.history()
        last_quote_bb = (round(dataBB.tail(1)['Close'].iloc[0],2))
        last_quote = (round(dataBB.tail(1)['Close'].iloc[0],2))
        last_open = (round(dataBB.tail(1)['Open'].iloc[0],2))
        TEXT = "B B"
        TEXT2 =  str((last_quote))
        tickerIdx=-1
  
    tickerIdx += 1

    #FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 6)
    FONT2 = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 9)
    #FONT = ('/usr/share/fonts/truetype/piboto/Piboto-Bold', 12)
    # sudo apt install fonts-droid
    # FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

    # sudo apt install fonts-roboto
    #FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 8)
    #FONT = ('/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf', 8)
    FONT = ('/usr/share/fonts/truetype/roboto/unhinted/RobotoCondensed-Light.ttf', 7)


    # Use `fc-list` to show a list of installed fonts on your system,
    # or `ls /usr/share/fonts/` and explore.

    # sudo apt install fonts-droid
    # FONT = ('/usr/share/fonts/truetype/droid/DroidSans.ttf', 12)

    # sudo apt install fonts-roboto
    # FONT = ('/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf', 10)

    # ================ Now, let's draw some amazing rainbowy text! ===================

    # Get the width/height of Unicorn HAT HD.
    # These will normally be 16x16 but it's good practise not to hard-code such numbers,
    # just in case you want to try and hack together a bigger display later.
    width, height = unicornhathd.get_shape()

    unicornhathd.rotation(90)
    unicornhathd.brightness(0.9)

    # We want to draw our text 1 pixel in, and 2 pixels down from the top left corner
    text_x = 0
    text_y = 0

    # Grab our font file and size as defined at the top of the script
    font_file, font_size = FONT
    font_file2, font_size2 = FONT2

    # Load the font using PIL's ImageFont
    font = ImageFont.truetype(font_file, font_size)
    font2 = ImageFont.truetype(font_file2, font_size2)

    # Ask the loaded font how big our text will be
    text_width, text_height = font.getsize(TEXT)

    # Make sure we accommodate enough width to account for our text_x left offset
    text_width += width + text_x

    # Now let's create a blank canvas wide enough to accomodate our text
    image = Image.new('RGB', (text_width, max(height, 16)), (0, 0, 0))

    # To draw on our image, we must use PIL's ImageDraw
    draw = ImageDraw.Draw(image)

    # And now we can draw text at our desited (text_x, text_y) offset, using our loaded font
    draw.text((text_x, text_y), TEXT, fill=(255, 255, 255), font=font)
    draw.text((text_x, text_y+6), TEXT2, fill=(255, 255, 255), font=font2)

    # To give an appearance of scrolling text, we move a 16x16 "window" across the image we generated above
    # The value "scroll" denotes how far this window is from the left of the image.
    # Since the window is "width" pixels wide (16 for UHHD) and we don't want it to run off the end of the,
    # image, we subtract "width".
    scroll2 = 0
    for scroll in range(text_width - width + 200):
        for x in range(width):

            # Figure out what hue value we want at this point.
            # "x" is the position of the pixel on Unicorn HAT HD from 0 to 15
            # "scroll" is how far offset from the left of our text image we are
            # We want the text to be a complete cycle around the hue in the HSV colour space
            # so we divide the pixel's position (x + scroll) by the total width of the text
            # If this pixel were half way through the text, it would result in the number 0.5 (180 degrees)
            if(scroll <= text_width): 
                hue = (x + scroll ) / float(text_width)
            else:
                hue = (x + scroll ) / float(text_width)
            # Now we need to convert our "hue" value into r,g,b since that's what colour space our
            # image is in, and also what Unicorn HAT HD understands.
            # This list comprehension is just a tidy way of converting the range 0.0 to 1.0
            # that hsv_to_rgb returns into integers in the range 0-255.
            # hsv_to_rgb returns a tuple of (r, g, b)
            br, bg, bb = [int(n * 255) for n in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]

            # Since our rainbow runs from left to right along the x axis, we can calculate it once
            # for every vertical line on the display, and then re-use that value 16 times below:

            for y in range(height):
                # Get the r, g, b colour triplet from pixel x,y of our text image
                # Our text is white on a black background, so these will all be shades of black/grey/white
                # ie 255,255,255 or 0,0,0 or 128,128,128
                pixel = image.getpixel((x + 0, y))

                # Now we want to turn the colour of our text - shades of grey remember - into a mask for our rainbow.
                # We do this by dividing it by 255, which converts it to the range 0.0 to 1.0
                r, g, b = [float(n / 255.0) for n in pixel]

                # We can now use our 0.0 to 1.0 range to scale our three colour values, controlling the amount
                # of rainbow that gets blended in.
                # 0.0 would blend no rainbow
                # 1.0 would blend 100% rainbow
                # and anything in between would copy the anti-aliased edges from our text
                r = int(br * r)
                g = int(bg * g)
                b = int(bb * b)

                # Finally we colour in our finished pixel on Unicorn HAT HD
                unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

        # Set a triangle up or down, red or green if close is higher/lower than open 
        if(last_open < last_quote): 
            unicornhathd.set_pixel(0 , 0, 0, 255, 0)
            unicornhathd.set_pixel(1 , 0, 0, 255, 0)
            unicornhathd.set_pixel(0 , 1, 0, 255, 0)
        else: 
            unicornhathd.set_pixel(0 , 0, 255, 0, 0)
            unicornhathd.set_pixel(1 , 1, 255, 0, 0)
            unicornhathd.set_pixel(0 , 1, 255, 0, 0)
        # Finally, for each step in our scroll, we show the result on Unicorn HAT HD
        unicornhathd.show()

        # And sleep for a little bit, so it doesn't scroll too quickly!
        time.sleep(0.05)

    time.sleep(0.02)
    unicornhathd.off()
unicornhathd.off()

