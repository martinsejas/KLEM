import streamlit as st 

st.header("Chat History")
markdown_content = ""    

history = []
    
with open("chatlogs/main_log.txt","r") as chat:
    history = chat.read()
history = history.split("£")
# history = history[:-1]



for i,item in enumerate(history):
    text = item.split("|")
  
    
    #if YOU marker
    if(i%2 == 0):
       
        if len(text[-1]) > 1:
            st.chat_message("user").write(text[-1])

    else:
        st.chat_message("assistant").write(text[-1])
 
#st.markdown(markdown_content,unsafe_allow_html=True)

        