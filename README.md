# StyleTTS-2 API
Made with 2 goals in mind for simple StyleTTS2 inference (and maybe training later):

    - A single function to LOAD StyleTTS2
    - A single function to GENERATE StyleTTS2

## Installation
Recommend doing this in a venv.

1. Clone the repo
```
https://github.com/JarodMica/styletts-api.git
```
2. cd into repo and initialize github submodules
```
git submodule init
git submodule update --remote
```
3. Install StyleTTS2 package:
```
pip install modules\StyleTTS2
```
4. Install this repo
```
pip install .
```

## Usage
First, load any StyleTTS2 model with `load_all_models`.  You must follow the format specified here: [Model Folder Structure](#model-folder-structure)
```
from styletts_api.inference.load import load_all_models
model_dict = load_all_models(model_path="path/to/your/model.pth")
```

Finally, call `generate_audio` to return back an audio path.  
```
from styletts_api.inference.generate import generate_audio
audio_path = generate_audio(
    text=text, 
    voice="mel", 
    reference_audio_file="segment_147.wav", 
    seed=100, 
    diffusion_steps=25, 
    alpha=0.7, 
    beta=0.3, 
    embedding_scale=0.5, 
    model_dict=model_dict, 
    voices_root="voices"
    )
```

Parameter           | Type | Description
----------          |------|------------
text                |str   |Text that you'd like to generate
voice               |str   |Voice you'd like to use
reference_audio_file|str   |Audio segment you'd like to use (should be less than 10s long)
seed                |int   |Set to keep model audio output the same, a seed of 2 will (generally) always sound the same for the same settings. Use -1 for random seed.
diffusion_steps     |int   |Larger values may result in higher quality outputs, controls number of denoising steps the model goes through
alpha               |float |Affects speaker timbre, the higher the value, the further it is from the reference sample. At 0, may sound closer to reference sample at the cost of a little quality
beta                |float |Affects speaker prosody and expressiveness. The higher the value, the more exaggerated speech may be.
embedding_scale     |float |Affects speaker expressiveness/emotion. A higher value may result in higher emotion or expression
model_dict          |dict  |Contains a dictionary of all loaded models that are needed for inference
voices_root         |str   |The root directory for where you put speaker voices into, see [Voices Root](#voices-root) for more details

### Model Folder Structure
The folder to the model should contain a StyleTTS2 model.pth and config.yml file.  These are the two files you get from training.  When you specify the model.pth file in load_all_models(), it deduces the path to the config.yml file based on model.pth so they have to be in the same location
```
name_of_model_folder
  ├-model.pth
  └-config.yml
```

### Voices Root
Designed with modularity in mind, you can change voice root anywhere as long as you follow the format below. The folder structure **needs** to be specified with the following structure:
```
name_of_voice_root
|
|--speaker_name1
|   └-reference_audio_of_speaker1.wav
|   
|--speaker_name2
|   └-reference_audio_of_speaker2.wav
```
You must follow this format as the construction to the reference_audio_path is constructed like this:

`reference_audio_path = os.path.join(voices_root, voice, reference_audio_file)`

## Acknowledgements
- Huge thanks to the creator of [StyleTTS2!](https://github.com/yl4579/StyleTTS2)