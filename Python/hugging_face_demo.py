# -*- coding: utf-8 -*-
"""
demo QA model found here
https://huggingface.co/deepset/roberta-base-squad2
"""

from transformers import TFAutoModelForQuestionAnswering, AutoTokenizer, pipeline

model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"

# a) Get predictions
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
QA_input = {
    'question': 'what do the Dutch call the Amazon?',
    'context': "The Amazon rainforest (Portuguese: Floresta Amazônica or Amazônia; Spanish: Selva Amazónica, Amazonía or usually Amazonia; French: Forêt amazonienne; Dutch: Amazoneregenwoud), also known in English as Amazonia or the Amazon Jungle, is a moist broadleaf forest that covers most of the Amazon basin of South America. This basin encompasses 7,000,000 square kilometres (2,700,000 sq mi), of which 5,500,000 square kilometres (2,100,000 sq mi) are covered by the rainforest. This region includes territory belonging to nine nations. The majority of the forest is contained within Brazil, with 60% of the rainforest, followed by Peru with 13%, Colombia with 10%, and with minor amounts in Venezuela, Ecuador, Bolivia, Guyana, Suriname and French Guiana. States or departments in four nations contain Amazonas in their names. The Amazon represents over half of the planet's remaining rainforests, and comprises the largest and most biodiverse tract of tropical rainforest in the world, with an estimated 390 billion individual trees divided into 16,000 species."
}
res = nlp(QA_input)
print('\nQ: ',
      QA_input['question'],
      '\nA: ',
      res['answer'])

#WTF is this for? - looks like pipeline function takes care of it.
# =============================================================================
# # b) Load model & tokenizer
# model = TFAutoModelForQuestionAnswering.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# =============================================================================

#something with more text
with open(r'C:\Users\JF\Desktop\git_projects\historical-figure-questions\Docs\test_text_2.txt') as f:
    test_text_2 = f.read()
    

QA_input = {
'question': "what was Napoleon's first battle?",
'context': test_text_2
}

res = nlp(QA_input)
print('\nQ: ',
      QA_input['question'],
      '\nA: ',
      res['answer'])