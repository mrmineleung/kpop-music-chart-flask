import scrapy


class BillboardChartBillboard200Spider(scrapy.Spider):
    name = 'billboard_chart_billboard200'
    allowed_domains = ['billboard.com']
    start_urls = ['https://www.billboard.com/charts/billboard-200/']

    def parse(self, response):

        chart = 'Billboard'
        type = 'Billboard200'
        date = response.xpath(
            '//p[@class="c-tagline  a-font-primary-medium-xs u-font-size-11@mobile-max u-letter-spacing-0106 u-letter-spacing-0089@mobile-max lrv-u-line-height-copy lrv-u-text-transform-uppercase lrv-u-margin-a-00 lrv-u-padding-l-075 lrv-u-padding-l-00@mobile-max"]/text()').extract_first().strip()

        result = {'chart': chart, 'type': type, 'date': date, 'ranking': []}

        self.logger.info("A response from %s just arrived!", response.url)
        self.logger.info("Chart: %s ; Type: %s ; Date: %s ", chart, type, date)

        album_image_list = []

        for temp_row in response.xpath(
                '//div[@class="o-chart-results-list-row-container"]/div[contains(@class, "charts-result-detail")]'):
            album_image_temp = temp_row.xpath('div/div/div/@style').re(r'url\(\'([^\)\']+)')
            album_image = None if len(album_image_temp) == 0 else album_image_temp[0]
            album_image_list.append(album_image)

        for key, row in enumerate(response.xpath(
                '//div[@class="o-chart-results-list-row-container"]/ul[contains(@class, "o-chart-results-list-row")]'),
                start=0):

            rank = row.xpath(
                'li[contains(@class, "o-chart-results-list__item")]/span[contains(@class, "a-font-primary-bold-l")]/text()').extract_first().strip()

            rank_changes = row.xpath('li[3]/span/text()').extract_first()
            rank_circle = row.xpath('li[3]/div/svg/g/circle/@fill').extract_first()
            rank_circle_2 = row.xpath('li[3]/div/svg/g/g/circle/@fill').extract_first()

            rank_changes_flow = ''

            if rank_changes is not None:
                rank_changes_flow = rank_changes.strip().replace('\n', '')
            elif rank_circle is not None and rank_circle == '#8289a1':
                rank_changes_flow = None
            elif rank_circle is not None and rank_circle == '#448118':
                rank_changes_flow = '+'
            elif rank_circle_2 is not None and rank_circle_2 == '#b91b20':
                rank_changes_flow = '-'

            album_image = album_image_list[key]
            song_title = row.xpath('li[4]/ul/li/h3/text()').extract_first().strip()
            song_artists = row.xpath('li[4]/ul/li/span/text()').extract_first().strip()
            last_week_position = row.xpath('li[4]/ul/li[4]/span/text()').extract_first().strip()
            peak_position = row.xpath('li[4]/ul/li[5]/span/text()').extract_first().strip()
            weeks_on_chart = row.xpath('li[4]/ul/li[6]/span/text()').extract_first().strip()

            rank_changes_position = ''

            if last_week_position != '-':
                rank_changes_position = abs(int(rank) - int(last_week_position))

            result['ranking'].append({
                'rank': rank,
                'rank_changes_flow': rank_changes_flow,
                'rank_changes_position': rank_changes_position,
                'album_image': album_image,
                'song_title': song_title,
                'song_artists': song_artists,
                'last_week_position': last_week_position,
                'peak_position': peak_position,
                'weeks_on_chart': weeks_on_chart
            })

        return result
