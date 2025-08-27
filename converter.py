import cv2
from time import sleep
import json

char = '█'

fill_hex = '0'

# Template 
template = {
            "style_name": "New",
            "update_tick_time": 1,
            "list_header": {
                "change_rate": 20,
                "values": [
                ]
            },
            "list_footer": {
                "change_rate": 20,
                "values": [
                ]
            },
            "hidden_in_commands": False
        }

# Get input
filename = input('Enter the name of the input file: ')
creator = input('Enter the name of the creator: ')
videoname = input('Enter the name of the video: ')

# Load video
vid = cv2.VideoCapture(filename)

# Frames 
frames = []

# Set framerate
template["list_header"]["change_rate"] = 20 / vid.get(cv2.CAP_PROP_FPS)
template["list_footer"]["change_rate"] = 20 / vid.get(cv2.CAP_PROP_FPS)

footer = [
    f'{videoname} By {creator}',
    'Produced With VideoTab by ADJByDay'
]

# Only read all frames in a video
ret,large_frame = vid.read()
while ret:
    # Sleep to regulate cpu use
    sleep(0.001)
    # Scale Frame
    frame = cv2.resize(large_frame,(80,45))

    # Convert frame to hex
    str_frame = []

    for row in frame:
        r = ''
        for pixel in row:
            p_hex = '#'
            # Add r
            blue = hex(pixel[2])[2:]
            if len(blue) == 1:
                p_hex += fill_hex
            p_hex += blue

            # Add g
            green = hex(pixel[1])[2:]
            if len(green) == 1:
                p_hex += fill_hex
            p_hex += green

            # Add r
            red = hex(pixel[0])[2:]
            if len(red) == 1:
                p_hex += fill_hex
            p_hex += red

            r += f'<color:{p_hex}>{char}</color>'
        # Add row string to list
        str_frame.append(r)

    for line in footer:
        str_frame.append(line)
    
    template["list_footer"]['values'].append(str_frame)
    
    # Read next frame
    ret,large_frame = vid.read()

open(f'{videoname}_{creator}.json','w').write(json.dumps(template))
