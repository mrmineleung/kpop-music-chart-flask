import scrapy
import time

from apscheduler.schedulers.twisted import TwistedScheduler
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings


# from extensions import mongo_db
# from service import youtube_data

class MelonChartHot100Spider(scrapy.Spider):
    name = 'melon_chart_hot100'
    allowed_domains = ['melon.com']
    start_urls = ['https://www.melon.com/chart/hot100/index.htm']

    def parse(self, response):

        chart = 'Melon'
        type = response.xpath('//div[@class="page_header"]/h2[@class="title"]/text()').extract_first()
        year = response.xpath('//span[@class="year"]/text()').extract_first()
        hour = response.xpath('//span[@class="hour"]/text()').extract_first()

        result = {'chart': chart, 'type': type, 'year': year, 'hour': hour, 'ranking': []}

        self.logger.info("A response from %s just arrived!", response.url)
        self.logger.info("Chart: %s ; Type: %s ; Year: %s ; Hour: %s", chart, type, year, hour)

        for row in response.xpath('//*[@class="service_list_song type02 d_song_list"]/table/tbody/tr'):

            rank = row.xpath('td[2]/div[@class="wrap t_center"]/span[@class="rank "]/text()').extract()[0]
            bullet_icon = row.xpath(
                'td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[contains(@class, "bullet_icons")]/@class').extract()[
                0].strip()

            rank_changes_position = ''
            rank_changes_flow = ''

            if bullet_icon == 'bullet_icons rank_static':
                rank_changes_flow = None
                rank_changes_position = None
            elif bullet_icon == 'bullet_icons rank_up':
                # rank_changes = '+' + row.xpath('td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[@class="up"]/text()').extract()[0]
                rank_changes_flow = '+'
                rank_changes_position = \
                    row.xpath('td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[@class="up"]/text()').extract()[0]
            elif bullet_icon == 'bullet_icons rank_down':
                rank_changes_flow = '-'
                rank_changes_position = \
                    row.xpath('td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[@class="down"]/text()').extract()[
                        0]

            album_image = row.xpath('td[4]/div[@class="wrap"]/a[@class="image_typeAll"]/img/@src').extract()[0]
            song_title = row.xpath(
                'td[6]/div[@class="wrap"]/div[@class="wrap_song_info"]/div[@class="ellipsis rank01"]/span/a/text()').extract()[
                0]
            song_artists = row.xpath(
                'td[6]/div[@class="wrap"]/div[@class="wrap_song_info"]/div[@class="ellipsis rank02"]/span/a/text()').extract()[
                0]
            album_name = row.xpath(
                'td[7]/div[@class="wrap"]/div[@class="wrap_song_info"]/div[@class="ellipsis rank03"]/a/text()').extract()[
                0]
            # print(rank)
            # print(rank_changes)
            # print(row.xpath('td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[@class, "up"]/text()').extract())
            # print(row.xpath('td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[@class, "down"]/text()').extract())
            # print(album_image)
            # print(song_title)
            # print(song_singers)
            # print(album_name)
            self.logger.info("rank: %s ; rank_changes_flow: %s ; rank_changes_position: %s ; song_title: %s ; "
                             "song_artists: %s ; album_name: %s", rank, rank_changes_flow, rank_changes_position,
                             song_title, song_artists, album_name)

            # record = mongo_db.songs.find_one({'song_title': song_title, 'song_artists': song_artists})
            # youtube_url = None
            # if record is None:
            #     youtube_url = youtube_data.youtube_search(part='snippet', q=song_title, maxResults=1, type='video')
            #     mongo_db.songs.insert_one(
            #         {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name,
            #          'album_image': album_image, 'youtube_url': youtube_url})
            #
            # if youtube_url is None and record is not None:
            #     youtube_url = record['youtube_url']

            result['ranking'].append({
                'rank': rank,
                'rank_changes_flow': rank_changes_flow,
                'rank_changes_position': rank_changes_position,
                'album_image': album_image,
                'song_title': song_title,
                'song_artists': song_artists,
                'album_name': album_name,
                # 'youtube_url': youtube_url
            })

            # mongo_db.song.update(
            #     {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image},
            #     {'$setOnInsert': {'song_title': song_title, 'song_artists': song_artists, 'album_name': album_name, 'album_image': album_image}},
            #     {'upsert': True})

            # yield {
            #     'rank': rank,
            #     'rank_changes': rank_changes,
            #     'album_image': album_image,
            #     'song_title': song_title,
            #     'song_singers': song_singers,
            #     'album_name': album_name
            # }

        # yield {
        #     'year': year,
        #     'hour': hour
        # }

        return result

    # # function to run the spider
    # def crawl_melon_chart(self):
    #     self.logger.info("Running scrapy crawl melon_chart...")
    #     cmdline.execute("scrapy crawl melon_chart".split())
    #
