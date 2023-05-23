# PilotGPT
PilotGPT is Python program that enables you to operate your computer using natural languae text or audio input, powered by OpenAI's GPT models (GPT-3.5-turbo and GPT-4). The program utilizes the OpenAI's Whisper to facilitate audio input.

## Usecases:

https://github.com/pp00x/PilotGPT/assets/134364157/86011d89-e363-4e6d-a483-c827b74976fe

### Requirements
### Installation
### Configuration
### Usage
### Features
### Contributing
### License and Author Info

## Requirements
- OpenAI API key is required for this program to work. Go and get your API key from https://platform.openai.com/
- Python 3.11+ is required for this program to work. Install python first. 
- You can install git too if you want to git clone this repository or you can either simply download the zip file.

## Installation

Open ther terminal

Clone the repository:
```git clone https://github.com/pp00x/PilotGPT.git```

Change the current working directory to the project folder:
```cd PilotGPT```

#### Create a virtual environment:

For Windows:
 ```python -m venv venv```
 
For macOS and Linux:
```python3 -m venv venv```

#### Activate the virtual environment:

For Windows:
```venv\Scripts\activate```

For macOS and Linux:
```source venv/bin/activate```

#### Install the required libraries:
```pip install -r requirements.txt```

## Configuration
Update the config.yml file with your settings: 

Replace the placeholders with your actual values.
  
 ```<your-openai-key>```: Your OpenAI API key. You can obtain an API key from OpenAI. Copy your secret API key from your Account Settings and add it to your config.yml file. Make sure not to expose your secret API key to the public.
 
```<your-gpt-model>```: Your preferred GPT model (e.g., "gpt-3.5-turbo", "gpt-4")

```<your-os>```: Your operating system (e.g., "Windows", "macOS", "Linux")

```<your-desktop-environment>```: Your desktop environment (e.g., "GNOME", "KDE", "XFCE"). For Windows and MacOs use version (e.g., "Windows 11", "Big Sur")

```<your-web-browser>```: Your web browser (e.g., "Chrome", "Firefox", "Safari")

```<how-much-delay-between-commands>```: The delay between commands in seconds (e.g., 10)


## Usage
To run the program, activate the virtual environment and execute the following command in your terminal:

```python main.py```

## Features
- Supports text and audio input for user commands
- Uses OpenAI's Whisper for audio input.
- Generates Python code using OpenAI's GPT models (e.g., GPT-3.5-turbo, GPT-4)
- Validates the generated code before execution
- Executes the generated code if valid
- Customizable configuration for operating system, desktop environment, web browser, and command delay
- Logs errors and other information for better debugging and monitoring

## Contributing
This project is open for contributions. If you want to contribute, please follow these steps:

1. Fork the repository and create a new branch for your changes.
2. Make your changes and commit them to your branch.
3. Create a pull request with a description of your changes.
4. Your changes will be reviewed and merged if approved.

## License and Author Info
This project is available under the MIT License. See the LICENSE.txt file for more information.

For any questions or suggestions, feel free to contact the author:

Email: Email
Twitter: Twitter

## Troubleshooting and Edge Cases
If you encounter issues while using the program, consider the following tips for troubleshooting and handling edge cases:

**- Check the API key:** Ensure that your OpenAI API key is correct and has the required permissions. If you have recently regenerated your key, update the config.yml file with the new key.

**- Verify the GPT model:** Make sure you have selected a valid GPT model in the config.yml file. The available models are "gpt-3.5-turbo" and "gpt-4". Double-check the model name for typos.

**- Update dependencies:** Ensure that you have the latest version of the required libraries installed. You can update the libraries by running ```pip install -r requirements.txt``` in your virtual environment.

**- Reinstall the virtual environment:** If the issue persists, try recreating the virtual environment. First, deactivate and delete the current virtual environment using ```deactivate```. Then, follow the installation instructions to create a new virtual environment and install the required libraries.

**- Edge cases with voice commands:** If the program is having trouble understanding your voice commands, try speaking more clearly and slowly. Alternatively, use text input for complex commands or when the program consistently misunderstands your voice input.

**- Unsupported commands:** The program may not be able to generate Python code for certain commands or may produce incorrect code. In such cases, provide more specific or detailed instructions, or try rephrasing your command.

**- Report issues:** If you encounter a bug or issue that cannot be resolved using these tips, consider reporting the issue on the project's GitHub repository by creating a new issue. Provide a detailed description of the problem, including the steps to reproduce it and any relevant log files or error messages.

## Disclaimer
By using this program, you acknowledge and accept the potential risks associated with executing AI-generated code. The developers of this program are not liable for any damages, losses, or issues that may arise from using this program or executing the generated code.
