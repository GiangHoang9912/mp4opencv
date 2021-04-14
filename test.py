from PIL import Image
import cv2
import sys
import time
import playsound
import os
import glob

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

frame_interval = 1/31
frame_size = 150

def play_video():
    if not os.path.exists('extracted-frame'):
        os.makedirs('extracted-frame')
    verified_frames = 1
    for frame_count in range(1, 6572):
        path_to_file = r'extracted-frame/' + 'video-test-' + str(frame_count) + '.jpg'
        if os.path.isfile(path_to_file):
            verified_frames += 1
    if verified_frames <= 6000:
        cap = cv2.VideoCapture("video-test.mp4")
        current_frame = 1
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        while current_frame < total_frames:
            ret, frame = cap.read()
            
            progress = float(current_frame) * 100 / ( total_frames - 1 ) 
            arrow = '#' * int(progress / 100 * 25 - 1)
            spaces = ' ' * (25 - len(arrow))
            sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, current_frame, total_frames))

            frame_name = r"extracted-frame/" + "video-test-" + str(current_frame) + ".jpg"
            cv2.imwrite(frame_name, frame)
            current_frame += 1
        cap.release()

    if not os.path.exists('text-files'):
        os.makedirs('text-files')
    verified_frames = 1

    files_length = len(glob.glob1('extracted-frame',"*.jpg"))

    for frame_count in range(1, files_length):
        path_to_file = r'text-files/' + 'video-test-' + str(frame_count) + '.txt'
        if os.path.isfile(path_to_file):
            verified_frames += 1
    if verified_frames <= 6000:
        for frame_count in range(1, files_length):
            path_to_file = r'extracted-frame/' + 'video-test-' + str(frame_count) + '.jpg'
            image = Image.open(path_to_file)

            width, height = image.size
            aspect_ratio = (height / float(width * 2.5))
            new_height = int(aspect_ratio * frame_size)
            resized_image = image.resize((frame_size, new_height))

            greyscale_image = resized_image.convert("L")

            pixels = greyscale_image.getdata()
            characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])

            ascii_characters = characters
            pixel_count = len(ascii_characters)
            ascii_image = "\n".join(
                [ascii_characters[frame_count:(frame_count + frame_size)] for frame_count in range(0, pixel_count, frame_size)])
            file_name = r"text-files/" + "video-test-" + str(frame_count) + ".txt"
            with open(file_name, "w") as f:
                f.write(ascii_image)
            progress = float(frame_count) * 100 / files_length
            arrow = '#' * int(progress / 100 * 25 - 1)
            spaces = ' ' * (25 - len(arrow))
            sys.stdout.write('\rProgress: [%s%s] %d%% Frame %d of %d frames' % (arrow, spaces, progress, frame_count, files_length))

    for frame_number in range(1, files_length):
        start_time = time.time()
        file_name = r"text-files/" + "video-test-" + str(frame_number) + ".txt"
        with open(file_name, 'r') as f:
            sys.stdout.write("\r" + f.read())
        compute_delay = float(time.time() - start_time)
        delay_duration = frame_interval - compute_delay
        if delay_duration < 0:
            delay_duration = 0
        time.sleep(delay_duration)

        

def main():
    while True:
        sys.stdout.write('==============================================================\n')
        sys.stdout.write('Select option: \n')
        sys.stdout.write('1) Play\n')
        sys.stdout.write('2) Exit\n')
        sys.stdout.write('==============================================================\n')

        user_input = input("Your option: ")
        user_input.strip()

        

        if user_input == '1':
            play_video()
            continue
        elif user_input == '2':
            exit()
            continue
        else:
            sys.stdout.write('Unknown input!\n')
            continue


if __name__ == "__main__":
    main()