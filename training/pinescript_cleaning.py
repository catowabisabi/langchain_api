import os
import json
import re
import random
import numpy as np
import pandas as pd
from zipfile import ZipFile
from nltk.tokenize import sent_tokenize
from docx import Document

def clean_code(code):
    code = re.sub(r'//.*', '', code)  # 去除單行註釋
    code = re.sub(r'/\*.*\*/', '', code, flags=re.DOTALL)  # 去除多行註釋
    code = re.sub(r'\s+', ' ', code)  # 去除多餘的空白
    #code = re.sub(r'\bsecurity\b\([^)]*\)', '', code)
    return code.strip()

def read_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])

    # 查找版本號
    version_pattern = r'//\s*version\s*=\s*(\d+)'
    version_match = re.search(version_pattern, text)

    if version_match:
        version = version_match.group(1)
    else:
        version = None

    return text, version

def create_json_dataset(dataset, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

def process_code(text):
    code = clean_code(text)
    sentences = sent_tokenize(code)
    return sentences

def split_train_test_val(dataset, test_ratio=0.2, val_ratio=0.1):
    random.shuffle(dataset)
    test_split_index = int(len(dataset) * (1 - test_ratio))
    val_split_index = int(len(dataset) * (1 - test_ratio - val_ratio))
    train_set = dataset[:val_split_index]
    val_set = dataset[val_split_index:test_split_index]
    test_set = dataset[test_split_index:]
    return train_set, val_set, test_set

def format_data(sentences):
    df = pd.DataFrame(sentences, columns=['sentence'])
    return df

def process_versions(dataset, version_mapping):
    for data in dataset:
        data['version'] = version_mapping[data['file_name']]

def main():
    input_folder = 'pinescripts'
    output_file = 'dataset.json'

    dataset = []
    version_mapping = {}  # 假設您有一個包含文件名和版本的映射字典

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.docx'):
            file_path = os.path.join(input_folder, file_name)

            # 讀取並處理文件
            text, version = read_docx(file_path)
            sentences = process_code(text)

            # 添加到資料集
            for sentence in sentences:
                dataset.append({
                    'file_name': file_name,
                    'version': version,
                    'sentence': sentence
                })

    process_versions(dataset, version_mapping)
    
    train_set, val_set, test_set = split_train_test_val(dataset)

    train_df = format_data([data['sentence'] for data in train_set])
    val_df = format_data([data['sentence'] for data in val_set])
    test_df = format_data([data['sentence'] for data in test_set])

    create_json_dataset({
        'train_set': train_set,
        'val_set': val_set,
        'test_set': test_set,
        'train_df': train_df.to_dict(orient='records'),
        'val_df': val_df.to_dict(orient='records'),
        'test_df': test_df.to_dict(orient='records')
    }, output_file)

    print(f"Dataset created and saved to {output_file}")

if __name__ == '__main__':
    main()
