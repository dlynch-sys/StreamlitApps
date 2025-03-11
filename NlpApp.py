
#Core pakages
import streamlit as st 
st.set_page_config(page_title="NLP Web App", layout="centered",initial_sidebar_state="auto")

#NLP packages
from textblob import TextBlob
import spacy
import neattext as nt
from collections import Counter
import re


# Visualization packages
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud

#Translatio packages
from deep_translator import GoogleTranslator

# Summarization Function
def summarize_text(text,num_sentences=3):
    # The line of code below removes all characters from the text string that are not upper or lower case letters '[^a-zA-Z]' (e.g., numbers,punctuation,symbols). It then replaces those non-letter characters with spaces, then converts all remaining letters to lowercase
    clean_text = re.sub('[^a-zA-Z]',' ',text).lower()

    #Split the text into words
    words = clean_text.split()

    # Calculate the frequency of each word
    word_freq = Counter(words)

    # Sort the words based on their frequency in decending order
    sorted_words = sorted(word_freq,key=word_freq.get,reverse=True)

    # Extract the to 'num_sentences' most frequent words
    top_words = sorted_words[:num_sentences]

    # Create the summary by joining the top words
    summary=' '.join(top_words)
    return summary

@st.cache_data
#Lemma and Tokens Function
def text_analyzer(text):
    #import English library
    nlp= spacy.load('en_core_web_sm')

    # create an nlp object that contains all the linguistic annotations and information extracted from the text. e.g part-of-speech, name entity recognition(identifying people, places, organizations,etc). Dependency parsing (analyzing the grammatical relationships between words) and much more.
    doc=nlp(text)
    
    #extract tokens an lemmas
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text, token.lemma_)) for token in doc]
    return allData

def main():
    """ NLP web app with Streamlit"""
    title_template = """
<div style="background-color:blue; padding:8px;">
<h1 style = "color:cyan">NLP Web App</h1>
</div>
"""
    st.markdown(title_template,unsafe_allow_html=True)
    subheader_template ="""
<div style="background-color:cyan; padding:8px;">
<h3 style = color:blue">Powered by Streamlit</h3
</div>"""
    st.markdown(subheader_template,unsafe_allow_html=True)
    activity=["Text Analysis","Translation", "Sentiment Analysis","About"]
    st.sidebar.image('MyStreamlitProject/nlp.jpg',use_container_width=True
                     )
    choice = st.sidebar.selectbox("Menu",activity)

    if choice == "Text Analysis":
        st.subheader("Text Analysis")
        st.write("")
        raw_text = st.text_area("Write something","Enter a text in english...",height=300)
        if st.button("Analyze"):
            if len(raw_text) ==0:
                st.warning("Enter a text...")
            else:
                blob=TextBlob(raw_text)
                #st.write("OK")
                st.info("Basic Function")
# The col1 , col2 = st.columns(2) line just creats two columns named col1 and col2. In the two with lines, we use these columns.In each of the columns, we create an expander: each expander has its own label (Basic Info and Processed Text)
                col1, col2 = st.columns(2)

                with col1:
                    with st.expander("Basic Info"):
                        st.info("Text Stats")
                        word_desc = nt.TextFrame(raw_text).word_stats()
                        result_desc = {"Length of Text":word_desc['Length of Text'],
                        "Num of Vowels":word_desc['Num of Vowels'],
                        "Num of Consonants":word_desc['Num of Consonants'],
                        "Num of Stopwords":word_desc['Num of Stopwords']}

                        st.write(result_desc)
                    with st.expander("Stopwords"):
                        st.success("Stop Words List")
                        stop_w = nt.TextExtractor(raw_text).extract_stopwords()
                        st.error(stop_w)
                                    
                with col2:
                    with st.expander("Processed Text"):
                        st.success("Stopwords Excluded Text")
                        processed_text = str(nt.TextFrame(raw_text).remove_stopwords())
                        st.write(processed_text)


                    with st.expander("Plot WordCloud"):
                        st.success("WordCloud")
                        wordcloud = WordCloud().generate(processed_text)
                        fig = plt.figure(1, figsize=(20,10))
                        plt.imshow(wordcloud,interpolation='bilinear')
                        plt.axis('off')
                        st.pyplot(fig)

# we use neattext's remove_stopwords() to get the text we input without the stopwords, thaten cast it to a string (str), and save it in a variable named processed_text: finally we write the processed text on the screen

# NOTE: stopwords are comon words that don't add any informatio to our orginal text
                        

                st.write("")
                st.write("")
                st.info("Advanced Features")

                col3, col4 = st.columns(2)

                with col3:
                    with st.expander("Tokens&Lemmas"):
                        st.write("T&K")
                        
                        
#Using neattet (alias nt) to remove stopwords, punctuation, and special characters. 
                        processed_text_mid = str(nt.TextFrame(raw_text).remove_stopwords())
                        processed_text_mid = str(nt.TextFrame(raw_text).remove_puncts())
                        processed_text_fin = str(nt.TextFrame(raw_text).remove_special_characters())

                        tandl = text_analyzer(processed_text_fin)

# Since the text_analyzer function returns a dictionary - or more accurately, a list of dictionaries - we are printing it in the JSON format (st.json(tandl))
                        st.json(tandl)

                with col4:
                    with st.expander("Summarize"):
                        st.success("Summarize")
                        summary = summarize_text(raw_text)
                        st.success(summary)
 
# Lemmas are made of so-called plain text, so if we say code, coding, or coder, we can assume that for all these three words, the lemma is just code.

    if choice == "Translation":
        st.subheader("Translation")
        st.write("")
        st.write("")
        raw_text = st.text_area("Original Text","Write something to be translated...",height=200)
        if len(raw_text)<3:
            st.warning("Please provide a text with at least 3 characters...")
        else:
            target_lang = st.selectbox("Target Language",['German','Spanish','French','Italian'])
            if target_lang == 'German':
                target_lang = 'de'
            elif target_lang == 'Spanish':
                target_lang = 'es'
            elif target_lang == 'French':
                target_lang = 'fr'
            else:
                target_lang = 'it'

                #When the translate buton is pressed we call jthe googletranslator function fo the deep_translator package, put the result into a translated_text variable, and then write it on the screen.
            if st.button("Translate"):
                translator = GoogleTranslator(source='auto',target=target_lang)
                translated_text = translator.translate(raw_text)
                st.write(translated_text)

    if choice == "Sentiment Analysis":
        st.subheader("Sentiment Analysis")
        st.write("")
        st.write("")
        raw_text = st.text_area("Text to analyse", "Enter your text here...", height= 200)
        if st.button("Sentiment Evaluator"):
            if len(raw_text)==0:
                st.warning("Enter a text...")
            else:
# The textblob class provides a simple API for common natural language proessing (NLP) tasks. the code below passes the raw_text string as an argument to the TextBlob constructor.The TextBlob object then proesses the tet, making it ready for various NLP operations such as:
#Part-of-speech tagging
# Sentiment analysis
# Noun phrase extraction
# Tokenization and more 
             
                blob = TextBlob(raw_text)
                st.info("Sentiment Analysis")
                st.write(blob.sentiment)
                st.write("")



    if choice == "About":
        st.subheader("About")
        st.write("")
        st.markdown("""
### NLP Web App made with Streamlit
                    
for info:
- [Streamlit](https://www.streamlit.io)
""")


if __name__ == "__main__":
    main()


