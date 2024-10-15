import streamlit as st
import requests
import json
import os
from urllib.parse import urlparse

st.set_page_config(page_title='hallucinator')

def validate_number_of_images(num):
    if not num:
        st.error("Please enter a number.")
        return False
    try:
        num = int(num)
        if num > 50:
            st.error("Number of images should be less than or equal to 50.")
            return False
        elif num < 1:
            st.error("Number of images should be at least 1.")
            return False
        return True
    except ValueError:
        st.error("Invalid input. Please enter a valid number.")
        return False


def fetchImages(url):
    error = None

    try:
        response = requests.get(url)
    except Exception as e:
        error = e
        return None, error
    response = response.json()
    return response, error


def main():
    st.title('hallucinator')

    count = st.text_input("Enter the number of dog images (1-50):", "")
    
    if not validate_number_of_images(count):
        st.write("Count should be less than 50!")
    else:
        api_url = "https://dog.ceo/api/breeds/image/random/"+count
            

        result, error = fetchImages(api_url)
        num_columns = 3 
        image_urls = result['message']
        if error is None:
            for idx in range(0, len(image_urls), num_columns):
                cols = st.columns(min(num_columns, len(image_urls) - idx)) 
                for col, image_url in zip(cols, image_urls[idx:idx + num_columns]):
                    with col:
                        st.image(image_url, caption=f"Dog Image {idx + 1}", use_column_width=True)
                    # for idx, image_url in enumerate(result['message'], start=1):
                    #     with cols[idx - 1]:  # Assign each image to a separate column
                    #         st.image(image_url, caption=f"Dog Image {idx}", use_column_width=True)
                    #st.markdown('<img src="%s" alt="picture" width="400"/>' % image_url,unsafe_allow_html=True)
                    #st.markdown("Image __%s__" % {idx})
                
        else:
            st.write("Something went wrong, error %s" % error)
            


if __name__ == "__main__":
    main()
