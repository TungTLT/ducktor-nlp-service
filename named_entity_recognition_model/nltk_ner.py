import nltk
from nltk.tag.stanford import StanfordNERTagger
from pathlib import Path


folder_location = Path(__file__).absolute().parent

input3 = 'The fate of Lehman Brothers, the beleaguered investment bank, hung in the balance on Sunday as Federal ' \
         'Reserve officials and the leaders of major financial institutions continued to gather in emergency meetings ' \
         'trying to complete a plan to rescue the stricken bank.  Several possible plans emerged from the talks, ' \
         'held at the Federal Reserve Bank of New York and led by Timothy R. Geithner, the president of the New York ' \
         'Fed, and Treasury Secretary Henry M. Paulson Jr. Gastroenteritis'

engine_path = f'{folder_location}/stanford_ner_tagger/stanford-ner.jar'
model_path_3 = f'{folder_location}/stanford_ner_tagger/english.all.3class.distsim.crf.ser.gz'
custom_model_path = f'{folder_location}/stanford_ner_tagger/disease_recognize.ser.gz'

entity_tagger_3 = StanfordNERTagger(model_path_3, engine_path, encoding='utf8')
entity_tagger_custom = StanfordNERTagger(custom_model_path, engine_path, encoding='utf8')

words = nltk.word_tokenize(input3)
entities = entity_tagger_custom.tag(words)
print(entities)