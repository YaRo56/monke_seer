# import os
# import sys
#
# is_whl_test = False
# if is_whl_test:
#     for i, path in enumerate(sys.path):
#         if path == os.getcwd():
#             del sys.path[i]
#             break

from rnnoise_wrapper import RNNoise
from recorder import recording

recording(3)

denoiser = RNNoise(f_name_lib='librnnoise_5h_ru_500k')

audio = denoiser.read_wav('example.wav')
denoised_audio = denoiser.filter(audio)
denoiser.write_wav('example_denoised.wav', denoised_audio)