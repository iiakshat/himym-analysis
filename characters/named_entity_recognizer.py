import os
import sys
import pathlib
import spacy
import pandas as pd
from ast import literal_eval
from nltk.tokenize import sent_tokenize

folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path, "../"))

from utils import load_subs

class NamedEntityRecognizer:
    def __init__(self):
        
        self.model = self.load_model()

    def load_model(self):
        nlp = spacy.load("en_core_web_trf")
        return nlp
    
    def get_chars_inference(self, script):
        script_sents = sent_tokenize(script)
        chars = [] 

        for sent in script_sents:
            doc = self.model(sent)
            char = set()

            for entity in doc.ents:
                if entity.label_ == "PERSON":
                    name  = entity.text.strip().split(" ")[0]
                    char.add(name)

            chars.append(char)

        return chars
    
    def get_chars(self, dataset_path, save_path=None):

        if save_path and not save_path.endswith(".csv"):
            save_path += "chars.csv"
        
        if save_path and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df["chars"] = df["chars"].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
            return df

        df = load_subs(dataset_path)

        df["chars"] = df["script"].apply(self.get_chars_inference)

        if save_path:
            df.to_csv(save_path, index=False)

        return df