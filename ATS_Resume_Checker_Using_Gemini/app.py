from dotenv import load_dotenv
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import base64
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Google API Key for Generative AI
GOOGLE_API_KEY = "YOUR-API-KEY"
genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="PNG")  # Save directly to BytesIO

        # Rewind the byte stream to the beginning
        img_byte_arr.seek(0)

        # Encode to base64
        pdf_parts = [
            {
                "mime_type": "image/png",  # PNG instead of jpeg, since you're saving as PNG
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()  # Encode the image bytes to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Input for job description
input_text = st.text_area("Job Description: ", key="input")
uploaded_files = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_files is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I improvise my skills")
submit3 = st.button("Percentage match")

input_prompt1 = """
You are an experienced HR with technical experience in the fields of Data Science, Full-stack Web Development,
Big Data Engineering, DEVOPS, Data Analysis. Your task is to review the provided resume against the job description for these profiles. 
Please share your professional evaluation of whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a Technical Human Resource Manager with expertise in Data Science, Full-stack Web Development,
Big Data Engineering, DEVOPS, Data Analysis. Your role is to scrutinize the resume in light of the job description provided. 
Share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify areas for improvement.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full-stack Web Development,
Big Data Engineering, DEVOPS, and Data Analysis with deep ATS functionality. 
Your task is to evaluate the resume against the provided job description. 
Give me the percentage of match if the resume matches the job description. First, the output should come as a percentage and then list missing keywords, followed by final thoughts.
"""

if submit1:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit2:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume.")

elif submit3:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume.")

