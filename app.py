import streamlit as st
from openai import OpenAI
from pypdf import PdfReader
from docx import Document

st.set_page_config(page_title="AI System Copilot", page_icon="🤖", layout="centered")

api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text


def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def extract_artifact_text(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif file_name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        return ""


st.title("AI Copilot for Enterprise System Understanding")
st.write("Upload a technical document or paste an artifact below and analyze it in different ways.")

analysis_mode = st.selectbox(
    "Choose analysis mode",
    [
        "Explain Artifact",
        "Dependency Analysis",
        "Change Impact Analysis",
        "Onboarding Summary"
    ]
)

uploaded_file = st.file_uploader(
    "Upload a PDF, Word document, or text file",
    type=["pdf", "docx", "txt"]
)

st.caption("Best results with text-based PDFs, DOCX files, and structured technical documents.")

artifact = st.text_area(
    "Or paste code, architecture notes, API documentation, or process notes",
    height=250
)

question = st.text_input(
    "Ask a question",
    placeholder="Example: Give me a beginner-friendly summary of this flow"
)

if st.button("Run Analysis"):
    extracted_text = extract_artifact_text(uploaded_file) if uploaded_file else ""
    final_artifact = extracted_text if extracted_text.strip() else artifact

    if not final_artifact or not question:
        st.warning("Please upload a file or paste an artifact, and enter a question.")
    else:
        try:
            if analysis_mode == "Explain Artifact":
                mode_instruction = """
Return your response in exactly this structure:

### 1. System / Module Summary
Explain in 2-3 lines what this artifact appears to do.

### 2. Key Components / Dependencies
List the main services, modules, systems, or actors mentioned or implied in the artifact.

### 3. End-to-End Workflow
Explain the likely end-to-end flow step by step in simple terms.

### 4. Simple Flow Diagram
Represent the workflow as a simple arrow diagram like this:

Customer
↓
OrderService
↓
InventoryService
↓
PaymentService
↓
NotificationService

### 5. Potential Impact if This Changes
Explain what downstream impact or risks may happen if this module or workflow changes.

### 6. Gaps / Unclear Areas
Mention what is missing, ambiguous, or would need validation from an engineer or documentation.

### 7. Program / Product Insight
Explain what a product manager or technical program manager should pay attention to in this system.
Mention risks, scaling concerns, or operational dependencies.
"""

            elif analysis_mode == "Dependency Analysis":
                mode_instruction = """
Return your response in exactly this structure:

### 1. Primary Module / Service
Identify the main module or service in the artifact.

### 2. Upstream Dependencies
List systems, services, inputs, or actors this module depends on.

### 3. Downstream Dependencies
List systems, services, or workflows likely affected by this module.

### 4. Dependency Risks
Mention any dependency-related risks or tight coupling visible from the artifact.

### 5. Gaps / Unclear Areas
Mention what dependency information is missing or needs confirmation.

### 6. Program / Product Insight
Explain what a PM or TPM should watch from a dependency and coordination standpoint.
"""

            elif analysis_mode == "Change Impact Analysis":
                mode_instruction = """
Return your response in exactly this structure:

### 1. Module / Area Being Considered
Explain what part of the system appears to be changing.

### 2. Likely Impacted Areas
List downstream systems, workflows, or business processes that may be affected.

### 3. Key Risks
Mention operational, technical, or business risks if this module changes.

### 4. Validation / Testing Recommendations
Suggest what should be validated before release.

### 5. Gaps / Unclear Areas
Mention what is missing and what needs deeper engineering review.

### 6. Program / Product Insight
Explain what a TPM should do before and during release if this area changes.
"""

            else:  # Onboarding Summary
                mode_instruction = """
Return your response in exactly this structure:

### 1. Beginner-Friendly Summary
Explain what this artifact does in very simple terms.

### 2. Key Components to Understand First
List the main modules, systems, or actors a new joiner should focus on first.

### 3. End-to-End Workflow
Explain the flow step by step as if explaining to someone new to the system.

### 4. Simple Flow Diagram
Represent the workflow as a simple arrow diagram.

### 5. What Could Be Confusing
Call out areas that may confuse a new engineer or PM.

### 6. Suggested Next Questions
List 3-5 follow-up questions a new joiner should ask to understand the system better.

### 7. Program / Product Insight
Explain what a PM or TPM should understand about this system beyond the technical flow.
"""

            prompt = f"""
You are an enterprise systems analyst helping a new engineer understand a complex enterprise system.

Your task is to analyze the technical artifact and answer the user's question in a practical, structured, beginner-friendly way.

Important instructions:
- Use only the information available in the artifact
- Do not invent dependencies or workflows that are not supported by the input
- If something is unclear or missing, explicitly mention it
- Explain in simple business and system language, not overly technical jargon
- Keep the answer crisp but useful

Analysis mode:
{analysis_mode}

Technical artifact:
{final_artifact}

User question:
{question}

{mode_instruction}
"""

            with st.spinner("Analyzing artifact..."):
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior enterprise systems analyst. You explain technical artifacts clearly, practically, and in a structured format for new engineers, product managers, and technical program managers."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )

                answer = response.choices[0].message.content

            st.subheader(f"AI Output — {analysis_mode}")
            st.markdown(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
