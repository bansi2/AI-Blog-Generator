import streamlit as st
import base64
import os
from google import genai
from google.genai import types
from openai import OpenAI
import os
os.environ["GEMINI_API_KEY"] = "AIzaSyBroo6adbAQDUXqLYoHZ_gEXnBkmOAoBRw"


client1 = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
client2 = OpenAI(api_key="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")


st.set_page_config(layout='wide')
st.title("BlogCrafter: AI crafted blogs")
st.subheader("Now you can craft perfect blogs with help of -AI BlogCrafter")
blog = "The blog content will appear here."
with st.sidebar:
    st.title("Input your blog details:")
    
    blog_title = st.text_input("Blog Title:")
    keywords = st.text_area("Enter keywords(comma-separated)")
    num_words = st.slider("Number of Words", min_value=250, max_value=1000, step=10)
    submit_button = st.button("Generate Blog")



def generate_blog(title, keywords, num_words):
    prompt = f"""
    You are a professional blog writer.
    Write a detailed and engaging blog article.
    Title: {title}
    Keywords to include naturally in the blog: {keywords}
    Target length: {num_words} words.
    Tone: Informative and conversational.
    Structure:
    - Introduction
    - At least 4 subheadings
    - Use bullet points where helpful
    - Include a conclusion
    """
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(thinking_budget=-1)
    )

    response = ""
    for chunk in client1.models.generate_content_stream(
        model="gemini-2.5-pro",
        contents=contents,
        config=generate_config,
    ):
        if chunk.text:
            response += chunk.text

    return response


def image_prompt(title:str, keyword:str) -> str:
    prompt = (
        f"High-quality, visually appealing image that represents the blog titled \"{title}\". "
        f"Include visual elements suggested by these keywords: {keywords}. "
        f"Make it compositionally clean and suitable for use in an online blog header or inline image. "
    )
    return prompt

def generate_image(prompt):
    try:
        response = client1.images.generate(
            model="imagen-2",  
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        image_path = "generated_blog_image.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        return image_path
    except Exception as e:
        st.error(f"Image generation failed: {e}")
        return None
    
if submit_button:
    with st.spinner("🎨 Generating blog image..."):
        prompt = image_prompt(blog_title, keywords)
        image_file = generate_image(prompt)

    with st.spinner("✍️ Writing your blog..."):
        blog_content = generate_blog(blog_title, keywords, num_words)

    if image_file:
        st.image(image_file, caption="AI Generated Blog Image", use_column_width=True)

    st.markdown(blog_content)