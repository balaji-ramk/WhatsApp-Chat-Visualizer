import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def get_file_name(path_to_file):
    return os.path.splitext(os.path.basename(path_to_file))[0]

def get_text(path_to_whatsapp_export, is_zip=True):
    path_to_whatsapp_export = os.path.abspath(path_to_whatsapp_export)
    if is_zip:
        from zipfile import ZipFile
        with ZipFile(path_to_whatsapp_export, 'r') as zObject:
            name_of_file = get_file_name(path_to_whatsapp_export)
            zObject.extractall(path='files/temp/')
        
        with open(os.path.join('files/temp/', name_of_file + '.txt'), 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        with open(path_to_whatsapp_export, 'r', encoding='utf-8') as file:
            text = file.read()
    
    text = text.replace('\u202f', ' ')
    return text

def get_df(text):
    # pattern = re.compile(r"(\d{2}\/\d{2}\/\d{4}),\s(\d{1,2}:\d{2}.[ap]m)\s[-]\s([^:\n]*):\s")
    pattern = re.compile(r"(\d{2}\/\d{2}\/\d{4}),\s(\d{1,2}:\d{2}.?[ap]?m?)\s[-]\s([^:\n]*):\s")

    processed_text = pattern.split(text)
    
    processed_text.pop(0)
    
    dates = processed_text[::4]
    times = processed_text[1::4]
    names = processed_text[2::4]
    messages = processed_text[3::4]

    messages = [i.strip() for i in messages]
    
    df = pd.DataFrame({
        'date': dates,
        'time': times,
        'name': names,
        'message': messages
    })
    
    return df


path = input('Enter file path: ')
is_zip = input('Zip File? (Y/N): ').lower().strip()

df = get_df(get_text(path, is_zip))

names_dict = df['name'].value_counts().to_dict()
plt.pie(names_dict.values(), labels=names_dict.keys(), autopct='%1.1f%%')
plt.show()