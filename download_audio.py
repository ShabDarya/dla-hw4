import yt_dlp
from datasets import load_dataset
import subprocess
import os
from tqdm import tqdm

ds = load_dataset("google/MusicCaps", split="train")

def download_clip(ytid: str, start_sec: float, end_sec: float,
                  output_dir: str = '.', filename_template: str = 'audio{ytid}.wav') -> bool:
    cookies_file = 'cookies.txt'
    video_url = f"https://www.youtube.com/watch?v={ytid}"
    output_name = filename_template.format(ytid=ytid)
    output_path = os.path.join(output_dir, output_name)

    duration = end_sec - start_sec
    if duration <= 0:
        with open('logs.txt', 's') as logs:
            logs.write(f"{ytid} - Некорректная длительность: {duration} (start={start_sec}, end={end_sec})\n")
        return False  

    if os.path.exists(output_path):
        with open('logs.txt', 'a') as logs:
            logs.write(f"{ytid} - Файл {output_path} уже существует, пропускаем.\n")
        return True

    try:
        result = subprocess.run(
                ['yt-dlp ',
                '--cookies', cookies_file,
                '--js-runtimes', 'node',
                '--audio-format', 'wav',
                '-x',
                '--download-sections', f'*{start_sec}-{end_sec}',
                '-o',
                output_path,
                video_url],
                capture_output=True, text=True, check=True, encoding='cp1251', errors='replace'
            )
    except subprocess.CalledProcessError as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f"{ytid} - Не удалось получить аудио-ссылку для {ytid}: {e.stderr}\n")
        return False
    return True


dir_audio = './audio'
os.makedirs(dir_audio, exist_ok=True)

with open('logs.txt', 'w') as f:
    pass
with open('./audio/done.txt', 'w') as f:
    pass
with open('./audio/error.txt', 'w') as f:
    pass

for i, row in tqdm(enumerate(ds), total=len(ds)):
    ytid = row['ytid']

    success = download_clip(
    ytid=ytid,
    start_sec=row['start_s'],
    end_sec=row['end_s'],
    output_dir=dir_audio)

    if success:
        with open('./audio/done.txt', 'a') as logs:
            logs.write(f'{ytid}\n')
    else:
        with open('./audio/error.txt', 'a') as logs:
            logs.write(f'{ytid}\n')
