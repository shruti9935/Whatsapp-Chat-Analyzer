from urlextract import URLExtract
from wordcloud import WordCloud
import  pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):

    # decide which dataframe to work on
    temp_df = df
    if selected_user != 'Overall':
        temp_df = df[df['user'] == selected_user]

    # now compute stats on temp_df (always defined)
    num_messages = temp_df.shape[0]

    words = []
    for message in temp_df['message']:
        words.extend(message.split())

    num_media_messages = temp_df[temp_df['message'].str.contains('<Media omitted>', na=False)].shape[0]

    links = []
    for message in temp_df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # join all messages into one string
    text = df['message'].str.cat(sep=' ')

    # build the wordcloud
    wc = WordCloud(width=800, height=400, background_color='white')
    df_wc = wc.generate(text)

    return df_wc

def most_common_words(selected_user, df):

    with open('stop_hinglish.txt','r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():  # Split messages into words
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create a new list "time" with Month-Year values
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_message(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_message = df.groupby('only_date').size().reset_index(name='message')
    daily_message.rename(columns={'only_date': 'time'}, inplace=True)

    return daily_message


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap
