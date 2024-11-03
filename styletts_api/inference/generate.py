import os
import time
import numpy as np

from scipy.io.wavfile import write

from styletts2.utils import *

# Stolen and modifed from my webui https://github.com/JarodMica/StyleTTS-WebUI/blob/master/webui.py 
def generate_audio(text, voice, reference_audio_file, seed, diffusion_steps, alpha, beta, embedding_scale, model_dict, output_audio_path="results/output.wav", device="cuda", voices_root="voices/styletts", ):
    global_phonemizer = model_dict["global_phonemizer"]
    model = model_dict["model"]
    model_params = model_dict["model_params"]
    sampler = model_dict["sampler"]
    textcleaner = model_dict["textcleaner"]
    to_mel = model_dict["to_mel"]
    
    reference_audio_path = os.path.join(voices_root, voice, reference_audio_file)
    reference_dicts = {f'{voice}': f"{reference_audio_path}"}
    # noise = torch.randn(1, 1, 256).to(device)
    set_seeds(seed)
    start = time.time()
    for k, path in reference_dicts.items():
        mean, std = -4, 4
        ref_s = compute_style(path, model, to_mel, mean, std, device)

        texts = split_and_recombine_text(text)
        audios = []
        
        # wav1 = inference(text, ref_s, model, sampler, textcleaner, to_mel, device, model_params, global_phonemizer=global_phonemizer, alpha=alpha, beta=beta, diffusion_steps=diffusion_steps, embedding_scale=embedding_scale)
        for t in texts:
            audios.append(inference(t, ref_s, model, sampler, textcleaner, to_mel, device, model_params, global_phonemizer=global_phonemizer, alpha=alpha, beta=beta, diffusion_steps=diffusion_steps, embedding_scale=embedding_scale))

        rtf = (time.time() - start)
        print(f"RTF = {rtf:5f}")
        print(f"{k} Synthesized:")
        os.makedirs("results", exist_ok=True)
        # audio_opt_path = os.path.join("results", f"{voice}_output.wav")
        write(output_audio_path, 24000, np.concatenate(audios))
    

    return output_audio_path