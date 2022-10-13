#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install google-api-python-client


# In[3]:


from googleapiclient.discovery import build


# In[6]:


import pandas as pd 
import seaborn as sns


# # introduction 
# 
# In this project we'll access the data of some channels and compare their growth. 

# In[5]:


api_key = "AIzaSyAUSkJIQeO98eHHFn2FxVoZZE7XXnOrhjE"
channel_id = "UCNjPtOCvMrKY5eLwr_-7eUg"

# to raise a request to the api we need youtube service 
# build("service Name", "version", "Api key")

youtube_service = build("youtube", "v3", developerKey = api_key) # this creates a service


# ## now we build a function to extract the channel details
# 
# * to get the channel details 

# In[7]:


def get_channel_stats(youtube_service, channel_id):
    
    request = youtube_service.channels().list(
        part="snippet,contentDetails,statistics",
        id="UCNjPtOCvMrKY5eLwr_-7eUg",
        #managedByMe=False
    )
    
    response = request.execute()
    return response
    


# In[8]:


get_channel_stats(youtube_service, channel_id)


# ## output analysis
# 
# the above output we have got is dictionary in json format, to read it more clearly we open a json formator (https://jsonformatter.curiousconcept.com/#) in our browser.

# In[9]:


# extracting data from the json output 

def get_channel_stats_2(youtube_service, channel_id):
    
    all_channel_data = []
    request = youtube_service.channels().list(
        part="snippet,contentDetails,statistics",
        id=["UCNjPtOCvMrKY5eLwr_-7eUg", # alux 
            "UCO5QSoES5yn2Dw7YixDYT5Q",  # aperture
            "UC4QZ_LsYcvcq7qOsOhpAX4A",  # cold fusion
            "UCIlU5KDHKFSaebYviKfOidw"   # news_think
           ]
        #managedByMe=False
    )
    
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict( name = response['items'][i]['snippet']['title'],
                         subscribers = response['items'][i]['statistics']['subscriberCount'],
                         views = response['items'][i]['statistics']['viewCount'],
                         no_of_videos = response['items'][i]['statistics']['videoCount'],
                         playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                   )
        all_channel_data.append(data)
    return all_channel_data 
              


# In[10]:



channel_stats = get_channel_stats_2 (youtube_service, channel_id)


# In[11]:


data_df = pd.DataFrame(channel_stats)


# In[12]:


data_df


# In[13]:


data_df.dtypes


# we need to change the data type to integers before we do make any visualization in this data.

# In[14]:


data_df["subscribers"] = pd.to_numeric(data_df["subscribers"])
data_df["views"] = pd.to_numeric(data_df["views"])
data_df["no_of_videos"] = pd.to_numeric(data_df["no_of_videos"])


# # Now we will visualize the data using seaborn liberary

# In[15]:


# whi=o has the most subscribers

sns.set(rc={'figure.figsize':(7,7)})
ax = sns.barplot(x = "name", y = "subscribers", data = data_df)


# In[16]:


# who has the most video views 

ax= sns.barplot(x="name", y="views", data=data_df)


# In[17]:


# who posted the most no. of videos

ax = sns.barplot(x="name", y="no_of_videos", data=data_df)


# ## we will scrape out the video data from the alux.com and try to analyse it 

# In[18]:


data_df


# In[ ]:


playlist_id = data_df['playlist_id'][1]
playlist_id 


# In[ ]:


# function to get video id 

def get_vid_id (youtube_service, playlist_id):
    
    video_ids = []
    request = youtube_service.playlistItems().list(
      part = 'contentDetails',
        playlistId = playlist_id,
        maxResults = 5)
    response = request.execute()
    for i in range(len(response['items'])):
        video_id = response['items'][i]['contentDetails']['videoId']
        video_ids.append(video_id)
    
    
    next_page_token = response['nextPageToken']
    more_pages = True 
    
    while more_pages:
                if next_page_token is None:
                    more_pages = False
                else:
                    request = youtube_service.playlistItems().list(
                        part = 'contentDetails',
                        playlistId = playlist_id,
                        maxResults = 5,
                        pageToken = next_page_token)
                    response = request.execute()
                    for i in range(len(response['items'])):
                          video_id = response['items'][i]['contentDetails']['videoId']
                video_ids.append(video_id)
                next_page_token = response.get('nextPageToken')
    
    print(video_ids)


# In[ ]:


video_data = get_vid_id (youtube_service, playlist_id)







# In[ ]:




