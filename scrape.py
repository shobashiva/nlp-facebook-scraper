import json
import facebook
import requests
import time
import urllib

FB_APP_ID = 'YOUR_FB_APP_ID'
FB_APP_SECRET = 'YOUR_FB_APP_SECRET'

start_date = '2016-09-19'
end_date = '2017-09-19'
users = ['skittles']

MAX_RETRIES = 10


def get_api():
    args = {
        'grant_type': 'client_credentials',
        'client_id': FB_APP_ID,
        'client_secret': FB_APP_SECRET
    }
   
    token = requests.get("https://graph.facebook.com/oauth/access_token?" + urllib.parse.urlencode(args)).json()["access_token"]
    return facebook.GraphAPI(access_token=token, version=2.7)


def write_to_file(screen_name, date):
    path = f'/YOUR_PATH_HERE/{date}/{screen_name}' # replace with your folder
    with open(path, 'a') as fo:
        for comment in get_comments(screen_name):
            fo.write(json.dumps(comment) + '\n')


def get_comments(screen_name):
    comments = get_api().get_connections(
        screen_name, 
        f'posts?fields=comments&since={start_date}&until={end_date}',
    )
    
    while comments:
        print(comments.get('data', []))
        for comment_json in comments.get('data', []):
            if comment_json.get('comments', None):
                while comment_json['comments']:
                    if 'data' in comment_json['comments']:
                        for i, comment in enumerate(comment_json['comments']['data']):
                            yield comment

                    if 'paging' in comment_json['comments']:
                        if 'next' in comment_json['comments']['paging']:
                            print(f'paging for {screen_name}')
                            comment_json['comments'] = get_or_retry(comment_json['comments']['paging']['next'])
                        else:
                            comment_json['comments'] = None
                    else:
                        comment_json['comments'] = None


        if 'paging' in comments:
            if 'next' in comments['paging']:
                comments = get_or_retry(comments['paging']['next'])
                print(f'moving to next page for {screen_name}')
            else:
                comments = None
        else:
            comments = None

def get_or_retry(url_string):
    retries = MAX_RETRIES
    while retries:
        try:
            values = requests.get(url_string).json()
        except requests.exceptions.ConnectionError as e:
            print('connection error')
            retries -= 1
            time.sleep(3)
            print('...waiting...')
            continue
        except json.JSONDecodeError as e:
            print('json decode error')
            retries -= 1
            time.sleep(3)
            print('...waiting...')
            continue
        else:
            if values:
                return values


if __name__ == "__main__":
    for screen_name in users:
        print(f'running for {screen_name}')
        write_to_file(screen_name, date)