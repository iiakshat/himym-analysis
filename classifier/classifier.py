import os
import sys
import pathlib
import nltk
import torch
import numpy as np
import pandas as pd
from transformers import pipeline
from nltk.tokenize import sent_tokenize

folder_name = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(folder_name, "../"))
from utils import load_subs

nltk.download("punkt")
nltk.download("punkt_tab")

class ThemeClassifier:
    def __init__(self, theme_list):
        self.model = "facebook/bart-large-mnli"
        self.device = 0 if torch.cuda.is_available() else "cpu"
        self.theme_list = theme_list
        self.theme_classifier = self.load_model(self.device)

    def load_model(self, device):
        clf = pipeline("zero-shot-classification",
                        model=self.model, 
                       device=device)

        return clf
    
    def get_theme_inference(self, script):

        script_sentences = sent_tokenize(script)
        sentence_batch_size = 20
        script_batches = []
        for index in range(0, len(script_sentences), sentence_batch_size):
            script_batches.append("".join(script_sentences[index:index + sentence_batch_size]))

        theme_output = self.theme_classifier(
            script_batches,
            self.theme_list,
            multi_label=True
        )

        themes = {}
        for output in theme_output:
            for label, score in zip(output["labels"], output["scores"]):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)
        
        themes = {key:np.mean(np.array(value)) for key, value in themes.items()}
        return themes

    def get_themes(self, path, save_path=None):
        
        # Read Save Output if Exists
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            return df
        
        # Load dataset
        df = load_subs(path)

        # Run Inference
        op = df["script"].apply(self.get_theme_inference)

        theme_df = pd.DataFrame(op.tolist())
        df[theme_df.columns] = theme_df

        # Save Output
        if save_path:
            df.to_csv(save_path, index=False)
            
        return df