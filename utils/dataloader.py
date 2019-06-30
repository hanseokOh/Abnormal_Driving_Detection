import av
import os
import cv2
import random
import numpy as np
import pandas as pd
from PIL import Image

class Imageloader:
    def __init__(self, directory, resize, batch_size=32, batch_per_video=4):
        self.directory = directory
        self.resize = resize
        self.batch_size = batch_size
        self.batch_per_video = batch_per_video


    def autoencoder_loader(self):
        while True:
            selected_video = self._choose_random_video()
            i = 0
            for video in selected_video:
                frame = self._choose_autoencoder_frame(video)
                if i == 0:
                    X = frame
                else:
                    X = np.concatenate((X, frame))
                i += 1

            X /= 255
            yield (X, X)


    def rnn_loader(self, offset_x, offset_y):
        while True:
            selected_video = self._choose_random_video()
            i = 0
            for video in selected_video:
                frame_x, frame_y = self._choose_rnn_frame(video, offset_x, offset_y)
                if i == 0:
                    X = frame_x
                    Y = frame_y
                else:
                    X = np.concatenate((X, frame_x))
                    Y = np.concatenate((Y, frame_y))
                i += 1

            X /= 255
            Y /= 255
            yield (X, Y)


    def _choose_random_video(self):
        video_list = os.listdir(self.directory)
        selected_index = np.random.randint(low=0, high=len(video_list), size=int(self.batch_size / self.batch_per_video))
        selected_video = [video_list[i] for i in selected_index]
        return selected_video


    def _choose_autoencoder_frame(self, video):
        video_path = os.path.join(self.directory, video)
        frame_list = os.listdir(video_path)

        selected_index = np.random.randint(0, len(frame_list), self.batch_per_video)
        selected_frame = np.array([idx_to_array(i, video_path) for i in selected_index])
        return selected_frame


    def _choose_rnn_frame(self, video, offset_x, offset_y):
        video_path = os.path.join(self.directory, video)
        frame_list = os.listdir(video_path)

        selected_index_y = np.random.randint(offset_y, len(frame_list), self.batch_per_video)
        selected_index_x = [[y - offset_y + x for x in range(offset_x)] for y in selected_index_y]
        selected_frame_y = np.array([idx_to_array(i, video_path) for i in selected_index_y])
        selected_frame_x = np.array([[idx_to_array(i, video_path) for i in l] for l in selected_index_x])
        return selected_frame_x, selected_frame_y


def img_to_array(img):
    im = Image.open(img)
    arr = np.array(im)
    return arr

def idx_to_array(idx, video_path):
    img_path = os.path.join(video_path, '{}.png'.format(idx))
    im = Image.open(img_path)
    arr = np.array(im)
    return arr


class Dataloader:
    def __init__(self, video_directory_path, resize=(64,64,3)):
        self.video_directory_path = video_directory_path
        self.video_list = self._get_video_list()
        self.resize = resize


    def choose_random_video(self):
        random_video = np.random.choice(self.video_list)
        try:
            random_video_frame = self._get_video_frame(random_video)
        except:
            random_video_frame = self._get_video_frame_cv2(random_video)

        random_video_frame = random_video_frame.astype('float32') / 255

        if self.resize:
            random_video_frame = [np.resize(i, self.resize) for i in random_video_frame]
            random_video_frame = np.array(random_video_frame)
        return random_video_frame

    def get_total_frames(self):
        for i in range(len(self.video_list)):
            cctv = self.video_list[i]
            frame = self._get_video_frame(cctv)
            if i == 0:
                total_frame = np.array(frame)
            else:
                total_frame = np.concatenate((total_frame, frame), axis=0)
        return total_frame

    def _get_video_list(self):
        video_list = os.listdir(self.video_directory_path)
        return [os.path.join(self.video_directory_path, i) for i in video_list]


    def _get_video_frame(self, video_path):
        container = av.open(video_path)
        video = container.streams.video[0]
        frames = container.decode(video=0)

        frame_list = []
        for frame in frames:
            img = frame.to_image()
            img = np.array(img)
            frame_list.append(img)
        return np.array(frame_list)


    def _get_video_frame_cv2(self, video_path):
        cap = cv2.VideoCapture(video_path) # video 불러오기
        video_frame_num = int(cap.get(cv2.cv2.CAP_PROP_FRAME_COUNT)) # frame 수

        # capture
        frame_list = []
        for i in range(video_frame_num):
            ret, frame = cap.read()
            frame_list.append(frame)

            if cv2.waitKey(30) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        return np.array(video_frame)
