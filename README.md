# ChatGPT telegram bot (voice, text)
> **NOTE**:
> The bot nickname is the same as the repository's :-)

## Feature
- Model - gpt-3.5-turbo.
- Can accept both text and voice requests.
- Python-telegram-bot library.
- To translate a voice message into text, use SpeechRecognition library

## Installation
1. Clone the repository or download the source code.
2. In the project directory, create a virtual environment using the command: `python -m venv venv`.
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Linux: `source venv/bin/activate`
4. Install the required Python packages from the `requirements.txt` file using the command: `pip install -r requirements.txt`.
5. Install the Flac utility and FFmpeg:
   - Flac: Install it from https://xiph.org/flac/download.html.
   - FFmpeg: Install it from https://ffmpeg.org/download.html.
6. Create a `.env` file in the project directory with the following content:
   ```
   TELEGRAM_API_KEY=YOUR_TELEGRAM_API_KEY_API_KEY
   OPENAI_API_KEY=YOUR_OPENAI_API_KEY_API_KEY
   ```
   Replace `YOUR_TELEGRAM_API_KEY_API_KEY` and `YOUR_OPENAI_API_KEY_API_KEY` with your actual API keys.

## Usage
1. Activate the virtual environment (if not already activated):
   - Windows: `venv\Scripts\activate`
   - Unix/Linux: `source venv/bin/activate`
2. Run the bot script using the command: `python run_tg_bot.py`.
3. Your Telegram bot is now up and running! You can search for it on Telegram and start interacting with it.

## License
This project is licensed under the [MIT License](LICENSE).


