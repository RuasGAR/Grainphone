
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator
from phonemizer.punctuation import Punctuation
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from typing import Dict, List
import pandas as pd
import os

EspeakWrapper.set_library('C:\Program Files\eSpeak NG\libespeak-ng.dll')
DATASET = pd.read_csv('PyCode\production_data.csv', index_col=0)
print(DATASET.head(5))
class TextPhone:
    
    PUNCT = Punctuation(';:,.!"?()-')
    SEPARATOR = Separator(phone=' ', word=None)

    def __init__(self,backend_lang:str) -> None:
        self.language = backend_lang
        self.BACKEND = EspeakBackend(backend_lang)

    def break_text_in_words(self, text:str):
        text = self.PUNCT.remove(text) 
        words = { w.lower() for w in text.strip().split(' ') if w}
        return words

    def get_lexicon(self, words:List[str]) -> Dict[str, List[str]]:
        
        lexicon = {
            word: self.BACKEND.phonemize([word], separator=self.SEPARATOR,strip=True, njobs=1)
            for word in words
        }
        return lexicon            

    def rebuild_phrase_with_lexicon(self, words:List[str], lexicon: Dict[str, List[str]]) -> List[List[str]]:
        
        phrase = []
        
        for w in words:
            phrase.append(lexicon[w])        
        
        return phrase
        

    """ 
        For each entry in the dictionary, specifically, for each phone in its repr list,
        it is required to search for the matching audio file of the specific phone.
        Since we actually have more than one speaker, a util function will be used to add some custom
        randomization, with functionalities such as: taking all of the recordings of a same person, chosen randomly; or 
        every piece from randomly selected people.
    """

    def get_matching_filepaths(self, phrase:List[List[str]]) -> None:
        
        for phone_repr_word in phrase:
            # I need to access the dataset and recover one path for each of the 
            # I can make a simple function that goes after the dataset for it;
            # And then use it to map each phone to its chosen_file;
            #  
            # file_paths
            pass
            
            


    # this function should be static too, see what are the rules for it
    def get_audio_filepath(phone, n_speaker) -> str:

        # have to see how it's going to roll off, how I'm building the database, etc;
        pass

     ##### BEFORE PUSHING, DO THE GIT IGNORE ACCORDING TO THE VENV FILE AND SEE HOW TO SET REQUIREMENTS!!!

if __name__ == "__main__":

    t_2_phone = TextPhone("en-us")
    #teste = "This is the weirdest thing I have ever seen"

"""     result = t_2_phone.break_text_in_words(test_text)
    result = t_2_phone.get_lexicon(result)

    with open('text_symbols.txt', '+a', encoding='utf-8') as f:
        print(len(result.values()))
        for val in result.values():
            for w in val[0].split(' '):
                f.write(f"{w} ")
            f.write("\t")
        f.write('\n') """
        
        