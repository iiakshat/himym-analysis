---
title: himym-analysis
app_file: app.py
sdk: gradio
sdk_version: 4.36.1
---
# HOW I MET YOUR MOTHER - SERIES ANALYSIS

![project3](https://github.com/user-attachments/assets/21f729dc-0767-4174-b4cc-b52c20519184)

## Overview
The HIMYM Analysis project is a web application designed to analyze themes and character networks in the TV series "How I Met Your Mother" using subtitles or scripts. 
This project leverages `gradio` for the web interface, allowing users to perform theme classification and generate character networks interactively.

## Features
### 1. __Theme Classification (Zero Shot Classifier):__
- Input a list of themes.
- Upload subtitles or scripts.
- Visualize the distribution of themes in the series using a bar chart.

![{5E844593-2CAB-4712-94A4-450DD7627EF3}](https://github.com/user-attachments/assets/28fad21e-0bcb-46f9-9b77-768a1c6b917e)
 

### 2. __Character Network:__
- Generate and visualize character interaction networks.
- Extract named entities from subtitles or scripts to create character networks.

![{43A0A626-DDE2-4297-96D8-EE918B4A4E08}](https://github.com/user-attachments/assets/643b7927-2d31-4873-a353-6c57585534dc)

### 3. __Talk To Barney:__
- Ask anything from Barney and the answer is gonna be legend- wait for it, -dary.


## Installation
__Clone the repository:__
```bash
git clone https://github.com/iiakshat/himym-analysis.git
cd HIMYM-Analysis
```

__Install the required Python packages:__

```bash
pip install -r requirements.txt
```

## Usage
__To run the application, execute the following command:__
```bash
python app.py
```

The web application will launch, and you will be provided with a URL to access the interface.

## Contributing
- Fork the repository.
- Create a new branch `(git checkout -b feature-branch)`.
- Make your changes and commit them `(git commit -m 'Add some feature')`.
- Push to the branch `(git push origin feature-branch)`.
- Create a new Pull Request.
