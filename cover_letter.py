import openai
import streamlit as st

# Authenticate the OpenAI API
openai.api_key = st.secrets["KEY"]


# Create a function to generate the cover letter
def generate_cover_letter(prompt, model, word_count, tone):
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=word_count,
        temperature=tone,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
 
    )

    message = completions.choices[0].text
    return message

# Create a function that takes user inputs and generates the cover letter
def cover_letter_generator():
    #st.set_page_config(page_title="GPT 求职信助手 OpenAI GPT Cover Letter Generator", page_icon=":guardsman:", layout="wide")
    #st.markdown("根据你的能力以及职位要求，由 OpenAI GPT 帮助你生成一封专业的求职信。要想了解更多 -> https://axton.blog \n\n OpenAI GPT will help you generate a professional cover letter based on your profile and job description. To learn more -> https://axton.blog")
    st.set_page_config(page_title="GPT OpenAI GPT Cover Letter Generator", page_icon=":guardsman:", layout="wide")
    #st.title("Cover Letter Generator")
    st.title("OpenAI GPT Cover Letter Generator")
    model = "text-davinci-003"
    word_count = st.slider("Word Count", 100, 500, 300)
    tone = st.slider("Tone", 0.0, 1.0, 0.5)

    job_title = st.text_input("Enter the job title you are applying for:")
    user_profile = st.text_area("Enter Your Profile:") 
    job_description = st.text_area("Enter Job Description:")


    prompt = ("Write a cover letter for {job_title} position:\n{job_description}\n\nMy profile:\n{user_profile}")


    if st.button("Generate Cover Letter"):
        cover_letter = generate_cover_letter(prompt, model, word_count, tone)
        st.success("Success! Your Cover Letter is Ready")
        st.markdown(cover_letter)
        st.markdown("**Click the Button to Download**")

        st.download_button(
            label="Download",
            data=cover_letter,
            file_name='cover_letter.md',
        )
        # Download the generated cover letter
        #if st.button("Download Cover Letter"):
        #    with open("cover_letter.txt", "w") as f:
         #       f.write(cover_letter)
          #  st.success("Downloaded successfully")

if __name__ == "__main__":
    cover_letter_generator()
