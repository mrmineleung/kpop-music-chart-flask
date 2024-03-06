# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import json
import logging

from pymongo import MongoClient

from .youtube_data import search


class MelonChartPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def process_item(self, item, spider):
        logging.getLogger('JsonWriterPipeline').info(
            'JsonWriterPipeline : ' + json.dumps(dict(item), ensure_ascii=False))
        try:
            with open(spider.name + '.json', 'w') as fp:
                json.dump(dict(item), fp)
                return item
        except:
            return item


def search_video_id(song_title, song_artists):
    search_result = search(part='snippet', q=song_title + ' ' + song_artists, maxResults=1, type='video')
    if search_result is not None:
        return search_result['items'][0]['id']['videoId']
    return ''


class MongoDBWriterPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'music_charts')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        for row in item['ranking']:
            song_title = row['song_title']
            song_artists = row['song_artists']
            album_name = row['album_name']
            album_image = row['album_image']

            song = self.db.songs.find_one({'song_title': song_title, 'song_artists': song_artists})

            youtube_video_id = ''

            if song is None:
                youtube_video_id = search_video_id(song_title, song_artists)
                self.db.songs.insert_one(
                        {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name,
                         'album_image': album_image, 'youtube_video_id': youtube_video_id})


            if song is not None and song['youtube_video_id'] == '':
                # self.db.songs.insert_one(
                #         {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name,
                #          'album_image': album_image, 'youtube_video_id': youtube_video_id})
                youtube_video_id = search_video_id(song_title, song_artists)
                self.db.songs.update_one(
                    {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image, 'youtube_video_id': ''},
                    {'$set': {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image, 'youtube_video_id': youtube_video_id}})

            # self.db.songs.update_one(
            #     {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image},
            #     {'$setOnInsert': {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image, 'youtube_video_id': youtube_video_id}},
            #     upsert=True)

            if song['youtube_video_id'] != '':
                row['youtube_video_id'] = song['youtube_video_id']
            else:
                row['youtube_video_id'] = youtube_video_id

        if item['type'] == 'TOP100':
            ranking = self.db.rankings.find_one({'type': 'TOP100', 'year': item['year'], 'hour': item['hour']})
            if ranking is None:
                self.db.rankings.insert_one(item)
        elif item['type'] == 'HOT100':
            ranking = self.db.rankings.find_one({'type': 'HOT100', 'year': item['year'], 'hour': item['hour']})
            if ranking is None:
                self.db.rankings.insert_one(item)
        elif item['type'] == 'DAY':
            ranking = self.db.rankings.find_one({'type': 'DAY', 'date': item['date']})
            if ranking is None:
                self.db.rankings.insert_one(item)

        item.pop('_id', None)
        return item

