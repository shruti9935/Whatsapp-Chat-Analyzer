import streamlit as st
import preprocessor,helper


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocessor(data)


    st.dataframe(df)

    #fetch unique users
    user_list= df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    num_messages = 0  # default
    if st.sidebar.button("Analyze"):
        num_messages, words , num_media_messages = helper.fetch_stats(selected_user, df)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.header("Total Messages")
        st.title(f"{num_messages}")

    with col2:
            st.header("Total Words")
            st.title(f"{words}")

    with col3:
        st.header("Total Media Messages")
        st.title(f"{num_media_messages}")
