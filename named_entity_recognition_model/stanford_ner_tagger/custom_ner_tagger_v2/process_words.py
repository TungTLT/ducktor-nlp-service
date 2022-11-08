train_data = open('train_data.tsv', 'r+')
diseases = open('disease_names.txt', 'r+')
question = open('questions.txt', 'r')

disease_list = diseases.read().split('\n')
sentences = question.read().split('\n')

final_list = []
disease_label = 'DISEASE'
no_name_label = 'O'

for disease in disease_list:
    split_disease = disease.split(' ')
    for sentence in sentences:
        split_words = sentence.split(' ')
        for word in split_words:
            if word != '$':
                final_list.append(word + '  ' + no_name_label + '\n')
            else:
                for s_d in split_disease:
                    final_list.append(s_d + '   ' + disease_label + '\n')
        final_list.append('\n')
    final_list.append('\n')

final_list = final_list[:-1]
train_data.writelines(final_list)

diseases.close()
train_data.close()
