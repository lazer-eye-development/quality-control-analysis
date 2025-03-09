# Quality Control Image Analysis

A Streamlit application for analyzing and comparing images for quality control purposes using OpenAI's vision capabilities.

![image](https://github.com/user-attachments/assets/676a344a-ae4c-47f1-8f57-f88f68a7004a)

## Overview

This application allows quality control teams to:
- Upload reference "good" and "bad" sample images with descriptions
- Analyze new images against these references
- Get detailed AI assessments of potential quality issues
- Browse and analyze images from a local folder

## Features

- **Few-shot learning**: Teach the AI what "good" and "bad" looks like with examples
- **Detailed analysis**: Get comprehensive assessments of potential defects
- **Model selection**: Choose between different OpenAI vision models
- **Local folder integration**: Analyze images directly from your quality control image folder
- **Results saving**: Save analysis results for documentation

## Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key with access to GPT-4o or GPT-4-vision-preview
- Image folders for quality control samples

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lazer-eye-development/quality-control-analysis.git
cd quality-control-analysis
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

4. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

### Setting Up Reference Images

1. **Add Good Examples**:
   - Specify the number of "good" reference images you want to add
   - Upload each image and provide a description of why it's considered good
   - These descriptions will help the AI understand quality standards

2. **Add Bad Examples**:
   - Specify the number of "bad" reference images
   - Upload each image and provide a description of the defects or issues
   - Be specific about what makes these examples unacceptable

### Analyzing Images

1. **Upload a new image** for analysis
2. **Select the OpenAI model** you want to use
3. **Click "Analyze Image"** to get a detailed assessment
4. **Save the results** if needed for documentation

### Using Local Folder

1. **Enter the path** to your quality control image folder
2. **Select an image** from the dropdown menu
3. **Click "Analyze Local Image"** to assess it against your references

## Requirements

- streamlit
- openai
- python-dotenv
- pillow
- requests
