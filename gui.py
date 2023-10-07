import streamlit as st
import json
import requests
from my_models import Question
from my_env import QUESTION_TYPE
API_ENDPOINT = "http://127.0.0.1:8000/"

class CustomEncoder(json.JSONEncoder):
    def encode(self, obj):
        def fix_none(item):
            return item if item is not None else "null"

        return super().encode(obj, default=fix_none)
    
def _call_api(question_input):
    try:
        payload = question_input.model_dump()
        print(json.dumps(payload))
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(
            API_ENDPOINT, headers=headers, data=json.dumps(payload))

        # Check for HTTP status code indicating a successful response
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error sending request to the server: {e}")
        return None


with st.sidebar:
    with open(f"how_to_use.md", "r") as f:
        st.markdown(f.read())
    st.subheader('Models and parameters')
    top_k = st.sidebar.slider(
        'Top K Articles', min_value=1, max_value=50, value=5, step=1)
    top_p = st.sidebar.slider(
        'Top Prompts', min_value=1, max_value=4, value=1, step=1)

st.title("Legal Question Answering")

t1, t2, t3 = st.tabs(
    [
        'True/False question',
        'Multiple-choice question',
        'Free-text question'
    ])


with t1.form(QUESTION_TYPE[0]):
    question = st.text_area('Enter Question:')
    submitted = st.form_submit_button('Submit')
    question_type = QUESTION_TYPE[0]
    if submitted:
        question_input = Question(
            question_type=question_type, question=question)
        response_data = _call_api(question_input)
        if response_data is not None:
            answser = response_data["answer"]
            law_id = response_data["law_id"]
            law = response_data["law"]
            law_text = response_data["law_text"]

            if answser == "True":
                st.success("True")
            else:
                st.error("False")

            with st.expander(f"Base on: {law}Article:{law_id}"):
                st.markdown(law_text)
        else:
            st.warning(
                "There was an issue with the server or API call. Please try again later.")


with t2.form(QUESTION_TYPE[1]):
    text = st.text_area('Enter Question:')
    option_a = st.text_input('Option A:')
    option_b = st.text_input('Option B:')
    option_c = st.text_input('Option C:')
    option_d = st.text_input('Option D:')
    submitted = st.form_submit_button('Submit')
    if submitted:
        print(submitted)
        import random
        answser = random.choice(["True", "False"])
        st.success(answser)
        law_id = 1
        law = "Luật A"
        law_text = "Luật abc"
        with st.expander(f"Căn cứ vào {law} điều:{law_id}"):
            st.markdown(law_text)

with t3.form("free_text"):
    text = st.text_area('Enter Question:')
    submitted = st.form_submit_button('Submit')
    if submitted:
        ans = "cau tra loi day ne"
        st.text_area(value=ans, disabled=True, label="Answer")
        law_id = 1
        law = "Luật A"
        law_text = "Luật abc"
        with st.expander(f"Căn cứ vào {law} điều:{law_id}"):
            st.markdown(law_text)
