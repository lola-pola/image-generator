import streamlit as st
import requests
import os

def sending_picture_azure(data_prompt,key,api_base,res="1024x1024"):
    import time
    time.sleep(10)
    api_base = api_base
    api_key = key
    api_version = '2022-08-03-preview'
    url = "{}dalle/text-to-image?api-version={}".format(api_base, api_version)
    headers= { "api-key": api_key, "Content-Type": "application/json" }
    body = {
        "caption": data_prompt,
        "resolution": res
    }
    submission = requests.post(url, headers=headers, json=body)
    operation_location = submission.headers['Operation-Location']
    retry_after = submission.headers['Retry-after']
    status = ""
    while (status != "Succeeded"):
        time.sleep(int(retry_after))
        response = requests.get(operation_location, headers=headers)
        status = response.json()['status']
    image_url = response.json()['result']['contentUrl']
    return image_url



st.set_page_config(page_title="image generator Chatbot", page_icon=":robot_face:")
st.title("image generator Chatbot")
st.markdown("This can generate whatever image that you like")

runner = False
with st.sidebar:
    key = st.text_input('API Key', type='password')
    base = st.text_input('API Base', value='https://xxxxx.openai.azure.com/')
    runner =  st.checkbox('Submit')
    if runner:
        st.success('This is a success message!', icon="✅")


if runner:
        
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = '2022-08-03-preview'
    os.environ["OPENAI_API_BASE"] = base
    os.environ["OPENAI_API_KEY"] = key

    model = st.text_input("image model","text-to-image")
    size = st.selectbox('select image size',('1024x1024','1024x576','300x300'))
    # The text prompt you want to use to generate an image
    prompt = st.text_input("prompt to create image","magic robot eat computer , frozen style")
    if st.button('generate image'):
        with st.spinner('wait while image is generated'):
            # Generate an image
            st.image(sending_picture_azure(prompt,key,base,size))