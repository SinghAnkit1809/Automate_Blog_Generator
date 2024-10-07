import streamlit as st
#from langchain.llms import Groq
from langchain_groq import ChatGroq
#from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
#from langchain.callbacks import StreamlitCallbackHandler
#from dotenv import load_dotenv
import time
import os
from typing import List

# Set up Groq API key
#load_dotenv()
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq LLM with a specific model
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",  # Specify the model you want to use
    temperature=0.7,
    max_tokens=32000  # Adjust based on the model's capabilities
)

# Define prompt templates
h2_prompt = ChatPromptTemplate(
    input_variables=["topic"],
    template="""Generate a sequence of H2 tags for a blog page on the topic of {topic}. 
    This is for a blog page, not the main page, so focus on relevant subtopics. 
    Provide between 10 and 20 H2 tags. Include FAQs at the end. 
    Only provide H2 tags that are relevant to the topic."""
)

content_prompt = ChatPromptTemplate(
    input_variables=["h2_tag"],
    template="""Generate unique and relevant content for the following H2 tag:

    {h2_tag}

    Provide 1 to 2 paragraphs of formal length. 
    Only provide information that has been asked for, with no unnecessary or unasked input."""
)

html_format_prompt = ChatPromptTemplate(
    input_variables=["content"],
    template="""Convert the following content into HTML format:

    {content}

    Wrap the H2 tag in a <section> tag. 
    Put the section heading in <h2> tags and the information in <p> tags. 
    Do not use <div> tags. 
    Do not change or modify any information, only update it into HTML format. 
    Bold important keywords, but don't make it too dense. 
    Ensure there aren't too many bold words in a single paragraph."""
)

# Create LLMChains
h2_chain = LLMChain(llm=llm, prompt=h2_prompt)
content_chain = LLMChain(llm=llm, prompt=content_prompt)
html_chain = LLMChain(llm=llm, prompt=html_format_prompt)

def generate_content_for_h2(h2_tag: str) -> str:
    """Generate content for a single H2 tag with error handling and retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return content_chain.run(h2_tag)
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Error generating content for '{h2_tag}'. Retrying... (Attempt {attempt + 1})")
                time.sleep(2)  # Wait before retrying
            else:
                st.error(f"Failed to generate content for '{h2_tag}' after {max_retries} attempts.")
                return f"Content generation failed for: {h2_tag}"

def format_html_section(content: str) -> str:
    """Format a single section of content as HTML with error handling."""
    try:
        return html_chain.run(content)
    except Exception as e:
        st.error(f"Error formatting HTML: {str(e)}")
        return f"<section><h2>Error</h2><p>Failed to format content as HTML.</p></section>"

# Streamlit app
st.title("Blog Content Generator")

topic = st.text_input("Enter the main topic for your blog page:")

if topic:
    st.write("Generating content...")
    
    # Generate H2 tags
    with st.spinner("Generating H2 tags..."):
        h2_tags_text = h2_chain.run(topic)
        h2_tags = [tag.strip() for tag in h2_tags_text.split('\n') if tag.strip()]
    st.write(f"{len(h2_tags)} H2 tags generated!")

    # Generate content for H2 tags
    html_sections = []
    for i, h2_tag in enumerate(h2_tags):
        with st.spinner(f"Generating content for H2 tag {i+1}/{len(h2_tags)}..."):
            content = generate_content_for_h2(h2_tag)
            html_section = format_html_section(f"{h2_tag}\n\n{content}")
            html_sections.append(html_section)
        
        # Optional: Add a delay to avoid rate limiting
        time.sleep(1)

    # Combine all HTML sections
    full_html_content = "\n".join(html_sections)

    # Display the generated HTML content
    st.subheader("Generated HTML Content:")
    st.code(full_html_content, language="html")

    # Option to download the HTML content
    st.download_button(
        label="Download HTML",
        data=full_html_content,
        file_name="blog_content.html",
        mime="text/html"
    )