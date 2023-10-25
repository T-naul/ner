import gradio as gr
from index import setup_ner

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
    if result:
        result = results_ner(result)
        pos_tokens = process_results(result, text)
    else:
        pos_tokens = [(text, None)]
    return pos_tokens

demo = gr.Interface(
    ner_langchain,
    gr.Textbox(placeholder="Enter sentence here...", show_label=False, lines=2),
    # ["highlight", 'json', "html"],
    ["highlight"],
    examples=[
        ["Công Lý là diễn viên hài"],
        ["Alya told Jasmine that Andrew could pay with cash.."],
        ["The conference will be held in New York City next week, and John Smith from ABC Inc. will be one of the speakers. He will talk about AI technology and its impact on the business world."]
    ],
    title='NAME ENTITY RECOGNITION',
    article="""
                <br><br><br>
                <div>
                    <h1>Name entity recognition tags:</h1>
                    <ul style="list-style-type: none;">
                        <li style="margin-left: 30px;">- PER (Person)</li>
                        <li style="margin-left: 30px;">- LOC (Location)</li>
                        <li style="margin-left: 30px;">- MISC (Miscellaneous)</li>
                        <li style="margin-left: 30px;">- ORG (Organization)</li>
                        <li style="margin-left: 30px;">- O (Other)</li>
                    </ul>
                </div>
            """,
)

demo.launch()