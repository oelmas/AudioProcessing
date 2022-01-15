from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip


clip = VideoFileClip("test_short.mp4")  # Subtract audio from video file
print(clip)

clip_audio = clip.audio.to_soundarray(fps=44100)  # Create audio sample array
print(clip_audio)
print(clip_audio.shape)  # test_short has 20 secons so 44100 x 20 is number of rows !!!  (885527, 2)
print(clip_audio.size)

margin_pos = 0.05       # volume cut off margin at positive
margin_neg = -0.05      # volume cut off margin at negative


# PLot the volume levels and margins
plt.plot(clip_audio, 'b', linewidth=0.5, label='Volume')

plt.plot(np.ones((len(clip_audio)))*margin_pos,'g',linewidth=0.5, label='Positive Margin')
plt.plot(np.ones((len(clip_audio)))*margin_neg,'b',linewidth=0.5, label='Negative Margin')
plt.xlabel('samples',fontsize=15)
plt.ylabel('amplitude',fontsize=15)
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')
plt.show()
