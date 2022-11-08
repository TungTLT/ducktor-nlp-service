import nltk
from nltk.tag.stanford import StanfordNERTagger
from pathlib import Path

folder_location = Path(__file__).absolute().parent

engine_path = f'{folder_location}/stanford_ner_tagger/stanford-ner.jar'
custom_model_path = f'{folder_location}/stanford_ner_tagger/disease_tagger.ser.gz'
disease_tagger = StanfordNERTagger(custom_model_path, engine_path, encoding='utf8', java_options='-mx4g')


def get_disease_tagger_words(user_input):
    words = nltk.word_tokenize(user_input)
    entities = disease_tagger.tag(words)
    entities = filter(lambda x: x[1] == 'DISEASE', entities)
    return ' '.join(list(x[0] for x in entities))
