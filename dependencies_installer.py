
import subprocess

# List of packages you want to install
packages = [
    "threading",
    "nltk",
    "simple-dotenv",
    "SpeechRecognition",
    "azure-cognitiveservices-speech",
    "openai"
    # Add more packages as needed
]

def install_packages(package_list):
    for package in package_list:
        try:
            # Use subprocess to run pip install commands
            subprocess.check_call(["pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")

# Call the function to install packages
install_packages(packages)
