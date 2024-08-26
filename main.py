import os
import re
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

# Directories
raw_videos_dir = os.path.abspath('container/raw_videos')
output_dir = os.path.abspath('output')
outro_path = os.path.abspath('container/outro.mp4')
download_directory = os.path.abspath('container/raw_videos')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
os.makedirs(download_directory, exist_ok=True)

# Load the outro clip
if not os.path.exists(outro_path):
    raise FileNotFoundError(f"Error: 'outro.mp4' not found at {outro_path}")

# Load and resize the outro clip
outro_clip = VideoFileClip(outro_path)

def add_laughter_to_lines(input_file, intermediate_file):
    with open(input_file, 'r') as infile, open(intermediate_file, 'w') as interfile:
        for line in infile:
            stripped_line = line.rstrip()
            modified_line = stripped_line + ' hahahahahahaha !\n'
            interfile.write(modified_line)

def text_to_audio(text, output_file, api_key, url):
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'text': text,
        'model_id': 'eleven_multilingual_v2',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.5
        },
        'output_format': 'mp3_44100_128'
    }
    
    response = requests.post(url, json=payload, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Audio file saved as {output_file}")
    else:
        print(f"Failed to generate audio: {response.status_code}, {response.text}")

def wait_for_download_to_complete(expected_filename, timeout=300):
    start_time = time.time()
    while True:
        if any(fname.endswith(expected_filename) for fname in os.listdir(download_directory)):
            print(f"Download of {expected_filename} complete.")
            break
        if time.time() - start_time > timeout:
            raise Exception("Download timed out.")
        time.sleep(1)

def generate_animations(audio_directory):
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else 0

    audios = [os.path.abspath(os.path.join(audio_directory, f)) for f in os.listdir(audio_directory) if f.endswith('.mp3')]
    audios.sort(key=lambda x: extract_number(x))
    print(f"Found audio files: {audios}")

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:/Users/mehdi/AppData/Local/Google/Chrome/User Data")
    chrome_options.add_argument("profile-directory=Default")

    service = Service(executable_path="chromedriver.exe")
    global driver, wait
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 200)

    driver.get('https://new.express.adobe.com/home/tools/animate-from-audio')
    time.sleep(30)

    def get_shadow_root(element):
        return element.shadow_root

    shadow_roots = {}

    def cache_shadow_roots():
        app = driver.find_element(By.CSS_SELECTOR, 'x-app')
        shadow_roots['root'] = get_shadow_root(app)

        quick_action_modal = shadow_roots['root'].find_element(By.CSS_SELECTOR, 'x-quick-action-modal')
        shadow_roots['quick_action_modal'] = get_shadow_root(quick_action_modal)

        quick_action_component = shadow_roots['quick_action_modal'].find_element(By.CSS_SELECTOR, 'quick-action-component')
        shadow_roots['quick_action_component'] = get_shadow_root(quick_action_component)

        qa_animate_from_audio_editor = shadow_roots['quick_action_component'].find_element(By.CSS_SELECTOR, 'qa-animate-from-audio-editor')
        shadow_roots['qa_animate_from_audio_editor'] = get_shadow_root(qa_animate_from_audio_editor)

        qa_animate_from_audio_backgrounds_panel = shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'qa-animate-from-audio-backgrounds-panel')
        shadow_roots['qa_animate_from_audio_backgrounds_panel'] = get_shadow_root(qa_animate_from_audio_backgrounds_panel)

    def find_element_in_shadow_root(shadow_root_key, selector):
        shadow_root = shadow_roots[shadow_root_key]
        return shadow_root.find_element(By.CSS_SELECTOR, selector)

    def generate_raw_video(audio, index):
        cache_shadow_roots()

        backgrounds_button = find_element_in_shadow_root('qa_animate_from_audio_editor', 'sp-tab[label="Background"]')
        backgrounds_button.click()

        qa_animate_from_audio_thumbnail_grid = shadow_roots['qa_animate_from_audio_backgrounds_panel'].find_element(By.CSS_SELECTOR, 'qa-animate-from-audio-thumbnail-grid')
        shadow_roots['qa_animate_from_audio_thumbnail_grid'] = get_shadow_root(qa_animate_from_audio_thumbnail_grid)

        qa_thumbnail_grid = shadow_roots['qa_animate_from_audio_thumbnail_grid'].find_element(By.CSS_SELECTOR, 'qa-thumbnail-grid')
        shadow_roots['qa_thumbnail_grid'] = get_shadow_root(qa_thumbnail_grid)

        qa_thumbnails = shadow_roots['qa_thumbnail_grid'].find_elements(By.CSS_SELECTOR, 'qa-thumbnail')
        qa_thumbnail = random.choice(qa_thumbnails)
        shadow_roots['qa_thumbnail'] = get_shadow_root(qa_thumbnail)

        choose_background_button = find_element_in_shadow_root('qa_thumbnail', 'button')
        driver.execute_script("arguments[0].click();", choose_background_button)

        try:
            replace_audio_link = shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'sp-link[id="replace-audio-link"]')
            replace_audio_link.click()
            print("Replace audio clicked")
        except (NoSuchElementException, Exception):
            print("Replace audio skipped")

        while True:
            try:
                qa_file_upload = shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'qa-file-upload')
                shadow_roots['qa_file_upload'] = get_shadow_root(qa_file_upload)
                upload_audio_input = find_element_in_shadow_root('qa_file_upload', 'input[id="file-input"]')
                upload_audio_input.send_keys(audio)
                break
            except StaleElementReferenceException:
                print("Stale element reference exception caught, retrying...")

        wait.until(lambda driver: shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'qa-export'))

        qa_export = shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'qa-export')
        shadow_roots['qa_export'] = get_shadow_root(qa_export)

        download_button = find_element_in_shadow_root('qa_export', 'sp-button[data-export-option-id="downloadExportOption"]')

        while True:
            try:
                if download_button.get_attribute('aria-disabled') == 'true':
                    print("Download button is disabled, waiting...")
                    time.sleep(1)
                    continue

                download_button.click()
                break
            except ElementClickInterceptedException:
                print("Element click intercepted, retrying...")
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected exception: {e}")
                time.sleep(1)

        expected_filename = f"dadjoke_{index + 1}.mp4"
        print(f"Waiting for download of {expected_filename}")
        wait_for_download_to_complete(expected_filename, timeout=600)

        wait.until(lambda driver: shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'sp-button[id="back-to-edit-button"]'))
        back_to_edit_button = shadow_roots['qa_animate_from_audio_editor'].find_element(By.CSS_SELECTOR, 'sp-button[id="back-to-edit-button"]')
        back_to_edit_button.click()

    for index, audio in enumerate(audios):
        print(f"Processing audio file: {audio} (index {index + 1})")
        generate_raw_video(audio, index)
        print(f"Completed processing audio file: {audio} (index {index + 1})")

    time.sleep(30)
    driver.quit()

def edit_video(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        outro_with_transition = outro_clip.crossfadein(2)
        pre_final_clip = concatenate_videoclips([video_clip, outro_with_transition], method="compose")
        final_clip = pre_final_clip.fx(vfx.blackwhite)
        video_filename = os.path.basename(video_path)
        output_path = os.path.join(output_dir, video_filename)
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            preset='slow',
            bitrate='5000k',
            ffmpeg_params=['-crf', '18'],
            audio=True
        )
    except Exception as e:
        print(f"Error processing video {video_path}: {e}")
        raise

def main(input_file):
    intermediate_file = 'container/addLaughter.txt'
    output_folder = 'container/audios'
    os.makedirs(output_folder, exist_ok=True)
    
    add_laughter_to_lines(input_file, intermediate_file)
    
    with open(intermediate_file, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            text = line.strip()
            output_file = f"{output_folder}/dadjoke_{index + 1}.mp3"

            api_key = 'your_api_key_here'
            url = "https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb"
            text_to_audio(text, output_file, api_key, url)

    generate_animations(output_folder)

    if not os.path.exists(raw_videos_dir):
        raise FileNotFoundError(f"Error: 'raw_videos' directory not found at {raw_videos_dir}")

    for video_filename in os.listdir(raw_videos_dir):
        video_path = os.path.join(raw_videos_dir, video_filename)
        if os.path.isfile(video_path):
            edit_video(video_path)

if __name__ == "__main__":
    input_file = 'container/rawData.txt'
    main(input_file)