import os, requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def search(**params):
    url = os.environ.get('YOUTUBE_DATA_API_URL')
    params['key'] = os.environ.get('YOUTUBE_DATA_API_KEY')

    try:
        response = requests.get(url, params=params)

        if response.status_code != 200:
            logger.error(response.json())

            if response.json()['error']['errors'][0]['reason'] == 'quotaExceeded':
                return retry_search_with_spare_token(**params)
            return None

        return response.json()
    except requests.exceptions.HTTPError:
        logger.exception("HTTP Error")
        return None
    except requests.exceptions.ConnectionError:
        logger.exception("Error Connecting")
        return None
    except requests.exceptions.Timeout:
        logger.exception("Timeout Error")
        return None
    except requests.exceptions.RequestException:
        logger.exception("RequestException raised")
        return None


def retry_search_with_spare_token(**params):
    logger.info('Retrying spare API Key')
    url = os.environ.get('YOUTUBE_DATA_API_URL')
    params['key'] = os.environ.get('YOUTUBE_DATA_API_KEY_SPARE')
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    return response.json()



if __name__ == '__main__':
    data = search(part='snippet', q='I GOT YOU', maxResults=1, type='video')
    print(data)
