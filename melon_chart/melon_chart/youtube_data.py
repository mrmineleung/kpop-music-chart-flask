import os, requests
import logging
from dotenv import load_dotenv

load_dotenv()

def search(**params):
    url = 'https://youtube.googleapis.com/youtube/v3/search?'
    params['key'] = os.environ.get('YOUTUBE_DATA_API_KEY')
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logging.error(response)

        if response.json()['error']['errors'][0]['reason'] == 'quotaExceeded':
            logging.info('Retrying spare API Key')
            params['key'] = os.environ.get('YOUTUBE_DATA_API_KEY_SPARE')
            response = requests.get(url, params=params)
            if response.status_code != 200:
                logging.error(response)
                return None
            return response.json()
        return None

    return response.json()


if __name__ == '__main__':
    data = search(part='snippet', q='I GOT YOU', maxResults=1, type='video')
    print(data)
