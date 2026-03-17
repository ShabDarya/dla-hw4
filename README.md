# Fine-tuning MusicGen

## About

This repository contains code for downloading audio from [MusicCaps](https://huggingface.co/datasets/google/MusicCaps) and creating json for fine-Tuning.

See the task assignment [here](https://github.com/NickKar30/DLA-HSE-AI-masters-course/tree/main/hw/hw4).

##Installation
Follow these steps to install the project:

0. (Optional) Create and activate new environment using [`conda`](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) or `venv` ([`+pyenv`](https://github.com/pyenv/pyenv)).

   a. `conda` version:

   ```bash
   # create env
   conda create -n project_env python=3.10

   # activate env
   conda activate project_env
   ```

   b. `venv` (`+pyenv`) version:

   ```bash
   # create env
   ~/.pyenv/versions/PYTHON_VERSION/bin/python3 -m venv project_env

   # alternatively, using default python version
   python3 -m venv project_env

   # activate env
   source project_env/bin/activate
   ```

1. Install all required packages

   ```bash
   pip install -r requirements.txt
   ```

 2. Download [yt-dlp.exe](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation) to project path.


## How To Use
To download audio, run following code:
  ```bash
  python download_audio.py
   ```
  
  To create captions for audio, run following code:
  ```bash
  python caption.py
   ```
     
