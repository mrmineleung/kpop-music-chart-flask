import scrapy


class MelonChartWeekSpider(scrapy.Spider):
    name = 'melon_chart_week'
    allowed_domains = ['melon.com']
    start_urls = ['https://www.melon.com/chart/week/index.htm']

    def parse(self, response):

        chart = 'Melon'
        type = 'WEEK'
        date = response.xpath('//span[@class="yyyymmdd"]/text()').extract_first().strip()

        result = {'chart': chart, 'type': type, 'date': date, 'ranking': []}

        self.logger.info("A response from %s just arrived!", response.url)
        self.logger.info("Chart: %s ; Type: %s ; Date: %s", chart, type, date)

        for row in response.xpath('//*[@class="service_list_song type02 d_song_list"]/table/tbody/tr'):

            rank = row.xpath('td[2]/div[@class="wrap t_center"]/span[@class="rank "]/text()').extract()[0]
            bullet_icon = row.xpath(
                'td[3]/div[@class="wrap"]/span[@class="rank_wrap"]/span[contains(@class, "bullet_icons")]/@class').extract()[
                0].strip()

            rank_changes_position = None
            rank_changes_flow = None

            if bullet_icon == 'bullet_icons rank_up':
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

            # self.logger.info("rank: %s ; rank_changes_flow: %s ; rank_changes_position: %s ; song_title: %s ; "
            #                  "song_artists: %s ; album_name: %s", rank, rank_changes_flow, rank_changes_position,
            #                  song_title, song_artists, album_name)

            result['ranking'].append({
                'rank': rank,
                'rank_changes_flow': rank_changes_flow,
                'rank_changes_position': rank_changes_position,
                'album_image': album_image,
                'song_title': song_title,
                'song_artists': song_artists,
                'album_name': album_name,
            })

        return result
