import json
import pandas as pd
import requests
import praw

subreddit = 'amd'
limit = 100
timeframe = 'day'  # hour, day, week, month, year, all
listing = 'top'  # controversial, best, hot, new, random, rising, top
# Reddit API credentials
client_id = "gK9Ej0iVk_hRYDYog2nF0g",
client_secret = "GPJfjDGs55KjclL0MVFudsa6XPRSRw",
user_agent = "Last_Mastod0n",
redirect_url = "http://localhost:8080",
refresh_token = "XXXXXXXXXXXXXXXXXXXX"

reddit = praw.Reddit(
    client_id="gK9Ej0iVk_hRYDYog2nF0g",
    client_secret="GPJfjDGs55KjclL0MVFudsa6XPRSRw",
    password="Trypt@min3",
    user_agent="testscript by u/Last_Mastod0n",
    username="Last_Mastod0n",
)


def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(base_url, headers={'User-agent': 'yourbot'})
    except:
        print('An Error Occurred')
    return request.json()


def get_post_titles(r):
    '''
    Get a List of post titles
    '''
    posts = []
    for post in r['data']['children']:
        x = post['data']['title']
        posts.append(x)
    return posts


def get_results(r):
    '''
    Create a DataFrame Showing Title, URL, Score and Number of Comments.
    '''
    myDict = {}
    for post in r['data']['children']:
        myDict[post['data']['title']] = {'url': post['data']['url'], 'score': post['data']['score'],
                                         'comments': post['data']['num_comments']}
    df = pd.DataFrame.from_dict(myDict, orient='index')
    return df

def print_posts(reddit, subreddit_name, filename, limit=10, timeframe='hot'):
    subreddit = reddit.subreddit(subreddit_name)

    # Depending on timeframe, call different functions
    if timeframe == 'hot':
        posts = subreddit.hot(limit=limit)
    elif timeframe == 'new':
        posts = subreddit.new(limit=limit)
    elif timeframe == 'top':
        posts = subreddit.top(limit=limit)
    else:
        print("Invalid timeframe. Valid options are 'hot', 'new', 'top'")
        return

    post_list = []
    for post in posts:
        post_dict = {
            'title': post.title,
            'id': post.id,
            'url': post.url
            # Add any other post attributes you're interested in here...
        }
        post_list.append(post_dict)

    with open(filename, 'w') as f:
        json.dump(post_list, f)


if __name__ == '__main__':
    r = get_reddit(subreddit, listing, limit, timeframe)
    df = get_results(r)
    df.to_csv('C:\\Users\\Steven\\Documents\\output.csv', index=False)
    print_posts(reddit, "Python", 'C:\\Users\\Steven\\Documents\\output.csv', limit=5, timeframe='new')
    print(reddit.user.me())
    '''print_posts(reddit, "Python", limit=5, timeframe='new')'''
