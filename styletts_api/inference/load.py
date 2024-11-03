from styletts2.utils import *

# Stolen and modifed from my webui https://github.com/JarodMica/StyleTTS-WebUI/blob/master/webui.py 
def load_all_models(model_path, device="cuda"):
    model_config = get_model_configuration(model_path)
    if not model_config:
        return None
    
    config = load_configurations(model_config)
    sigma_value = config['model_params']['diffusion']['dist']['sigma_data']
    
    model, model_params = load_models_webui(sigma_value, device)
    global_phonemizer = load_phonemizer()
    sampler = create_sampler(model)
    textcleaner = TextCleaner()
    to_mel = torchaudio.transforms.MelSpectrogram(
        n_mels=80, n_fft=2048, win_length=1200, hop_length=300)
    
    load_pretrained_model(model, model_path=model_path)

    return {
        "global_phonemizer": global_phonemizer,
        "model": model,
        "model_params": model_params,
        "sampler": sampler,
        "textcleaner": textcleaner,
        "to_mel": to_mel
    }


def get_model_configuration(model_path):
    base_directory, _ = os.path.split(model_path)
    for file in os.listdir(base_directory):
        if file.endswith(".yml"):
            configuration_path = os.path.join(base_directory, file)
            return configuration_path
    
    raise Exception("Configuration file not found for chosen styletts model!")
