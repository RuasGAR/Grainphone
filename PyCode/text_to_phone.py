
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator
from phonemizer.punctuation import Punctuation
from phonemizer.backend.espeak.wrapper import EspeakWrapper
from typing import Dict, List
from translation_dict import ipa_to_arpabet
import pandas as pd
import random

EspeakWrapper.set_library('C:\Program Files\eSpeak NG\libespeak-ng.dll')
DATASET = pd.read_csv('PyCode\production_data.csv', index_col=0)

class TextPhone:
    
    PUNCT = Punctuation(';:,.!"?()-')
    SEPARATOR = Separator(phone=' ', word=None)


    def __init__(self,backend_lang:str) -> None:
        self.language = backend_lang
        self.BACKEND = EspeakBackend(backend_lang)
        self.dataset = DATASET
        self.phonetic_dict = ipa_to_arpabet
        self.speakers = list(DATASET["speaker"].unique())
        self.recordings = list(DATASET["recording_label"].unique())
        self.available_phones = list(DATASET["phone"].unique())

    """ 
        Given a text, usually in a sentence, removes the punctuation and returns a list
        with each word
    """
    def break_text_in_words(self, text:str)->List[str]:
        text = self.PUNCT.remove(text) 
        words = [ w.lower() for w in text.strip().split(' ') if w]
        return words

    """ 
        Given a list of words, returns a dictionary with the words themselvels as keys; and its phonetic
        representation - a list of individual phones - as values;
    """
    def get_lexicon(self, words:List[str]) -> Dict[str, List[str]]:
        
        lexicon = {
            word: self.BACKEND.phonemize([word], separator=self.SEPARATOR,strip=True, njobs=1)[0].split(' ')
            for word in words
        }
        return lexicon            

    """ 
        For some reason, the order in which translations into phonetic representation happens doesn't follow
        the real order of an array - instead, they start from the shortest to the longest word.
        In order to rebuild the order - and the sense - of the original text, we can use both the 
        previously segmented word, as well as its lexicon.
    """

    def rebuild_phrase_with_lexicon(self, words:List[str], lexicon: Dict[str, List[str]]) -> List[List[str]]:
        phrase = []
        for w in words:
            phrase.append(lexicon[w])            
        return phrase
    
    """ 
        We are dealing with 2 translations simultaneously: espeakNG uses IPA official set of Unicode characters,
        which are not represented in the same way as the Buckeye Dataset (which uses ARPAbet, a more english-focused form).
        In order to achieve a translation, I've used ChatGPT to provide me with a mapping between some of the representations
        I had (after phonemizing some samples) and the actual notation in the wav folder structure, for example.
        This function exhaust verificiation to check if the IPA fonema really does not have a form in 
        ARPAbet representation.
        To make things simple, whenever we don't find the phonema, we print it and return a default value
        instead - which obviously compromises the understanding.  
    """

    def check_phonema(self, phone):
        if phone not in self.available_phones:
            try:
                phone = self.phonetic_dict[phone]
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
            return phone
            
    """ 
        For each entry in the dictionary, specifically, for each phone in its repr list,
        it is required to search for the matching audio file of the specific phone.
        Since we actually have more than one speaker, a util-nested structure will be used to add some custom
        randomization, even though the user will never be able to select which speaker to get from.
        The random layer comes in relation to all recordings coming from one or more speakers:
            - same_speaker = True -> all phoneme are going to be retrieved from the same person;
            - same_speaker = False -> can be composed by different speech corpus;
    """

    def get_matching_filepaths(self, phrase:List[List[str]], same_speaker:bool=True) -> List[List[str]]:

        n_speakers = len(self.speakers)-1
        
        n_rand_speaker = random.randint(1, n_speakers)
        random_speaker = f's0{n_rand_speaker}' if n_rand_speaker < 10 else f's{n_rand_speaker}'
    
        if same_speaker:
            search_random_sample = lambda p: self.dataset.query(f'phone=="{p}" and speaker=="{random_speaker}"').sample(1)["wav_path"].values[0]        
        else:
            search_random_sample = lambda p: self.dataset.query(f'phone=="{p}"').sample(1)["wav_path"].values[0]
        
       
        # has to go over the index, so it doesn't create a new copy
        for i in range(len(phrase)):
            try:
                word_in_phone = phrase[i]
                word_in_phone = list(map(self.check_phonema,word_in_phone))
                word_in_phone = list(map(search_random_sample, word_in_phone))
                phrase[i] = word_in_phone
            except Exception as e:
                print("Exception: ",e);
                return None
        return phrase
    
    """ 
        Straightforward script function for getting the final result - a list made of lists 
        of each phoneme path - given an entry text. 
    """

    def granulate(self, text:str, same_speaker:bool=True) -> List[List[str]]:
        words = self.break_text_in_words(text)
        lexicon = self.get_lexicon(words)
        phrase = self.rebuild_phrase_with_lexicon(words, lexicon)
        res = self.get_matching_filepaths(phrase,same_speaker=same_speaker)    
        return res
    
        