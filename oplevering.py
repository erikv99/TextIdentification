# Opdracht: Tekstidentificatie
#
# Naam: Erik V

from os.path import exists
import string
import nltk
from nltk.stem.snowball import SnowballStemmer

class TextModel():
    """A class supporting complex models of text."""

    # Class properties
    text = ""

    def __init__(self):
        """
            Create an empty TextModel.
        """

        # For keeping track of word count per sentence occurences
        self.words = {}

        # For keeping track of word length occurences
        self.word_lengths = {}

        # For keeping track the amount of occurences for each found stem.
        self.stems = {}

        # For keeping track of sentence length occurences
        self.sentence_lengths = {}

        # Amount of numbers
        self.numeric_count = {}

    def __repr__(self):
        """
            Display the contents of a TextModel in a readable manner
        """
        
        representation = 'Amount of words:\n' + str(self.words) + '\n\n'
        representation += 'Length of words:\n' + str(self.word_lengths) + '\n\n'
        representation += 'Stems:\n' + str(self.stems) + '\n\n'
        representation += 'Sentence lengths:\n' + str(self.sentence_lengths) + '\n\n'
        representation += 'Amount of used numbers:\n' + str(self.numeric_count)
        return representation

    def read_text_from_file(self, filename):
        """
            Attemtps to read the content of the file at the given path in to the text property
            Arg filename: path to the file to read
        """

        # Checking if the file exists, if not printing a log and returning.
        if not exists(filename):
            
            print("Given path '{}' is not valid".format(filename))
            return

        all_lines = []

        # Opening the file with a context manager so we're no longer responsible for closing it.
        with open(filename) as input_file:

            # Reading all lines from the file to a list
            all_lines = input_file.readlines()

        # Checking if the file contains any content else sending a log and returning.
        if len(all_lines) == 0:

            print("File at given path '{}' is empty!".format(filename))
            return

        self.text = "".join(all_lines)

    def get_sentences(self): 
        """
            Returns a list containing every sentence present in self.text
        """

        # replacing every ? and ! with a ., then splitting on every . so we effectifly splitted on every !, ? or .
        sentences = self.text.replace("?", ".").replace("!", ".").split(".")

        # Spliting on . can leave us with an extra element so we filter this empty element out and return the result.
        return list(filter(None, sentences))

    def increment_or_create(self, dir, key):
        """
            Tries to increment the amount for the given key, if not found adds it with the count 1
        """

        # If added ealier we increase the count
        if key in dir:
            dir[key] += 1

        # If not present yet we add it.
        else:
            dir[key] = 1

        return dir

    def make_sentence_lengths(self):
        """
            Gets the length of each sentence and assigns it to the sentences property
            Length: amount of words in a sentence.
        """

        sentences = self.get_sentences()
        sentence_lengths = {}

        for sentence in sentences:
            
            # Getting all words for the current sentence by splitting on each space.
            words_in_sentence = sentence.split(" ")

            # Getting the length of all the words in the sentence.
            sentence_length = len(words_in_sentence)

            # Incrementing if it exists, creating if it does not.
            sentence_lengths = self.increment_or_create(sentence_lengths, sentence_length)

        self.sentence_lengths = sentence_lengths

    def clean_string(self, s):
        """
            Makes given string lowercase and removes and punctuations
        """
        
        # Making word lowercase and using translate to remove any punctuation.
        return s.lower().translate(str.maketrans('', '', string.punctuation))

    def get_all_words(self):
        """
            Will return all words stored in self.text
        """

        # Returning all words by splitting on any space, removing any empty elements in the result.
        return list(filter(None, self.text.split(" ")))

    def split_newline_divided_words(self, words):
        """
            Splits any words sticked togheter ('omdat\ndeze') in order to get a accurate list of just singulair words.
        """

        clean_words = []

        for word in words:

            if ("\n" in word):

                for splitted_word in word.split("\n"):
                    clean_words.append(splitted_word)

            else:

                clean_words.append(word)

        return clean_words

    def get_all_words_sanitized(self):
        """
            Returns a list of all words but fully sanitized and ready for usage.
        """

        words = [self.clean_string(word) for word in self.get_all_words()]

        # since a 2 words can still count as one because it is formatted like this 'hello\nworld' we also need to handle that.
        # if we dont handle it we cant get the result given by school for testing.
        return self.split_newline_divided_words(words)

    def make_word_lengths(self):
        """
            Returns a dictionary containing every word length (amount of chars in a word)
            and how many times this specific length occurred in the text.
            arg words: dictionary of sentence numbers and all words for each sentence number.
            Assigns output to self.word_lengths
        """

        word_lengths = {}

        for word in self.get_all_words_sanitized():

            # Getting length of current word.
            word_length = len(word)

            # Incrementing if  existing, else creating in dir.
            word_lengths = self.increment_or_create(word_lengths, word_length)

        self.word_lengths = word_lengths

    def make_words(self):
        """
            Returns a dictionary containing every word and how many times they were present in the text
            arg words: dictionary of words and the amount of times they were found.
            Assigns output to self.words
        """

        words = {}

        for word in self.get_all_words_sanitized():

            # Incrementing if already existing in dir, else creating
            words = self.increment_or_create(words, word)

        self.words = words
    
    def make_stems(self):
        """
            Fills the self.stems dictionary with the stems for each word and
            the amount of times they were found.
            Assigns output to self.stems
        """

        snow_stemmer = SnowballStemmer(language='dutch')
        stems = {}

        for word in self.get_all_words_sanitized():

            stem = snow_stemmer.stem(word)

            # Incrementing if already existing in dir, else creating
            stems = self.increment_or_create(stems, stem)

        self.stems = stems


tm = TextModel()

test_text = """Dit is een korte zin. Dit is geen korte zin, omdat
deze zin meer dan 10 woorden en een getal bevat! Dit is
geen vraag, of wel?"""

tm.read_text_from_file('test.txt')
assert tm.text == test_text

tm.make_sentence_lengths()
assert tm.sentence_lengths == {16: 1, 5: 1, 6: 1}

clean_text = """dit is een korte zin dit is geen korte zin omdat
deze zin meer dan 10 woorden en een getal bevat dit is
geen vraag of wel"""
clean_s = tm.clean_string(tm.text)
assert clean_s == clean_text

tm.make_word_lengths()
assert tm.word_lengths == {2: 6, 3: 10, 4: 4, 5: 6, 7: 1}

tm.make_words()
assert tm.words == {
  'dit': 3, 'is': 3, 'een': 2, 'korte': 2, 'zin': 3, 'geen': 2,
  'omdat': 1, 'deze': 1, 'meer': 1, 'dan': 1, '10': 1, 'woorden': 1,
  'en': 1, 'getal': 1, 'bevat': 1, 'vraag': 1, 'of': 1, 'wel': 1
}

tm.make_stems()
test = tm.stems
assert tm.stems == {
  'dit': 3, 'is': 3, 'een': 2, 'kort': 2, 'zin': 3, 'gen': 2,
  'omdat': 1, 'dez': 1, 'mer': 1, 'dan': 1, '10': 1, 'woord': 1,
  'en': 1, 'getal': 1, 'bevat': 1, 'vrag': 1, 'of': 1, 'wel': 1
}