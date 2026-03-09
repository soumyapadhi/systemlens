import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI System Copilot", page_icon="🤖", layout="centered")
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("AI Copilot for Enterprise System Understanding")
st.write("Paste a technical artifact below and ask a question about it.")

artifact = st.text_area(
    "Paste code, architecture notes, API documentation, or process notes",
    height=250
)

question = st.text_input(
    "Ask a question",
    placeholder="Example: Explain what this module does in simple terms"
)


if st.button("Generate Explanation"):
    if not artifact or not question:
        st.warning("Please paste an artifact, enter a question, and provide your API key.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            prompt = f"""
You are an enterprise systems analyst helping a new engineer understand a complex system.

Your job is to:
1. Read the technical artifact carefully
2. Answer the user's question in simple, plain English
3. Explain module responsibility, likely dependencies, and possible downstream impact where relevant
4. Avoid hallucinating specific facts not supported by the artifact
5. If information is missing, clearly say so

Technical artifact:
{artifact}

User question:
{question}

Please structure your answer as:
- Summary
- Key components / dependencies
- Possible impact / notes
"""

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You explain enterprise systems clearly and practically."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )

            answer = response.choices[0].message.content

            st.subheader("AI Explanation")
            st.write(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
