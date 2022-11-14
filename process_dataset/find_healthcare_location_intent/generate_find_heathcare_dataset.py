healthcare_noun = open('healthcare_noun.txt', 'r')
question_list = open('questions.txt', 'r')

healthcare_sym = healthcare_noun.read().split('\n')
questions = question_list.read().split('\n')

final_list = []

for noun in healthcare_sym:
    for question in questions:
        replaced_question = question.replace('$', noun)
        final_list.append(replaced_question)

print(final_list)