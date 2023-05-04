from typing import Optional, List, Set, Tuple, Union, Dict
from keras.preprocessing.text import Tokenizer
from nltk.tokenize.regexp import RegexpTokenizer
from keras.utils import pad_sequences
from keras.engine.sequential import Sequential
import pickle
import nltk
from nltk.corpus import stopwords
from keras.models import load_model
from dataclasses import dataclass
import numpy as np

STOP_WORDS: Optional[Set[str]] = None
MAX_WORD_COUNT = 5
LABELS = ('manipulation', 'profanity', 'advertisement', 'begging', 'normal')


class ModelNotLoadException(Exception):
    def __init__(self):
        super().__init__("Model not load")


class TokenizerNotLoadException(Exception):
    def __init__(self):
        super().__init__("Tokenizer not load")


def init_stopwords_nltk():
    global STOP_WORDS

    nltk.download("stopwords")
    stop_words = set(stopwords.words('russian'))
    stop_words.update(['.', ',', '"', "'", ':', ';', '(', ')', '[', ']', '{', '}'])

    STOP_WORDS = stop_words


def preprocess_input(text: str, stop_words: Set[str]) -> List[str]:
    processed_docs = []
    tokens = RegexpTokenizer(r'\w+').tokenize(text)
    filtered = [word for word in tokens if word not in stop_words]
    return filtered


def vectorize_input(processed_docs: List[str], tokenizer: Tokenizer) -> List[List[int]]:
    return pad_sequences(tokenizer.texts_to_sequences(processed_docs), maxlen=64)


class PredictResult:
    separate_result: List[Tuple[str, np.array]]
    total_result: np.array
    text: str
    max_separates_len: int

    def __init__(self, separate_result):
        self.separate_result = separate_result
        self.total_result = self.calculate_total_result(separate_result)
        self.text = self.calculate_text(separate_result)
        self.max_separates_len = max(map(lambda x: len(x[0]), separate_result))

    @staticmethod
    def calculate_total_result(separate_result) -> np.array:
        funcs = (max, max, max, max, min)
        return np.array([funcs[i]([x[1][i] for x in separate_result]) for i in range(5)])

    @staticmethod
    def calculate_text(separate_result):
        return " ".join(map(lambda x: x[0], separate_result))

    def get_max_result(self):
        return np.max(self.total_result)

    def get_max_label(self):
        return LABELS[np.argmax(self.total_result)]

    def __repr__(self):
        return "<Prediction for \"{:.20}...\": {} with probability {:%}>".format(
            self.text,
            self.get_max_label(),
            self.get_max_result()
        )

    def __str__(self):
        return repr(self)

    def get_scores(self) -> Dict[str, List[Tuple[float, str]]]:
        return {LABELS[i]: [
            (proba[i], text)
            for text, proba in self.separate_result
            if np.argmax(proba) == i
        ] for i in range(len(LABELS))}

    def get_human_readable_separates(self) -> str:
        format_str = '{text:^{max_sep_len}} | {_class:^13} | {prob}'
        header = format_str.format(
            text="text",
            max_sep_len=self.max_separates_len,
            _class="class",
            prob="prob, %"
        )
        lines = [format_str.format(
            text=text,
            _class=LABELS[np.argmax(res)],
            prob=np.max(res) * 100,
            max_sep_len=self.max_separates_len
        ) for text, res in self.separate_result]
        return "\n".join([header] + lines)


class ClassifierModule:
    _model: Optional[Sequential] = None
    _tokenizer: Optional[Tokenizer]

    def __init__(self, path_to_model: Optional[str], path_to_tokenizer: Optional[str], init_stopwords=True):
        if path_to_model is not None:
            self.load_model(path_to_model)
        if path_to_tokenizer is not None:
            self.load_tokenizer(path_to_tokenizer)
        if init_stopwords:
            init_stopwords_nltk()

    def load_model(self, path_to_model: str, raise_exception: bool = False):
        try:
            self._model = load_model(path_to_model)
        except Exception as e:
            self._model = None
            if raise_exception:
                raise e

    def get_model(self, raise_exception: bool = False):
        if self._model is None and raise_exception:
            raise ModelNotLoadException
        return self._model

    def load_tokenizer(self, path_to_tokenizer: str, raise_exception: bool = False):
        try:
            with open(path_to_tokenizer, "rb") as f:
                self._tokenizer = pickle.load(f)
        except Exception as e:
            self._tokenizer = None
            if raise_exception:
                raise e

    def get_tokenizer(self, raise_exception: bool = False):
        if self._tokenizer is None and raise_exception:
            raise TokenizerNotLoadException
        return self._tokenizer

    def _predict(self, data: List[str], verbose: int | str = 0):
        word_seq = vectorize_input(data, self.get_tokenizer(raise_exception=True))
        return self.get_model(raise_exception=True).predict(word_seq, verbose=verbose)

    def predict_one(self, text: str, max_words: Optional[int] = MAX_WORD_COUNT, verbose: int | str = 0):
        text = preprocess_input(text, STOP_WORDS)
        lines = []
        if max_words is not None:
            for i in range(max_words, len(text) + 1, max_words):
                lines.append(" ".join(text[i - max_words:i]))
            if len(text) % max_words > 0:
                lines.append(" ".join(text[-(len(text) % max_words):]))
        else:
            lines.append(" ".join(text))
        return PredictResult([(line, res) for line, res in zip(lines, self._predict(lines, verbose))])

    def predict_many(self, data: List[str], max_words: Optional[int] = MAX_WORD_COUNT, verbose: int | str = 0):
        return list(map(lambda x: self.predict_one(x, max_words, verbose), data))