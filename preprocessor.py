import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s1[012]:[0-5][0-9]|1[1-9]:[0-5][0-9]'

    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)
    a = {'user_messages': messages, 'message_date': dates}
    df = pd.DataFrame.from_dict(a, orient='index')
    df = df.transpose()
    df.rename(columns={'message_date': 'dates'}, inplace=True)
    df.head(5)

    df['AM/PM'] = df['user_messages'].str.split().str.get(0).astype(str)
    df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%y, %H:%M')
    df = df[1:]

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append[entry[0]]
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df.head(5)
    df['users'] = df['users'].str.split('-').str.get(1).astype(str)
    df['Year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['num_month'] = df['dates'].dt.month
    df['date_only'] = df['dates'].dt.date
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['day_name'] = df['dates'].dt.day_name()
    print(df)
    return df
