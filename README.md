# TikTok Content Creator Script

## Overview
This script automates the creation of TikTok videos by transforming a list of plain text dad jokes into animated videos with AI-generated voiceovers. It utilizes MoviePy for video editing and Selenium for automation, streamlining the entire content creation process.

## Features
- **Automated Video Creation**: Converts dad jokes into engaging TikTok videos.
- **AI Voiceover**: Adds AI-generated voiceovers to each joke.
- **Adobe Express AI Animations**: Enhances videos with custom animations choosing a random background with Selenium  .
- **Easy Social Media Sharing**: Generates ready-to-upload content for TikTok.

## Requirements
- Python 3.x
- MoviePy
- Selenium
- Additional Python libraries as needed (e.g., `gTTS` for text-to-speech)

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/ai-content-creator.git
    cd ai-content-creator
    ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Selenium by downloading the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome).

## Important Notes
- **API Key**: Make sure to update the Eleven Labs API key in the script (`main.py`) with your own key to enable AI voice generation.
- **ChromeDriver Compatibility**: Ensure that the ChromeDriver version matches the version of Google Chrome installed on your system. You can download the correct version from [here](https://sites.google.com/chromium.org/driver/downloads).
- **Customizing the outro**:After generating the raw videos the script will add the outro at the end of each generated video ,feel free to custimize your outro in (`container/outro.mp4`)

## Usage
1. Prepare your list of dad jokes in the text file (`container/rawData.txt`), with one joke per line.
2. Run the script:
    ```bash
    python main.py
    ```
3. The script will generate TikTok videos with the jokes and save them to the output directory.

## Customization
- **Voiceover**: Customize the AI voice by adjusting parameters in the script.
- **Animations**: Modify the animations by editing the MoviePy functions in the script.
- **Output Settings**: Change the resolution, frame rate, or other video settings as needed.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you have suggestions or improvements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Let's Work Together
Have ideas for improving this script or need help with a similar project? Let's collaborate! Reach out to get started.
