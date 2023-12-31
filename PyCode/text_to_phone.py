from collections import dict
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator
from phonemizer.punctuation import Punctuation

PUNCT = Punctuation(';:,.!"?()-')
BACKEND = EspeakBackend('pt_pt')
SEPARATOR = Separator(phone=' ', word=None)

class TextPhone:

    """ phone_audio_features should contain a dictionary of dicts with MFCC, Spectral Centroid, Spectral ... """

    def __init__(self, text:str) -> None:
        self.text = PUNCT.remove(text)
        self.lexicon = dict()
        self.phone_filepaths = []
        self.phone_files = []
        self.phone_audio_features = dict()

    """ 
        A lexicon is the actual representation in phonema, especially considering its formatting features.
        Each of the words are broken into phone units (a py list) after removing the punctuation marks. (should I really
        remove it? maybe it induces entonnation...)
        composing a larger dictionary in the format:

        { word: [word's phones separated by Separator]}
    """
    def create_lexicon(self) -> None:
        
        # Segments the sentence in word units 
        words = [w.lower() for w in self.text.strip().split(' ') if w]

        self.lexicon = BACKEND.phonemize("teste", njobs=4)

    """ 
        For each entry in the dictionary, specifically, for each phone in its repr list,
        it is required to search for the matching audio file of the specific phone.
        Since we actually have more than one speaker, a util function will be used to add some custom
        randomization, with functionalities such as: taking all of the recordings of a same person, chosen randomly; or 
        every piece from randomly selected people.
    """

    def get_matching_filepaths(self, mode:str) -> None:
        
        for key, value in self.lexicon.items():
            for phone, i in iter(value):
                if(mode=="multi_speakers"):
                    # one random speaker for each phone, in each word
                    speakers = [0] * len(value)
                    self.phone_filepaths[key] = self.get_audio_filepath(phone, n_speaker=speakers[i]) 


    # this function should be static too, see what are the rules for it
    def get_audio_filepath(phone, n_speaker) -> str:

        # have to see how it's going to roll off, how I'm building the database, etc;
        pass

     ##### BEFORE PUSHING, DO THE GIT IGNORE ACCORDING TO THE VENV FILE AND SEE HOW TO SET REQUIREMENTS!!!
