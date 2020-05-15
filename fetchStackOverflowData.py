from stackapi import StackAPI
import html
import csv

def tags_to_string(tags):
    tags_concatenadas = ""
    for tag in tags:
        tags_concatenadas += f"{tag}, "
    return tags_concatenadas.rstrip(', ')

def get_questions(path):
    conseguiu_recuperar = False
    while(conseguiu_recuperar is False):
        try:
            STACK_SITE = StackAPI('stackoverflow')
            STACK_SITE.max_pages=1
            top_viewed_questions = STACK_SITE.fetch('questions', sort='votes', order='desc')
            conseguiu_recuperar = True
        except:
            print("Ocorreu um erro")
    
    for question in top_viewed_questions["items"]:
        question['tags'] = tags_to_string(question['tags'])
        question['title'] = html.unescape(question['title'])
    
    return top_viewed_questions

def questions_to_csv(questions, path_csv):
    path_csv += "\\stackoverflow.csv"
    
    with open(path_csv, mode='w+') as arquivo_csv:
        csv_writer = csv.writer(arquivo_csv, quotechar='"')
    
        header = (["question_id", "view_count", "answer_count", "score", "title", "tags", "link"])
        csv_writer.writerow(header)
        for question in questions["items"]:
            dict_question_info = {0: question['question_id'], 1: question['view_count'], 2: question['answer_count'],
                                3: question['score'], 4: question['title'], 5: question['tags'], 6: question['link']}
            csv_writer.writerow(dict_question_info.values())

def main_script(): 
    path_questions = str(pathlib.Path().absolute()) + "\\stackoverflow"
    questions = get_questions(path_questions)
    questions_to_csv(questions, path_questions)