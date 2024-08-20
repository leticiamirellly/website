

import os
from langchain_community.document_loaders import JSONLoader
import json
from pprint import pprint
import jq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup


class RagService:
    def __init__(self):
        print('Rag Service')
        

    def clean_documents(self, documents):        
        soup = BeautifulSoup(documents, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def chunk_section(self, item, content):
        chunk_size = 600
        chunk_overlap = 15
        
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n", "<h1>","<h2>","<h3>", "<h4>", " "],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len)      
        
        split_chunks = text_splitter.create_documents(texts=[content])
        chunks = []
        for i, chunk in enumerate(split_chunks):
            chunk_item = {
                'title': item.get('title'),
                'pubDate': item.get('pubDate'),
                'link': item.get('link'),
                'guid': item.get('guid'),
                'author': item.get('author'),
                'thumbnail': item.get('thumbnail'),
                'content': chunk,
                'enclosure': item.get('enclosure'),
                'categories': item.get('categories')
            }
            chunks.append(chunk_item)
        return chunks
    
    async def get_message(self, message):
        data_bytes = message['data']
        data_str = data_bytes.decode('utf-8')
        data_dict = json.loads(data_str)        
        if isinstance(data_dict, list):
            sections = []
            for i, item in enumerate(data_dict):
                content = item['content']                                
                cleaned_content_item = self.clean_documents(content)
                section_mapped = self.chunk_section(item, cleaned_content_item)
                sections.append(section_mapped)
        print(sections[0][0])        
                


# export interface data_dict {
#     title:       string;
#     pubDate:     Date;
#     link:        string;
#     guid:        string;
#     author:      string;
#     thumbnail:   string;
#     description: string;
#     content:     string;
#     enclosure:   Enclosure;
#     categories:  string[];
# }
