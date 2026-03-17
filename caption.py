from datasets import load_dataset
import ollama
import os
import json
import re
from tqdm import tqdm

ds = load_dataset("google/MusicCaps", split="train")

base_prompt = '''Generate JSON based on the description. Here are some examples:
description: An epic and triumphant orchestral soundtrack featuring powerful brass and a sweeping string ensemble, driven by a fast march-like rhythm and an epic background choir, recorded with massive stadium reverb.
json: {
"description": "An epic and triumphant orchestral soundtrack featuring powerful brass and a sweeping string ensemble, driven by a fast march-like rhythm and an epic background choir, recorded with massive stadium reverb.",
"general_mood": "Epic, heroic, triumphant, building tension",
"genre_tags": ["Cinematic", "Orchestral", "Soundtrack"],
"lead_instrument": "Powerful brass section (horns, trombones)",
"accompaniment": "Sweeping string ensemble, heavy cinematic percussion, timpani",
"tempo_and_rhythm": "Fast, driving, march-like rhythm",
"vocal_presence": "Epic choir in the background (wordless chanting)",
"production_quality": "High fidelity, wide stereo image, massive stadium reverb"
}

description: An energetic progressive house dance track with a bright detuned synthesizer lead, pumping sidechain bass, and chopped vocal samples over a fast four-on-the-floor beat.
json: {
"description": "An energetic progressive house dance track with a bright detuned synthesizer lead, pumping sidechain bass, and chopped vocal samples over a fast four-on-the-floor beat.",
"general_mood": "Energetic, uplifting, party vibe, euphoric",
"genre_tags": ["EDM", "Progressive House", "Dance"],
"lead_instrument": "Bright, detuned synthesizer lead",
"accompaniment": "Pumping sidechain bass, risers, crash cymbals",
"tempo_and_rhythm": "Fast, driving, strict four-on-the-floor beat",
"vocal_presence": "Chopped vocal samples used as a rhythmic instrument",
"production_quality": "Modern, extremely loud, punchy, club-ready mix"
}

description: '''

folder_path = './audio'
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
ytids = [f[5:-4] for f in files if '.wav' in f]
ytid_to_row = {item['ytid']: item for item in ds}

with open('capt_audio.txt', 'w') as f:
    pass

dir_audio = './audio/'

for y in tqdm(ytids):
    try:
        file_name = dir_audio + y + '.json'
        if os.path.exists(file_name):
            continue

        response = ollama.chat(model='gemma3:4b', messages=[
        {'role': 'system', 'content': 'You write only json'},
        {'role': 'user', 'content': base_prompt + ytid_to_row[y]['caption']}],
        options={
        'keep_alive': '10m'})

        content_str = response['message']['content']

        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content_str, re.DOTALL | re.IGNORECASE)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = response['message']['content'].strip()

        

        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(json.loads(json_str), f, ensure_ascii=False, indent=2)

    except:
        with open('capt_audio.txt', 'a') as f:
            f.write(y+'\n')
        
    