#coding: utf-8
import json
import sys
import surprise 
import lightfm
import cPickle as pickle



def parse_song_line(in_line):
	data = json.loads(in_line)
	name = data['result']['name']
	tags = ",".join(data['result']['tags'])
	subscribed_count = data['result']['subscribedCount']
	if(subscribed_count<100):
		return False
	playlist_id = data['result']['id']
	song_info = ''
	songs = data['result']['tracks']
	for song in songs:
		try:
			song_info += "\t"+":::".join([str(song['id']),song['name'],song['artists'][0]['name'],str(song['popularity'])])
		except Exception, e:
			#print e
			#print song
			continue
	return name+"##"+tags+"##"+str(playlist_id)+"##"+str(subscribed_count)+song_info

def parse_file(in_file, out_file):
	out = open(out_file, 'w')
	for line in open(in_file):
		result = parse_song_line(line)
		if(result):
			out.write(result.encode('utf-8').strip()+"\n")
	out.close()



def is_null(s): 
	return len(s.split(","))>2

def parse_song_info(song_info):
	try:
		song_id, name, artist, popularity = song_info.split(":::")
		#return ",".join([song_id, name, artist, popularity])
		return ",".join([song_id,"1.0",'1300000'])
	except Exception,e:
		#print e
		#print song_info
		return ""

def parse_playlist_line(in_line):
	try:
		contents = in_line.strip().split("\t")
		name, tags, playlist_id, subscribed_count = contents[0].split("##")
		songs_info = map(lambda x:playlist_id+","+parse_song_info(x), contents[1:])
		songs_info = filter(is_null, songs_info)
		return "\n".join(songs_info)
	except Exception, e:
		print e
		return False
		

def parse_file(in_file, out_file):
	out = open(out_file, 'w')
	for line in open(in_file):
		result = parse_playlist_line(line)
		if(result):
			out.write(result.encode('utf-8').strip()+"\n")
	out.close()


def parse_playlist_get_info(in_line, playlist_dic, song_dic):
	contents = in_line.strip().split("\t")
	name, tags, playlist_id, subscribed_count = contents[0].split("##")
	playlist_dic[playlist_id] = name
	for song in contents[1:]:
		try:
			song_id, song_name, artist, popularity = song.split(":::")
			song_dic[song_id] = song_name+"\t"+artist
		except:
			print "song format error"
			print song+"\n"

		

def parse_file(in_file, out_playlist, out_song):
	#从歌单id到歌单名称的映射字典
	playlist_dic = {}
	#从歌曲id到歌曲名称的映射字典
	song_dic = {}
	for line in open(in_file):
		parse_playlist_get_info(line, playlist_dic, song_dic)
	#把映射字典保存在二进制文件中
	pickle.dump(playlist_dic, open(out_playlist,"wb")) 
	#可以通过 playlist_dic = pickle.load(open("playlist.pkl","rb"))重新载入
	pickle.dump(song_dic, open(out_song,"wb"))	