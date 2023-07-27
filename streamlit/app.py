import streamlit as st
import requests
import json


def llama():

    ## 파싱 EXAMPLE
    text = """"message":"You are now a bot making music captions.
create a caption (keyword) to create music that matches the [Input Text].
just print [Output Phrase].

example start>

[Input Text]: Thrilling tension in a chase scene
[Output Phrase]: Thrill, tension, electronic music

[Input Text]: Dancing with joyful friends at a party
[Output Phrase]: Dance, friends, high spirits

[Input Text]: Music that accompanies the loneliness of walking on a lonely night street
[Output Phrase]: Emotion, loneliness, calm piano

[Input Text]: Small moments of joy in everyday life
[Output Phrase]: Pleasant, happiness, cheerful melody

[Input Text]: Playful children having fun and laughter
[Output Phrase]: Children, joy, lively music

[Input Text]: The passionate performance of a musician, moving the audience
[Output Phrase]: Passion, emotion, classical music

[Input Text]: Relaxing time on a calm lake in a swaying boat
[Output Phrase]: Relaxation, lake, acoustic guitar

[Input Text]: Enjoying a comedy movie scene with laughter
[Output Phrase]: Comedy, laughter, cheerful music

[Input Text]: An emotional explosion of anger and sadness
[Output Phrase]: Emotion, anger, slow orchestral music

[Input Text]: A timeless story of innocent love
[Output Phrase]: Innocence, love, romantic piano

end example>

[Input Text]: Seonbi's father is a worker of Jeong Deok-ho, the landowner of Yongyeon Village, who went to receive the light under Deok-ho's direction and was killed by Deok-ho for helping the tenant.
[Output Phrase]: Tragedy, death, melancholic music"""

    print(text.split("[Output Phrase]:")[-1])
    text = text.split("[Output Phrase]:")[-1]
    print(text.split(','))
    text = text.split(',')
    text = [t.strip() for t in text]
    print(text)


    prompt_text = """You are now a bot making music captions.
create a caption to create music that matches the [Input Text].
just print [Output Phrase].

example start>

[Input Text]: Thrilling tension in a chase scene
[Output Phrase]: Thrill, tension, electronic music

[Input Text]: Dancing with joyful friends at a party
[Output Phrase]: Dance, friends, high spirits

[Input Text]: Music that accompanies the loneliness of walking on a lonely night street
[Output Phrase]: Emotion, loneliness, calm piano

[Input Text]: Small moments of joy in everyday life
[Output Phrase]: Pleasant, happiness, cheerful melody

[Input Text]: Playful children having fun and laughter
[Output Phrase]: Children, joy, lively music

[Input Text]: The passionate performance of a musician, moving the audience
[Output Phrase]: Passion, emotion, classical music

[Input Text]: Relaxing time on a calm lake in a swaying boat
[Output Phrase]: Relaxation, lake, acoustic guitar

[Input Text]: Enjoying a comedy movie scene with laughter
[Output Phrase]: Comedy, laughter, cheerful music

[Input Text]: An emotional explosion of anger and sadness
[Output Phrase]: Emotion, anger, slow orchestral music

[Input Text]: A timeless story of innocent love
[Output Phrase]: Innocence, love, romantic piano

end example>

[Input Text]: """

    prompt = st.text_area(
        label='prompt',
        value=prompt_text
    )

    text = st.text_area(
        label='text를 입력해 주세요'
    )

    if st.button('submit'):
        st.session_state['text'] = text
        st.session_state['prompt'] = prompt

        inputs = {
            'prompt': prompt,
            'text': text
        }

        res = requests.post(url="http://118.67.130.63:40003/chat", data=json.dumps(inputs))
        st.session_state['res'] = res
        print("res >>", res)
        st.session_state['llama_state'] = 'submit'
        st.experimental_rerun()

def result_llama():

    # res 파싱
    res = st.session_state['res'].json()['message']
    res = res.split('\n\n')
    
    print(res)

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
    else:
        result_llama()