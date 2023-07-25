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
        markdown_content += f"""<div style="text-align: right"><strong>{text[0]}</strong></div> \n"""
        markdown_content += f"""<div style="text-align: right"">{text[-1]}</div> \n\n\n"""

    else:
        markdown_content += f"""<div style="text-align: left"><strong>{text[0]}</strong></div> \n"""
        markdown_content += f"""<div style="text-align: left;color:grey">{text[-1]}</div> \n\n\n"""
st.markdown(markdown_content,unsafe_allow_html=True)
            
        