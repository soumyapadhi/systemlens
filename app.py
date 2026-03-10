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
        st.warning("Please paste an artifact and enter a question.")
    else:
        try:
            prompt = f"""
You are an enterprise systems analyst helping a new engineer understand a complex enterprise system.

Your task is to analyze the technical artifact and answer the user's question in a practical, structured, beginner-friendly way.

Important instructions:
- Use only the information available in the artifact
- Do not invent dependencies or workflows that are not supported by the input
- If something is unclear or missing, explicitly mention it
- Explain in simple business and system language, not overly technical jargon
- Keep the answer crisp but useful

Technical artifact:
{artifact}

User question:
{question}

Return your response in exactly this structure:

### 1. System / Module Summary
Explain in 2-3 lines what this artifact appears to do.

### 2. Key Components / Dependencies
List the main services, modules, systems, or actors mentioned or implied in the artifact.

### 3. Workflow Explanation
Explain the likely end-to-end flow step by step in simple terms.

### 4. Potential Impact if This Changes
Explain what downstream impact or risks may happen if this module or workflow changes.

### 5. Gaps / Unclear Areas
Mention what is missing, ambiguous, or would need validation from an engineer or documentation.
"""

            with st.spinner("Analyzing artifact..."):
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior enterprise systems analyst. You explain technical artifacts clearly, practically, and in a structured format for new engineers, product managers, and program managers."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )

                answer = response.choices[0].message.content

            st.subheader("AI Explanation")
            st.markdown(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
