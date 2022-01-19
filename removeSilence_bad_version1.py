from typing import final
import numpy as np
import matplotlib.pyplot as plt
from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
from time import perf_counter

clip = VideoFileClip("test_short.mp4")  # Subtract audio from video file
print(clip)

clip_audio = clip.audio.to_soundarray(fps=44100)  # Create audio sample array
print(clip_audio)
print(clip_audio.shape)  # test_short has 20 secons so 44100 x 20 is number of rows !!!  (885527, 2)
print(clip_audio.size)

margin_pos = 0.05  # volume cut off margin at positive
margin_neg = -0.05  # volume cut off margin at negative


# PLot the volume levels and margins
# plt.plot(clip_audio, 'b', linewidth=0.5, label='Volume')

# plt.plot(np.ones((len(clip_audio)))*margin_pos,'g',linewidth=0.5, label='Positive Margin')
# plt.plot(np.ones((len(clip_audio)))*margin_neg,'b',linewidth=0.5, label='Negative Margin')
# plt.xlabel('samples',fontsize=15)
# plt.ylabel('amplitude',fontsize=15)
# plt.grid(True)
# plt.legend(loc='upper right', fontsize='small')
# plt.show()

print("Start")
t1_start = perf_counter()
# Store  non-silent sound audio array elements !
order = np.array([])

# Search  clip_audio row by row
for i in range(0, len(clip_audio)):
    if np.abs(clip_audio[i][0]) > margin_pos or np.abs(clip_audio[i][0]) > np.abs(margin_neg):
        order = np.concatenate((order, i), axis=None)
        # print(order)

first_margin = 0.8
right_margin = 0.4
left_margin = 0.4
end_margin = 0.8

beginning = True
memory = 0
clipNewTotal = 0
order_difference = 40000
# print(clip_audio.shape[0])
# print(clip.reader.nframes)
# print(clip.reader.fps)
samples_per_second = clip_audio.shape[0] / clip.reader.nframes * clip.reader.fps
# print(samples_per_second)
# exit()

for i in range(1, len(order)):
    difference = order[i] - order[i - 1]
    if difference > order_difference or i == len(order) - 1:
        if beginning:
            if (
                order[0] / samples_per_second - first_margin <= 0
                and order[i - 1] / samples_per_second + left_margin >= clip.duration
            ):
                clipNewTotal = clip.subclip(order[0] / samples_per_second, order[i - 1] / samples_per_second)
            elif order[0] / samples_per_second - first_margin <= 0:
                clipNewTotal = clip.subclip(
                    order[0] / samples_per_second,
                    order[i - 1] / samples_per_second + left_margin,
                )

            elif order[i - 1] / samples_per_second + left_margin >= clip.duration:
                clipNewTotal = clip.subclip(
                    order[0] / samples_per_second,
                    order[i - 1] / samples_per_second + left_margin,
                )

            else:
                clipNewTotal = clip.subclip(
                    order[0] / samples_per_second - first_margin,
                    order[i - 1] / samples_per_second + left_margin,
                )
                beginning = False
                memory = order[i]
        elif i == len(order) - 1:
            if order[i] / samples_per_second + end_margin >= clip.duration:
                clipNew_temp = clip.subclip(
                    memory / samples_per_second - first_margin,
                    order[i] / samples_per_second,
                )
            else:
                clipNew_temp = clip.subclip(
                    memory / samples_per_second - right_margin,
                    order[i - 1] / samples_per_second + end_margin,
                )
            clipNewTotal = concatenate_videoclips([clipNewTotal, clipNew_temp])
        else:
            clipNew_temp = clip.subclip(
                memory / samples_per_second - right_margin,
                order[i - 1] / samples_per_second + left_margin,
            )
            clipNewTotal = concatenate_videoclips([clipNewTotal, clipNew_temp])
            memory = order[i]

t1_stop = perf_counter()
print("Spent time: ")
print(t1_stop - t1_start)
exit()
clipNewTotal_audio = clipNewTotal.audio.to_soundarray(fps=44100)

plt.plot(clipNewTotal_audio, "b", linewidth=0.5, label="Volume")

plt.plot(np.ones((len(clipNewTotal_audio))) * margin_pos, "g", linewidth=0.5, label="Positive Margin")
plt.plot(np.ones((len(clipNewTotal_audio))) * margin_neg, "b", linewidth=0.5, label="Negative Margin")
plt.xlabel("samples", fontsize=15)
plt.ylabel("volumes", fontsize=15)
plt.grid(True)
plt.legend(loc="upper right", fontsize="small")
plt.show()
