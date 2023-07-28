import streamlit as st 
from PIL import Image

#st.header("Chat History")
avatar = Image.open("data/logo.png")
user_avatar = Image.open("data/user_avatar.png")


st.markdown("<h1 style='text-align: center;'>Chat History</h1>", unsafe_allow_html=True)
history = []

with open("chatlogs/main_log.txt","r") as chat:
    history = chat.read()
history = history.split("£")

current_chat = ""

for i,item in enumerate(history):
    text = item.split("|")

    if(i%2 == 0):
        if len(text[-1]) > 1:
            current_chat+=("User \n ======== \n")
            current_chat+=(f"{text[-1]} \n \n \n \n")

    else:
            current_chat+=("KLEM \n ======== \n")
            current_chat+=(f"{text[-1]} \n \n \n \n")
            
            
st.markdown(
    """
    <style>
    .stDownloadButton > button {
        margin: 0 auto;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    
    
st.download_button("Download Chat History",current_chat,"chat_history.txt")

st.divider()
    


for i,item in enumerate(history):
    text = item.split("|")
  
    
    #if YOU marker
    if(i%2 == 0):
       
        if len(text[-1]) > 1:
            
            st.chat_message("ActionLearning", avatar=user_avatar).write(text[-1])

    else:
        st.chat_message("KLEM", avatar=avatar).write(text[-1])
 
#st.markdown(markdown_content,unsafe_allow_html=True)

