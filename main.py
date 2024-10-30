import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import time
import os
load_dotenv()

def generate_blog_content(topic):
    # Initialize Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Craft the prompt for structured blog content
    prompt = f"""Generate a comprehensive, informative, and topic-focused blog post on '{topic}', designed for readers seeking reliable medical information.

Content and Structure:
- Create **20 distinct sections** on key aspects of the topic, with the **final section dedicated to FAQs**.
- Each section should directly relate to the main topic and contain content strictly relevant to the heading.
- Begin each section with a <section> tag, using <h2> tags for section headings and <p> tags for content.

Content Requirements:
- Use precise and informative medical language to ensure clarity and reader confidence.
- Each <h2> tag heading must directly support or expand upon the main topic, avoiding unrelated or extraneous information.
- **Highlight essential terms** with <strong> tags, focusing on clarity and key concepts dont forget this its very important.
- Ensure each paragraph is 150-200 words and stays focused on providing depth and relevance without digressing.

Formatting and Tone:
- Use a formal, authoritative tone appropriate for a professional medical blog.
- Avoid unnecessary questions or unrelated content; every section should add value, with each <h2> and associated content directly tied to '{topic}'.
- Ensure FAQs answer only relevant questions readers might have after reading the main content.

Example of Section Structure:
<section>
    <h2>Overview of [Medical Condition]</h2>
    <p>Clear, comprehensive overview with <strong>key terms</strong> highlighted for emphasis...</p>
</section>

Example of FAQ Section:
<section>
    <h2>FAQs</h2>
    <h3>What causes [Medical Condition]?</h3>
    <p>A clear, accurate answer with <strong>relevant terms</strong> highlighted.</p>
</section>
"""

    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq's Mixtral model
            messages=[
                {"role": "system", "content": "You are a specialized medical content writer with expertise in Indian healthcare and medical tourism. Create professional, accurate, and well-structured content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=32000
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Streamlit UI
st.title("Blog Content Generator")
st.write("Enter your blog topic and get a formatted blog post with proper HTML structure.")

# Input field for blog topic
topic = st.text_input("Enter your blog topic:")

# Generate button
if st.button("Generate Blog Content"):
    if topic:
        with st.spinner("Generating your blog content..."):
            # Show a progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Generate content
            blog_content = generate_blog_content(topic)
            
            # Display raw HTML
            st.subheader("Generated HTML Content:")
            st.code(blog_content, language='html')
            
            # Display rendered content
            st.subheader("Preview:")
            st.markdown(blog_content, unsafe_allow_html=True)
            
            # Add download button
            st.download_button(
                label="Download HTML",
                data=blog_content,
                file_name=f"{topic.lower().replace(' ', '-')}-blog.html",
                mime="text/html"
            )
    else:
        st.warning("Please enter a blog topic.")

# Add sidebar with instructions
with st.sidebar:
    st.header("Instructions")
    st.write("""
    1. Enter your blog topic in the text field
    2. Click 'Generate Blog Content'
    3. View the generated HTML and preview
    4. Download the HTML file if satisfied
    """)
    
    st.header("Features")
    st.write("""
    - Generates 20 sections including FAQs
    - Proper HTML structure with semantic tags
    - Bold important keywords
    - Clean, readable format
    - Downloadable HTML file
    - Powered by Groq's Mixtral model
    """)