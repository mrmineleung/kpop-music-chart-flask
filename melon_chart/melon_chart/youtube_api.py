import ssl

from pytube import Search

ssl._create_default_https_context = ssl._create_unverified_context

def search_data_from_youtube(query):
    s = Search(query).results[0]
    return {'id': s.video_id, 'title': s.vid_info['videoDetails']['title'], 'author': s.vid_info['videoDetails']['author']}

if __name__ == "__main__":
    s = Search('fate gidle').results[0]
    print(s.video_id, s.views, s.title, s.vid_info['videoDetails']['title'] , s.vid_info['videoDetails']['author'], s.caption_tracks, 'MUSIC_VIDEO_TYPE_UGC')

    s = Search('twice one spark').results[0]
    print(s.video_id, s.views, s.title, s.vid_info['videoDetails']['title'] , s.vid_info['videoDetails']['author'], s.caption_tracks, s.vid_info['videoDetails']['musicVideoType'],'MUSIC_VIDEO_TYPE_OMV')
