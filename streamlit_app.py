import streamlit as st
import openai
from metaphor_python import Metaphor

# Set your API keys
OPENAI_API_KEY = "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"
METAPHOR_API_KEY = "af2eb21b-560c-4cbe-9ba7-e358d973f560"

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set Metaphor API key
metaphor = Metaphor(METAPHOR_API_KEY)

# Streamlit app title and description
st.title("Job Search Assistant")

# User input for the question
USER_QUESTION = st.text_input("Enter your question:")

# Button to perform the search and display results
if st.button("Search"):
    if USER_QUESTION:
        SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."

        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": USER_QUESTION},
            ],
        )

        query = completion.choices[0].message.content
        search_response = metaphor.search(
            query, use_autoprompt=True, start_published_date="2023-06-01"
        )

        SYSTEM_MESSAGE = "Please provide the following details considering all the information available: Company Name, Job Title, Years of Experience Required (if mentioned)"

        contents_result = search_response.get_contents()

        # Limit the number of processed links to 5
        max_links_to_process = 5

        # Iterate through each link in the search results
        for i, link in enumerate(contents_result.contents):
            # Check if we have processed the desired number of links
            if i >= max_links_to_process:
                break

            # Extract the content of the link
            link_content = link.extract

            # Use the link content as user input for OpenAI API
            messages = [
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": link_content},
            ]

            # Make an API request for the current link
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
            )

            # Extract and display the response for the current link
            summary = completion.choices[0].message.content
            st.write(f"{link.url}: {summary}")
