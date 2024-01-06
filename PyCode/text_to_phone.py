
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator
from phonemizer.punctuation import Punctuation
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from typing import Dict, List
from translation_dict import ipa_to_arpabet
import pandas as pd
import os

EspeakWrapper.set_library('C:\Program Files\eSpeak NG\libespeak-ng.dll')
DATASET = pd.read_csv('PyCode\production_data.csv', index_col=0)

class TextPhone:
    
    PUNCT = Punctuation(';:,.!"?()-')
    SEPARATOR = Separator(phone=' ', word=None)

    def __init__(self,backend_lang:str) -> None:
        self.language = backend_lang
        self.BACKEND = EspeakBackend(backend_lang)
        self.dataset = DATASET
        self.available_phones = list(DATASET["phone"].unique())
        self.phonetic_dict = ipa_to_arpabet

    def break_text_in_words(self, text:str):
        text = self.PUNCT.remove(text) 
        words = { w.lower() for w in text.strip().split(' ') if w}
        return words

    def get_lexicon(self, words:List[str]) -> Dict[str, List[str]]:
        
        lexicon = {
            word: self.BACKEND.phonemize([word], separator=self.SEPARATOR,strip=True, njobs=1)[0].split(' ')
            for word in words
        }
        return lexicon            

    def rebuild_phrase_with_lexicon(self, words:List[str], lexicon: Dict[str, List[str]]) -> List[List[str]]:
        phrase = []
        for w in words:
            phrase.append(lexicon[w])            
        return phrase
    
    def check_phonema(self, phone):
        if phone not in self.available_phones:
            try:
                phone = self.phonetic_dict[phone]
                print(phone)
                if phone not in self.available_phones:
                    print("NOT_FOUND: Unavailable phone audio, even after conversion. Default applied.")
                    print(f"Associated Phone: {phone}")
                    print("\n")
                    return "aa"
                else:
                    return phone
            except KeyError as e:
                print("KEY_ERROR: Unavailable phone audio. Default applied.")
                print(f"Associated Phone: {e}")
                print("\n")
                return "aa"
        else:
            return "aa"
            
    """ 
        For each entry in the dictionary, specifically, for each phone in its repr list,
        it is required to search for the matching audio file of the specific phone.
        Since we actually have more than one speaker, a util function will be used to add some custom
        randomization, with functionalities such as: taking all of the recordings of a same person, chosen randomly; or 
        every piece from randomly selected people.
    """

    def get_matching_filepaths(self, phrase:List[List[str]]) -> List[List[str]]:
        
        # query lambda function -> select a random sample from the phone category
        # and retrieve its wav path
        search_random_sample = lambda p: self.dataset.query(f'phone == "{p}"').sample(1)["wav_path"].values[0]
       
        # has to go over the index, so it doesn't create a new copy
        for i in range(len(phrase)):
            try:
                word_in_phone = phrase[i]
                word_in_phone = list(map(self.check_phonema,word_in_phone))
                word_in_phone = list(map(search_random_sample, word_in_phone))
                phrase[i] = word_in_phone
            except Exception as e:
                print(e);
                return None
        return phrase

if __name__ == "__main__":

    t_2_phone = TextPhone("en-us")
    test = "This is the weirdest thing I have ever seen"
    test_words = t_2_phone.break_text_in_words(test)
    test_lex = t_2_phone.get_lexicon(test_words)
    test_phrase = t_2_phone.rebuild_phrase_with_lexicon(test_words, test_lex)
    res = t_2_phone.get_matching_filepaths(test_phrase)

    print(res)
    

"""     result = t_2_phone.break_text_in_words(test_text)
    result = t_2_phone.get_lexicon(result)

    with open('text_symbols.txt', '+a', encoding='utf-8') as f:
        print(len(result.values()))
        for val in result.values():
            for w in val[0].split(' '):
                f.write(f"{w} ")
            f.write("\t")
        f.write('\n') """
        
        