import pickle
import string
import pandas as pd
# API client library
import googleapiclient.discovery


def get_video_info_by_id(video_id, return_list=False):
    """ 
    Get information about a video using YouTube Data API v3. 
    Parse the following information:
        video_id (str) - video id
        title (str) - video title
        description (str) - video description
        channelId (str) - channel id
        channelTitle (str) - channel title
        publishedAt (str) - video publication date
        tags (str) - tags if author specified, else " " or empty list
        viewCount (int) - number of views
        likeCount (int) - number of likes
        dislikeCount (int) - number of dislikes
        commentCount (int) - number of comments
        comments (str) - 20 video comments
    Parameters:
        video_id (str): YouTube video id
        youtube: googleapiclient.discovery.build object
        return_list (bool): If True, tags and comments are returned as lists of string
                            If False - as one concatenated string

    Returns:
        list, containing all items in the same order OR None in cases:
            if video_id is invalid or if comments are turned off
    """
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyB0YGem5Zq5IYml5Pg3AhkdA1npKEkiUww'
    # API client
    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
    # youtube request for information about video
    request = youtube.videos().list(
        part="snippet, statistics",
        id=video_id)
    response = request.execute()
    
    if not response['items']:
        # empty list - video isn't available anymore
        return None

    # public fields that are 100% availible
    publishedAt = response['items'][0]['snippet']['publishedAt']
    channelId = response['items'][0]['snippet']['channelId']
    title = response['items'][0]['snippet']['title']
    description = response['items'][0]['snippet']['description']
    channelTitle = response['items'][0]['snippet']['channelTitle']

    # next fields can be hidden
    try:
        viewCount = int(response['items'][0]['statistics']['viewCount'])
    except KeyError:
        viewCount = None

    try:
        likeCount = int(response['items'][0]['statistics']['likeCount'])
    except KeyError:
        likeCount = None

    # is private from 13 December 2021
    try:
        dislikeCount = int(response['items'][0]['statistics']['dislikeCount'])
    except KeyError:
        dislikeCount = None

    # tags are unavailable if author didn't specify them
    try:
        tags_list = response['items'][0]['snippet']['tags']
        if return_list:
            tags = tags_list
        else:
            # list to string
            tags = ' '.join([tag for tag in tags_list])
    except KeyError:
        tags = None

    # if commentCount is unavailible, comments are turned off
    try:
        commentCount = int(response['items'][0]['statistics']['commentCount'])
    except KeyError:
        return None

    if commentCount == 0:
        comments = []
    else:
        # youtube request for comments information
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                maxResults=20,
                order="relevance",
                textFormat="plainText",
                videoId=video_id)
            response = request.execute()
        except Exception:
            # comments are unavailable
            return None
        
        if return_list:
            comments = [obj['snippet']['topLevelComment']['snippet']['textDisplay'] for obj in response['items']]
        else:
            # list to string
            comments = ' '.join([obj['snippet']['topLevelComment']['snippet']['textDisplay'] for obj in response['items']])

    return [video_id, title, description, channelId, channelTitle,
            publishedAt, tags, viewCount, likeCount, dislikeCount,
            commentCount, comments]


def request_loop(video_ids, filename, save_iter=False):
    """ 
    Iterate over video_ids and execute `get_video_info_by_id()` function
    Save data to filename_{}.p file using pickle.

    Parameters:
        video_ids (list of strings): list of YouTube video ids
        filename (str): path to file to save data using pickle
        youtube: googleapiclient.discovery.build object 
        save_iter (bool/int): If an integer, save data every save_iter iterations

    Returns:
        number of successful iterations (int)
    """
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyB0YGem5Zq5IYml5Pg3AhkdA1npKEkiUww'
    # API client
    youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=DEVELOPER_KEY)
    youtube_data = []
    total = len(video_ids)
    if not video_ids:
        # empty list
        return 0

    for counter, video_id in enumerate(video_ids):
        try:
            curr = get_video_info_by_id(video_id, youtube)
        except Exception as e:
            print(str(e) + '\n')
            print("This is most likely Http Error 403 due to exceeded quota")
            break

        # append all data in the list
        youtube_data.append(curr)
        # save data every save_iter iterations
        if save_iter and counter != 0 and counter % save_iter == 0:
            pickle.dump(youtube_data, open(f"{filename}_{counter+1}.p", "wb"))

        print(f"{counter+1}/{total}: collect information about {video_id}")

    if youtube_data:
        # if list is not empty
        # save data in the end of the loop or if exception occurs
        pickle.dump(youtube_data, open(f"{filename}_final.p", "wb"))
        print(f'\tSaved in f"{filename}_final.p"')

    return counter


def process_one_list(filename):
    """ Read 'filename' using pickle and convert list of lists to a pd.Dataframe """

    data = pickle.load(open(filename, 'rb'))
    data = list(filter(None, data))  # delete empty list elements

    df = pd.DataFrame(data, columns=['video_id', 'title', 'description', 'channelId', 'channelTitle',
                                     'publishedAt', 'tags',  'viewCount', 'likeCount', 'dislikeCount',
                                     'commentCount', 'comments'])

    return df
