import random
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
import nltk

kw_model = KeyBERT()

def keyword_extractor(chunk:str):

    keywords = kw_model.extract_keywords(chunk, keyphrase_ngram_range=(1,2), stop_words='english', top_n=1)
    topic = keywords[0][0] if keywords else "artificial intelligence"
    return topic

def prompter(keyword:str):
    templates = [
        "Can you explain {}?",
        "What can you tell me about {}?",
        "Give me an overview of {}.",
        "Could you describe {} in detail?",
        "In simple terms, what is {}?"
    ]

    prompt = random.choice(templates).format(keyword)
    return prompt

def text_chunker(text:str):

    nltk.download('punkt')

    model = SentenceTransformer('all-MiniLM-L6-v2')

    sentences = nltk.sent_tokenize(text)

    # encoding
    embeddings = model.encode(sentences, convert_to_tensor=True)

    # grouping sentences

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = util.cos_sim(embeddings[i-1], embeddings[i]).item()
        if sim < 0.7:  # threshold for topic change
            chunks.append(" ".join(current_chunk))
            current_chunk = []
        current_chunk.append(sentences[i])

    chunks.append(" ".join(current_chunk))

    return chunks