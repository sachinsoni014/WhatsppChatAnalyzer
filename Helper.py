from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extracter = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]
        #1.No of messages
        num_messages = df.shape[0]

        # 2.no. of words
        words = []
        for message in df['messages']:
            words.extend(message.split())

        # 3.no. of media messages
        num_media_msgs = df[df['messages'] == "<Media omitted>\n"].shape[0]

        # 3.no. of links

        links = []
        for message in df['messages']:
            links.extend(extracter.find_urls(message))

        return num_messages,len(words),num_media_msgs,len(links)


def busy_user(df):
    x = df['users'].value_counts().head(4)
    df = round((df['users'].value_counts()/ df.shape[0]) * 100, 2).reset_index().rename(
        columns = {'index': 'name', 'users': 'percent'})
    return x,df



def most_commonwords(selected_user, df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    if selected_user != "Group":
        df = df[df['users'] == selected_user]
    words = []
    for message in df['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                from collections import Counter
                Common_words =pd.DataFrame(Counter(words).most_common(20))
    return Common_words


def emoji_Hepler(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def timeline_msgs(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['Year', 'month', 'num_month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time
    return timeline

def timeline_daily(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby(df['date_only']).count()['messages'].reset_index()

    return daily_timeline

def timeline_days(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]

   # df['day_name'].value_counts()
   # day_timeline = df.groupby(df['day_name']).count()['messages'].reset_index()

    return df['day_name'].value_counts()

def tbusy_month(selected_user, df):

    if selected_user != "Group":
        df = df[df['users'] == selected_user]

   # df['day_name'].value_counts()
   # day_timeline = df.groupby(df['day_name']).count()['messages'].reset_index()

    return df['month'].value_counts()





