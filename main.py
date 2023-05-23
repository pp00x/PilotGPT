# Import required libraries to enable the various functionalities of the script
import ast
import logging
import openai
import pyaudio
import subprocess
import sys
import tempfile
import time
import traceback
import yaml
import wave

# Set up logging to track program execution and any errors for better
# debugging and monitoring
logging.basicConfig(level=logging.INFO)

# Function to check if the given code is valid Python code, necessary to
# avoid executing invalid or harmful code


def is_valid_python_code(code):
    if not code:
        return False

    try:
        compile(code, '<string>', 'exec', ast.PyCF_ONLY_AST)
        return True
    except SyntaxError:
        return False
    except Exception as e:
        logging.error("Error compiling Python code: %s", e)
        return False

# Function to record audio and transcribe it, allowing users to interact
# with the program using voice commands


def record_and_transcribe_audio():
    CHUNK = 1024
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as audio_file:
        with wave.open(audio_file.name, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(RATE)
            wav_file.writeframes(b''.join(frames))

    with open(audio_file.name, "rb") as file:
        transcript = openai.Audio.transcribe(
            file=file,
            model="whisper-1",
            response_format="text",
            language="en",
            sample_rate=RATE
        )

    print(f"Command:{transcript}")
    return transcript

# Function to execute the generated Python code, necessary to perform the
# desired action based on user input


def execute_command(python_code):
    try:
        logging.info("Executing command....")

        with open('last_command.py', 'w') as f:
            f.write(python_code)

        subprocess.run([sys.executable, "last_command.py"])

        print("Command successfully executed.")

    except subprocess.CalledProcessError as e:
        logging.error(
            "Command '%s' There was an error running the command %d: %s",
            e.cmd,
            e.returncode,
            e.output)
    except Exception as e:
        logging.error("An error occurred: %s", e)
        logging.error("Traceback: %s", traceback.format_exc())

# Main function to run the program, orchestrating the various components
# and handling user input


def main(config):
    # Clear the console screen to improve readability and focus on the current
    # command
    print("\033[2J\033[H", end="")

    # Set the API key from the configuration file to authenticate with the
    # OpenAI API
    openai.api_key = config["API_KEY"]

    # Load the GPT model from the configuration file
    gpt_model = config.get("GPT_MODEL", "gpt-3.5-turbo")

    # Validate the GPT model and set it to the default if it's invalid
    if gpt_model not in ["gpt-3.5-turbo", "gpt-4"]:
        print("Invalid model name in config file, defaulting to gpt-3.5-turbo")
        gpt_model = "gpt-3.5-turbo"

    # Load the system prompt from the prompt.txt file to provide context for
    # the AI model
    try:
        with open("prompt.txt", "r") as f:
            system_prompt = str(f.read())
    except FileNotFoundError:
        logging.error("Prompt file not found")
        sys.exit(1)
    except PermissionError:
        logging.error("Permission denied while opening prompt file")
        sys.exit(1)

    # Main loop to continuously accept user input and generate code, allowing
    # for ongoing interaction
    while True:
        # Get user input for the input mode (text, audio, or quit) to provide
        # flexibility in user interaction
        input_mode = input(
            "Choose input mode (t for text/ a for audio) or type 'q' to exit:\n").lower()

        if input_mode == "q":
            logging.info("Shutting down")
            break

        # Handle input mode selection and get the user's command, accommodating
        # different input preferences
        if input_mode == 't':
            prompt = input("Type your command here, or quit:\n")
        elif input_mode == 'a':
            try:
                prompt = record_and_transcribe_audio()
            except Exception as e:
                logging.error("Error recording and transcribing audio: %s", e)
                continue
        else:
            logging.warning(
                "Invalid input mode. Please choose 'text' or 'audio'.")
            continue

        # Call the OpenAI API to generate Python code based on the user's
        # command, leveraging AI to automate code generation
        try:
            completion = openai.ChatCompletion.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            logging.error("Error calling OpenAI API: %s", e)
            continue

        response = completion.choices[0].message.content.replace(
            'super', 'win')

        python_code = response

        # Display the generated Python code and execute it if it's valid,
        # providing feedback and executing the desired action
        print(f"Code:\n{python_code}")

        if is_valid_python_code(python_code):
            execute_command(python_code)
        else:
            logging.warning("Invalid Python code received from API. Skipping")
            continue

        # Wait for a specified delay before allowing the next command, giving
        # time for users to review the results
        try:
            delay = int(config.get("NEXT_CMD_DELAY"))
            if delay <= 0:
                raise ValueError("Delay value must be greater than 0")
        except (ValueError, TypeError) as e:
            delay = 6
            print(
                f"Error: {e}. Using default value for now. Check the config file.")

        time.sleep(delay)


# Entry point of the program, responsible for loading the configuration
# and starting the main function
if __name__ == "__main__":

    # Load the configuration file and check for required keys, ensuring the
    # program is properly configured
    try:
        required_keys = [
            "API_KEY",
            "OS",
            "DESK_ENV",
            "WEB_BRO",
            "NEXT_CMD_DELAY"]
        config = yaml.safe_load(open("config.yml", encoding="utf-8"))
        if not all(key in config for key in required_keys):
            logging.error("Required keys missing in the configuration file")
            sys.exit(1)
    except FileNotFoundError:
        logging.error("Config file not found")
        sys.exit(1)
    except Exception as e:
        logging.error("Error loading config file: %s", e)
        sys.exit(1)

    # Run the main function with the loaded configuration, starting the user
    # interaction loop
    main(config)
