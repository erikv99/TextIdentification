# Opdracht: Tekstidentificatie
#
# Naam: Erik V

from os.path import exists

class TextModel():
    """A class supporting complex models of text."""

    # Class properties
    text = ""

    def __init__(self):
        """
            Create an empty TextModel.
        """
        
        """
            From top to bottom:
            wordCount: Amount of words used in the model (om woorden te tellen)
            wordLength: Length of the words (om woordlengtes te tellen)
            stems: stems (om stammen te tellen)
            sentenceLenghts: lengths of the sentences
            numericCount: Amount of used numbers (0 - 9) 
        """

        # For keeping track of word count per sentence occurences
        self.words = {}

        # For keeping track of word length occurences
        self.word_lengths = {}

        # STEMS
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

    def _get_sentences(self): 
        """
            Returns a list containing every sentence present in self.text
        """

        # replacing every ? and ! with a ., then splitting on every . so we effectifly splitted on every !, ? or .
        sentences = self.text.replace("?", ".").replace("!", ".").split(".")

        # Spliting on . can leave us with an extra element so we filter this empty element out and return the result.
        return list(filter(None, sentences))

    def make_sentence_lengths(self):
        """
            Gets the length of each sentence and assigns it to the sentences property
            Length: amount of words in a sentence.
        """

        sentences = self._get_sentences()

        for sentence in sentences:
            
            # Getting all words for the current sentence by splitting on each space.
            words_in_sentence = sentence.split(" ")

            # Getting the length of all the words in the sentence.
            sentence_length = len(words_in_sentence)

            # Checking if the sentence_lengths dictionary already contains a entry for the current sentence length.
            if sentence_length in self.sentence_lengths:

                # Increasing the count of it.
                self.sentence_lengths[sentence_length] += 1

            else:

                # Setting count to 1.
                self.sentence_lengths[sentence_length] = 1

tm = TextModel()

test_text = """Dit is een korte zin. Dit is geen korte zin, omdat
deze zin meer dan 10 woorden en een getal bevat! Dit is
geen vraag, of wel?"""

tm.read_text_from_file('test.txt')
assert tm.text == test_text

tm.make_sentence_lengths()
assert tm.sentence_lengths == {16: 1, 5: 1, 6: 1}