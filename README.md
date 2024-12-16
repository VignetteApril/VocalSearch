
# Non-Real-Time Speech-to-Text and File Retrieval System

This project is a speech-to-text and file retrieval system using **SenseVoice** for audio transcription and **Elasticsearch** for file indexing and searching. Users can upload audio files, transcribe them to text, and search for file names in a specified directory based on the transcription results.

## Features
- **Audio Transcription**: Leverages SenseVoice for high-quality speech-to-text conversion.
- **File Indexing**: Automatically indexes files in a specified folder using Elasticsearch.
- **File Searching**: Retrieves matching file names based on transcription results.
- **User Interface**: A simple and intuitive web interface built with **Gradio**.

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/speech-to-file-retrieval.git
cd speech-to-file-retrieval
```

### 2. Requirements

#### Python Dependencies
Install required Python packages:
```bash
pip install -r requirements.txt
```

#### Elasticsearch
Ensure an Elasticsearch instance is running. If using Docker:
```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.0.0
```

---

## Directory Structure
- **`DOCUMENT_FOLDER`**: Path to the folder containing files to be indexed. Set as `/app/documents` in the code. You can modify this as needed.
- **Model Directory**: The default model directory is `iic/SenseVoiceSmall`. Update the `model_dir` path in the code if necessary.

---

## How to Run

### 1. Index Files
On startup, the system automatically indexes all files in the specified folder (`DOCUMENT_FOLDER`). To manually reindex the files:
- Click the **Index Files** button on the web interface.

### 2. Upload Audio and Retrieve Files
1. Upload an audio file.
2. The system transcribes the audio into text using SenseVoice.
3. It searches for file names in the indexed directory matching the transcription result.
4. The top 5 matching files are displayed for download.

---

## Run the Application

### Local Setup
Run the application locally:
```bash
python app.py
```

Access the interface at `http://localhost:7860`.

### Docker Deployment
Build and run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t speech-to-file-retrieval .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 7860:7860 speech-to-file-retrieval
   ```

Access the interface at `http://localhost:7860`.

---

## API Endpoints
The application includes the following core functionalities:

### 1. File Indexing
- Automatically indexes files from the `DOCUMENT_FOLDER` into Elasticsearch.

### 2. Speech-to-Text Conversion
- Processes audio files using the SenseVoice model and converts them to text.

### 3. File Retrieval
- Searches file names based on the transcribed text and retrieves matching results.

---

## Example Workflow

1. Place files in the `DOCUMENT_FOLDER` directory.
2. Upload an audio file through the web interface.
3. The system transcribes the audio and searches for matching file names.
4. Matching results are displayed as downloadable links.

---

## Technologies Used
- **Gradio**: User interface for file uploads and results display.
- **Elasticsearch**: Indexing and searching files.
- **SenseVoice**: Speech-to-text transcription model.
- **Python**: Core application logic.

---

## Notes
- GPU is recommended for faster transcription. If GPU is unavailable, set `device="cpu"` in the code.
- Ensure Elasticsearch is properly configured and accessible before starting the application.

---

## Contributing
Feel free to fork this repository and contribute. Submit a pull request with improvements or bug fixes.

---
## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
