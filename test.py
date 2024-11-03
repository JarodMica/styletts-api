
from styletts_api.inference.generate import generate_audio
from styletts_api.inference.load import load_all_models


model_dict = load_all_models(model_path="engines/styletts2/mel/epoch_2nd_00029.pth")

text= "Hey there, how are you doing?  My name is Melonuh and I'm here to take you through your journey.  Ready to get started?"

generate_audio(text=text, 
               voice="mel", 
               reference_audio_file="segment_147.wav", 
               seed=100, 
               diffusion_steps=25, 
               alpha=0.7, 
               beta=0.3, 
               embedding_scale=0.5, 
               model_dict=model_dict, 
               voices_root="voices")