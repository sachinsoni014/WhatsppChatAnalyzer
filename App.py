import streamlit as st
import preprocessor, Helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    #fetching the unique users

    user_list = df['users'].unique().tolist()
    #user_list - it's a python list
    user_list.sort()
    user_list.insert(0, "Group")
    selected_user = st.sidebar.selectbox("Show Users", user_list)

    if st.sidebar.button("Show Analysis"):
        if selected_user != "Group":
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.beta_columns(4)
            num_messages, total_words, num_media_msgs, links = Helper.fetch_stats(selected_user, df)

            with col1:
                st.header("Messages")

                st.title(num_messages)
            with col2:
                st.header("Words")
                st.title(total_words)
            with col3:
                st.header("Media")
                st.title(num_media_msgs)

            with col4:
                st.header("Links")
                st.title(links)


           #Finding the busy user in the group
        if selected_user != "Group":
            st.title('Most Busy user')
            x,new_df = Helper.busy_user(df)
            fig, ax = plt.subplots()

            col1,col2 = st.beta_columns(2)

            with col1:
                ax.bar(x.index, x.values)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


            # Common_words
            st.title("Most Common Words")
            Common_words = Helper.most_commonwords(selected_user, df)
            fig, ax = plt.subplots()

            ax.barh(Common_words[0],Common_words[1])
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

            # Emoji Analysis
            st.title("Emoji Analysis")
            emoji_df = Helper.emoji_Hepler(selected_user, df)
            col1, col2 = st.beta_columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1], labels=emoji_df[0],autopct='%1.1f%%', shadow=True, startangle=90)
                ax.axis('equal')
                st.pyplot(fig)

            st.title("Monthly Timeline analysis")
            timeline = Helper.timeline_msgs(selected_user, df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'],timeline['messages'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

            st.title("daily Timeline analysis")
            daily_timeline = Helper.timeline_daily(selected_user, df)
            fig,ax = plt.subplots()
            ax.plot(daily_timeline['date_only'],daily_timeline['messages'])
            #plt.xticks(rotation='vertical')
            st.pyplot(fig)

            # Common_words
            st.title("Week Activity")
            col1, col2 = st.beta_columns(2)

            with col1:
                busy_day = Helper.timeline_days(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                st.pyplot(fig)

            with col2:
                busy_month = Helper.tbusy_month(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                st.pyplot(fig)

















