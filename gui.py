import streamlit as st

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


with t1.form('true_false'):
    text = st.text_area('Enter Question:')
    submitted = st.form_submit_button('Submit')
    if submitted:
        import random
        answser = random.choice(["True", "False"])
        if answser == "True":
            st.success("True")
        else:
            st.error("False")
        law_id = 1
        law = "Luật A"
        law_text = "Luật abc"
        with st.expander(f"Căn cứ vào {law} điều:{law_id}"):
            st.markdown(law_text)

with t2.form('options'):
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
