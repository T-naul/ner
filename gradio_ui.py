import gradio as gr
# import os
# os.system('python -m spacy download en_core_web_sm')
import spacy
from spacy import displacy

from index import setup_ner

# nlp = spacy.load("en_core_web_sm")

# def text_analysis(text):
#     doc = nlp(text)
#     html = displacy.render(doc, style="dep", page=True)
#     html = (
#         "<div style='max-width:100%; max-height:360px; overflow:auto'>"
#         + html
#         + "</div>"
#     )
#     pos_count = {
#         "char_count": len(text),
#         "token_count": 0,
#     }
#     pos_tokens = []

#     for token in doc:
#         print(token.text, token.pos_)
#         pos_tokens.extend([(token.text, token.pos_), (" ", None)])
#     print(pos_tokens)

#     return pos_tokens, pos_count, html

classifier = setup_ner(cache_dir='./cache_models/')

def results_ner(result: list):
    temp_results = []
    result_lists = []
    temp_list = [result[0]]
    for i in range(1, len(result)):
        temp_sub = result[i]['start'] - result[i-1]['end'] 
        if temp_sub == 0 or temp_sub == 1:
            temp_list.append(result[i])
        else:
            result_lists.append(temp_list) 
            temp_list = [result[i]] 
    if temp_list:
        result_lists.append(temp_list)
    
    for sublist in result_lists:
        words = [item['word'] for item in sublist]
        combined_word = ''.join(words).replace('▁', ' ').strip()
        pos_word = sublist[0]['entity'].split('-')[-1]
        temp_results.append({'word': combined_word, 'pos': pos_word, 'start': sublist[0]['start'], 'end': sublist[-1]['end']})

    return temp_results

def process_results(results: list, text: str):
    pos_tokens = []
    if results[0]['start'] ==0:
        pos_tokens.extend([(results[0]['word'], results[0]['pos'])])
    else:
        pos_tokens.extend([(text[:results[0]['end']] , None), (results[0]['word'], results[0]['pos'])])
    end = results[0]['end']
    for i in range(1, len(results)):
        pos_tokens.extend([(text[results[i-1]['end']: results[i]['start']] , None), (results[i]['word'], results[i]['pos'])])
        end = results[i]['end']
    
    if end != len(text):
        pos_tokens.extend([(text[end:] , None)])

    return pos_tokens
    
def ner_langchain(text):
    result = classifier(text)
    result = results_ner(result)
    pos_tokens = process_results(result, text)
    return pos_tokens

demo = gr.Interface(
    ner_langchain,
    gr.Textbox(placeholder="Enter sentence here..."),
    # ["highlight", 'json', "html"],
    ["highlight"],
    examples=[
        ["Công Lý là diễn viên hài"],
        ["Alya told Jasmine that Andrew could pay with cash.."],
    ],
)

demo.launch()