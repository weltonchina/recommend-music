from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import io

from surprise import KNNBaseline, Reader
from surprise import Dataset

import cPickle as pickle
# 重建歌单id到歌单名的映射字典
id_name_dic = pickle.load(open("popular_playlist.pkl","rb"))
print("加载歌单id到歌单名的映射字典完成...")
# 重建歌单名到歌单id的映射字典
name_id_dic = {}
for playlist_id in id_name_dic:
    name_id_dic[id_name_dic[playlist_id]] = playlist_id
print("加载歌单名到歌单id的映射字典完成...")


file_path = os.path.expanduser('./popular_music_suprise_format.txt')
# 指定文件格式
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
music_data = Dataset.load_from_file(file_path, reader=reader)
# 计算歌曲和歌曲之间的相似度
print("构建数据集...")
trainset = music_data.build_full_trainset()
#sim_options = {'name': 'pearson_baseline', 'user_based': False}



# 重建歌曲id到歌曲名的映射字典
song_id_name_dic = pickle.load(open("popular_song.pkl","rb"))
print("加载歌曲id到歌曲名的映射字典完成...")
# 重建歌曲名到歌曲id的映射字典
song_name_id_dic = {}
for song_id in song_id_name_dic:
    song_name_id_dic[song_id_name_dic[song_id]] = song_id
print("加载歌曲名到歌曲id的映射字典完成...")


import cPickle as pickle
# 重建歌曲id到歌曲名的映射字典
song_id_name_dic = pickle.load(open("popular_song.pkl","rb"))
print("加载歌曲id到歌曲名的映射字典完成...")
# 重建歌曲名到歌曲id的映射字典
song_name_id_dic = {}
for song_id in song_id_name_dic:
    song_name_id_dic[song_id_name_dic[song_id]] = song_id
print("加载歌曲名到歌曲id的映射字典完成...")


user_inner_id = 4
user_rating = trainset.ur[user_inner_id]
items = map(lambda x:x[0], user_rating)
for song in items:
    print(algo.predict(algo.trainset.to_raw_uid(user_inner_id), algo.trainset.to_raw_iid(song), r_ui=1), song_id_name_dic[algo.trainset.to_raw_iid(song)])