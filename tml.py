"""Topic Modelling and Labelling App"""

#Importing packages
import gensim
import pandas as pd
from gensim import corpora,models
import streamlit as st
import os
import re
import base64
import heapq

#### topic labeling ##########

insurance_keywords = ['actuary', 'claims', 'coverage', 'deductible', 'policyholder', 'premium', 'underwriter', 'risk assessment', 'insurable interest', 'loss ratio', 'reinsurance', 'actuarial tables', 'property damage', 'liability', 'flood insurance', 'term life insurance', 'whole life insurance', 'health insurance', 'auto insurance', 'homeowners insurance', 'marine insurance', 'crop insurance', 'catastrophe insurance', 'umbrella insurance', 'pet insurance', 'travel insurance', 'professional liability insurance', 'disability insurance', 'long-term care insurance', 'annuity', 'pension plan', 'group insurance', 'insurtech', 'insured', 'insurer', 'subrogation', 'adjuster', 'third-party administrator', 'excess and surplus lines', 'captives', 'workers compensation', 'insurance fraud', 'health savings account', 'health maintenance organization', 'preferred provider organization']

finance_keywords = ['asset', 'liability', 'equity', 'capital', 'portfolio', 'dividend', 'financial statement', 'balance sheet', 'income statement', 'cash flow statement', 'statement of retained earnings', 'financial ratio', 'valuation', 'bond', 'stock', 'mutual fund', 'exchange-traded fund', 'hedge fund', 'private equity', 'venture capital', 'mergers and acquisitions', 'initial public offering', 'secondary market', 'primary market', 'securities', 'derivative', 'option', 'futures', 'forward contract', 'swaps', 'commodities', 'credit rating', 'credit score', 'credit report', 'credit bureau', 'credit history', 'credit limit', 'credit utilization', 'credit counseling', 'credit card', 'debit card', 'ATM', 'bankruptcy', 'foreclosure', 'debt consolidation', 'taxes', 'tax return', 'tax deduction', 'tax credit', 'tax bracket', 'taxable income']

banking_capital_markets_keywords = ['bank', 'credit union', 'savings and loan association', 'commercial bank', 'investment bank', 'retail bank', 'wholesale bank', 'online bank', 'mobile banking', 'checking account', 'savings account', 'money market account', 'certificate of deposit', 'loan', 'mortgage', 'home equity loan', 'line of credit', 'credit card', 'debit card', 'ATM', 'automated clearing house', 'wire transfer', 'ACH', 'SWIFT', 'international banking', 'foreign exchange', 'forex', 'currency exchange', 'central bank', 'Federal Reserve', 'interest rate', 'inflation', 'deflation', 'monetary policy', 'fiscal policy', 'quantitative easing', 'securities', 'stock', 'bond', 'mutual fund', 'exchange-traded fund', 'hedge fund', 'private equity', 'venture capital', 'investment management', 'portfolio management', 'wealth management', 'financial planning']

healthcare_life_sciences_keywords = ['medical device', 'pharmaceutical', 'biotechnology', 'clinical trial', 'FDA', 'healthcare provider', 'healthcare plan', 'healthcare insurance', 'patient', 'doctor', 'nurse', 'pharmacist', 'hospital', 'clinic', 'healthcare system', 'healthcare policy', 'public health', 'healthcare IT', 'electronic health record', 'telemedicine', 'personalized medicine', 'genomics', 'proteomics', 'clinical research', 'drug development', 'drug discovery', 'medicine', 'health']

law_keywords = ['law', 'legal', 'attorney', 'lawyer', 'litigation', 'arbitration', 'dispute resolution', 'contract law', 'intellectual property', 'corporate law', 'labor law', 'tax law', 'real estate law', 'environmental law', 'criminal law', 'family law', 'immigration law', 'bankruptcy law']

sports_keywords = ['sports', 'football', 'basketball', 'baseball', 'hockey', 'soccer', 'golf', 'tennis', 'olympics', 'athletics', 'coaching', 'sports management', 'sports medicine', 'sports psychology', 'sports broadcasting', 'sports journalism', 'esports', 'fitness']

media_keywords = ['media', 'entertainment', 'film', 'television', 'radio', 'music', 'news', 'journalism', 'publishing', 'public relations', 'advertising', 'marketing', 'social media', 'digital media', 'animation', 'graphic design', 'web design', 'video production']

manufacturing_keywords = ['manufacturing', 'production', 'assembly', 'logistics', 'supply chain', 'quality control', 'lean manufacturing', 'six sigma', 'industrial engineering', 'process improvement', 'machinery', 'automation', 'aerospace', 'automotive', 'chemicals', 'construction materials', 'consumer goods', 'electronics', 'semiconductors']

automobile_keywords = ['automotive', 'cars', 'trucks', 'SUVs', 'electric vehicles', 'hybrid vehicles', 'autonomous '
                                                                                                    'vehicles', 'car manufacturing', 'automotive design', 'car dealerships', 'auto parts', 'vehicle maintenance', 'car rental', 'fleet management', 'telematics']

telecom_keywords = ['telecom', 'telecommunications', 'wireless', 'networks', 'internet', 'broadband', 'fiber optics', '5G', 'telecom infrastructure', 'telecom equipment', 'VoIP', 'satellite communications', 'mobile devices', 'smartphones', 'telecom services', 'telecom regulation', 'telecom policy']


digital_world_keywords = [
    "Artificial intelligence", "Machine learning", "Data Science", "Big Data", "Cloud Computing",
    "Cybersecurity", "Information security", "Network security", "Blockchain", "Cryptocurrency",
    "Internet of things", "IoT", "Web development", "Mobile development", "Frontend development",
    "Backend development", "Software engineering", "Software development", "Programming",
    "Database", "Data analytics", "Business intelligence", "DevOps", "Agile", "Scrum",
    "Product management", "Project management", "IT consulting", "IT service management",
    "ERP", "CRM", "SaaS", "PaaS", "IaaS", "Virtualization", "Artificial reality", "AR", "Virtual reality",
    "VR", "Gaming", "E-commerce", "Digital marketing", "SEO", "SEM", "Content marketing",
    "Social media marketing", "User experience", "UX design", "UI design", "Cloud-native",
    "Microservices", "Serverless", "Containerization"
]

industries = {
    'Insurance': insurance_keywords,
    'Finance': finance_keywords,
    'Banking': banking_capital_markets_keywords,
    'Health': healthcare_life_sciences_keywords,
    'Law': law_keywords,
    'Sports': sports_keywords,
    'Entertainment': media_keywords,
    'Manufacturing': manufacturing_keywords,
    'Automobile': automobile_keywords,
    'Telecom': telecom_keywords,
    'Digital World': digital_world_keywords
}

#Topic Modelling on a given text
def preprocess_text(text):
    # Replace this with your own preprocessing code
    # This example simply tokenizes the text and removes stop words
    tokens = gensim.utils.simple_preprocess(text)
    stop_words = gensim.parsing.preprocessing.STOPWORDS
    preprocessed_text = [[token for token in tokens if token not in stop_words]]
    return preprocessed_text

def perform_topic_modeling(transcript_text, num_topics=5, num_words=10):
    # Preprocess the transcript text
    # Replace this with your own preprocessing code
    preprocessed_text = preprocess_text(transcript_text)
    # Create a dictionary of all unique words in the transcripts
    dictionary = corpora.Dictionary(preprocessed_text)
    # Convert the preprocessed transcripts into a bag-of-words representation
    corpus = [dictionary.doc2bow(text) for text in preprocessed_text]
    # Train an LDA model with the specified number of topics
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
    # Extract the most probable words for each topic
    topics = []
    for idx, topic in lda_model.print_topics(-1, num_words=num_words):
        # Extract the top words for each topic and store in a list
        topic_words = [word.split('*')[1].replace('"', '').strip() for word in topic.split('+')]
        topics.append((f"Topic {idx}", topic_words))
    return topics

def label_topic(labelling_text):
    """
        Given a piece of text, this function returns the top two industry labels that best match the topics discussed in the text.
        """
    # Count the number of occurrences of each keyword in the text for each industry
    counts = {}
    for industry, keywords in industries.items():
        count = sum([1 for keyword in keywords if re.search(r"\b{}\b".format(keyword), labelling_text, re.IGNORECASE)])
        counts[industry] = count
    # Get the top five industries based on their counts
    top_industries = heapq.nlargest(5, counts, key=counts.get)

    # If only one industry was found, return it
    if len(top_industries) == 1:
        return top_industries[0]
    # If two industries were found, return them both
    else:
        return top_industries

#Streamlit Code
st.set_page_config(layout='wide')
#Font Style
with open('font.css') as f:
    st.markdown("<style>{}</style>".format(f.read()),unsafe_allow_html=True)

#Display Background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: contain
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('1239346.png')

st.title('TAGIFY')
st.sidebar.image('PngItem_1395774.png')
st.sidebar.header('CHOOSE PLATFORM TO PERFORM')
choice=st.sidebar.selectbox("Select your choice",["Home","Text","CSV"])

if choice=="Home":
    st.subheader('Topic Modelling and Labelling App')
    with st.expander('Web-App Description'):
        st.write("TAGIFY is a cutting-edge web application that empowers users to extract meaningful insights and categorize textual data using state-of-the-art techniques in topic modelling and labelling.")
        st.write("The app is built using a powerful combination of Streamlit and Gensim, providing a "
                 "seamless and intuitive user experience for exploring and understanding topics within large corpora "
                 "of text and CSV files.")
        st.write("The streamlined interface of TAGIFY, powered by Streamlit, ensures simplicity and user-friendliness, allowing users to effortlessly navigate the application and focus on exploring topics and labelling their data with ease.")
        st.write("TAGIFY's  enables users to efficiently explore topics and label their data, making it the most important task at hand.")
elif choice=="Text":
    st.subheader('Topic Modelling and Labeling Web-App on TEXT')
    input=st.text_area('Paste your input text',height=200)
    if input is not None:
        if st.button("Analyze Text"):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.info("Text is below")
                st.success(input)
            with col2:
                # Perform topic modeling on the transcript text
                topics = perform_topic_modeling(input)
                # Display the resulting topics in the app
                st.info("Topics in the Text")
                for topic in topics:
                    st.success(f"{topic[0]}: {', '.join(topic[1])}")
            with col3:
                st.info("Topic Labeling")
                labeling_text = input
                industry = label_topic(labeling_text)
                st.markdown("**Topic Labeling Industry Wise**")
                st.write(industry)
elif choice=="CSV":
    st.subheader('Topic Modelling and Labeling Web-App on CSV file')
    uploaded_file=st.file_uploader('Upload your CSV file',type='csv')
    with st.expander('NOTE'):
        st.write("To perform topic modeling and labeling, please ensure that the uploaded CSV file includes a column titled 'Data' which contains the relevant text.")
    if uploaded_file is not None:
        if st.button('Analyze CSV file'):
            col1,col2=st.columns([2,3])
            with col1:
                st.info('Uploaded CSV file')
                csv_file=uploaded_file.name
                with open(os.path.join(csv_file),'wb') as f:
                    f.write(uploaded_file.getbuffer())
                print(csv_file)
                df=pd.read_csv(csv_file,encoding='unicode_escape')
                st.dataframe(df)
            with col2:
                data_list=df['Data'].to_list()
                industry_list=[]
                for i in data_list:
                    industry_list.append(label_topic(i))
                df['Industry']=industry_list
                st.info('Topic Modelling and Labeling')
                st.dataframe(df)
