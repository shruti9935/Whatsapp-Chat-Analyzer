import re
import pandas as pd

def preprocessor(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?:\s*(?:am|pm))?\s*-\s*'

    message_pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?:\s*(?:am|pm))?\s*-\s*)(.*)'
    messages_and_dates = re.findall(message_pattern, data, flags=re.IGNORECASE)
    messages_and_dates

    dates = re.findall(pattern, data, flags=re.IGNORECASE)
    print("Found", len(dates), "date/time stamps. Example:", dates)

    dates = [item[0] for item in messages_and_dates]
    messages = [item[1] for item in messages_and_dates]

    df = pd.DataFrame({'user_messages': messages, 'messages_date': dates})
    df['messages_date'] = pd.to_datetime(df['messages_date'], format='%d/%m/%Y, %I:%M %p - ', errors='coerce')
    df.rename(columns={'messages_date': 'date'}, inplace=True)
    df.head()

    users = []
    messages_list = []
    for date_message_tuple in messages_and_dates:
        message = date_message_tuple[1]  # Get the message part from the tuple
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # If there is a user (split was successful)
            users.append(entry[1])
            messages_list.append(entry[2])
        else:  # If it's a group notification or system message
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list
    if 'user_messages' in df.columns:
        df.drop(columns=['user_messages'], inplace=True)
    df.head()
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df