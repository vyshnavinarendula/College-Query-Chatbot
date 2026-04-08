"""
chatbot_engine.py
Core ML engine: TF-IDF vectorisation + Cosine Similarity matching.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


class CollegeChatbot:
    def __init__(self, data_path: str = "college_data.csv"):
        self.df = pd.read_csv(data_path)
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True,
        )
        # Combine question + category for richer matching
        corpus = (
            self.df["Question"] + " " + self.df["Category"]
        ).tolist()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def _clean(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text

    def get_response(self, user_query: str, threshold: float = 0.15):
        """
        Returns (answer, confidence_pct, category, matched_question).
        If best similarity < threshold, returns a fallback response.
        """
        cleaned = self._clean(user_query)
        vec = self.vectorizer.transform([cleaned])
        sims = cosine_similarity(vec, self.tfidf_matrix).flatten()
        best_idx = int(np.argmax(sims))
        best_score = float(sims[best_idx])

        if best_score < threshold:
            return (
                "I'm sorry, I don't have information on that topic. "
                "Please contact the admissions office at admissions@college.edu "
                "or call +91-98765-43210.",
                best_score * 100,
                "Unknown",
                "",
            )

        row = self.df.iloc[best_idx]
        return (
            row["Answer"],
            round(best_score * 100, 1),
            row["Category"],
            row["Question"],
        )

    def get_all_categories(self):
        return sorted(self.df["Category"].unique().tolist())

    def get_questions_by_category(self, category: str):
        return self.df[self.df["Category"] == category]["Question"].tolist()
