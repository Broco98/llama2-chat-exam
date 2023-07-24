import streamlit as st
import requests
import json


def llama():

    text = st.text_area(
        label='text를 입력해 주세요'
    )

    if st.button('submit'):
        st.session_state['text'] = {'text' : text}
        st.session_state['llama_state'] = 'submit'
        st.experimental_rerun()


def submit_llama():

    text = st.text_area(
        label='text를 입력해 주세요',
        value=st.session_state['text']['text'],
        disabled=True
    )

    with st.spinner('캡션을 생성중입니다. 잠시만 기다려 주세요'):
        res = requests.post(url="http://118.67.130.63:40003/chat", data=json.dumps(st.session_state['text']))
        st.session_state['res'] = res
        st.session_state['llama_state'] = 'result'
        st.experimental_rerun()


def result_llama():

    st.write(st.session_state['res'].json())

    if st.button('return'):
        st.session_state['llama_state'] = 'execute'
        st.experimental_rerun()


if __name__ == "__main__":

    st.title('llama2-7B-chat-hf')

    if 'llama_state' not in st.session_state:
        st.session_state['llama_state'] = 'execute'

    if st.session_state['llama_state'] == 'execute':
        llama()
    elif st.session_state['llama_state'] == 'submit':
        submit_llama()
    else:
        result_llama()