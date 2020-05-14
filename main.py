import pyautogui
import subprocess
import re
import time
import pyocr
import pyocr.builders

# TODO: automatically fetch these parameters
# For Ubuntu 18.04 Gnome Desktop:
X_OFFSET = 8
Y_OFFSET = 28 + 8

'''
Window 187475849
  Position: 440,333 (screen: 0)
  Geometry: 734x459
'''
def get_active_window_geometry():
    cmd = [ 'xdotool', 'getactivewindow', 'getwindowgeometry' ]
    p = subprocess.run(cmd, capture_output=True)
    output = p.stdout.decode('utf-8')
    lines = output.split('\n')

    m = re.match(r'  Position: (\d+),(\d+).*', lines[1])
    left = int(m.group(1)) - X_OFFSET
    top = int(m.group(2)) - Y_OFFSET

    m = re.match(r'  Geometry: (\d+)x(\d+).*', lines[2])
    width = int(m.group(1))
    height = int(m.group(2))

    return (left, top, width, height)

def resize_active_window(width, height):
    cmd = [ 'xdotool', 'getactivewindow', 'windowsize', str(width), str(height), ]
    subprocess.run(cmd)

def open_and_activate_zoom_participants():
    loc = pyautogui.locateOnScreen('parts/zoom_info.png')
    pyautogui.moveTo(loc)

    time.sleep(1)

    loc = pyautogui.locateOnScreen('parts/participants.png')
    pyautogui.click(loc)

    time.sleep(1)

    resize_active_window(600, 800)

def get_active_window_screenshot():
    box = get_active_window_geometry()
    image = pyautogui.screenshot(region=box)
    # image.save('image.png')

    # TODO: this parameters may be change if the window size is changed
    image = image.crop(box=(49, 0, image.width - 55, image.height - 40))
    # image.save('cropped.png')

    return image

def do_ocr(image):
    tools = pyocr.get_available_tools()
    tool = tools[0]

    langs = tool.get_available_languages()
    assert 'jpn' in langs

    text = tool.image_to_string(
        image,
        lang='jpn',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6),
    )
    return text


if __name__ == '__main__':
    import schedule

    def do_job():
        open_and_activate_zoom_participants()
        image = get_active_window_screenshot()
        text = do_ocr(image)

        print(text)

    schedule.every(10).seconds.do(do_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
