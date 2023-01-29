# Opdracht: Tekstidentificatie
#
# Naam: Erik V

from heapq import merge
from os.path import exists
import string
import nltk
import math
from nltk.stem.snowball import SnowballStemmer
from tabulate import tabulate

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

        # Amount of punctuations 
        self.punctuations = {}

    def __repr__(self):
        """
            Display the contents of a TextModel in a readable manner
        """
        
        representation = 'Amount of words:\n' + str(self.words) + '\n\n'
        representation += 'Length of words:\n' + str(self.word_lengths) + '\n\n'
        representation += 'stems:\n' + str(self.stems) + '\n\n'
        representation += 'Sentence lengths:\n' + str(self.sentence_lengths) + '\n\n'
        representation += 'punctuations:\n' + str(self.punctuations)
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
        with open(filename, encoding='utf-8', errors='ignore') as input_file:

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
            Gets the length of each sentence and assigns it to self.sentence_lengths
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
            Makes given string lowercase and removes and punctuations before returning it.
        """
        
        # Making word lowercase and using translate to remove any punctuation.
        return s.lower().translate(str.maketrans('', '', string.punctuation))

    def get_all_words(self):
        """
            Will return all words stored in self.text as a list.
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

    def make_punctuations(self):
        """
            Fills the self.punctuations dictionary with the punctuations used throughout the text.
        """

        result = {}

        # Looping through every char in the text
        for char in self.text:

            # If current char is punctuation we add or increment it in our result dict
            if char in string.punctuation:

                result = self.increment_or_create(result, char)

        self.punctuations = result

    def normalize_dictionary(self, d):
        """
            Normalizes the values of a given dictionary.
        """

        normalized_dictionary = {}
        
        # Getting the total
        total = sum(d.values())

        # looping over each kv entry
        for key, value in d.items():
            
            # Getting the new normalised value
            normalized_value = 1 / total * value

            # Adding it to the normalised dictionary
            normalized_dictionary[key] = normalized_value

        return normalized_dictionary

    def smallest_value(self, nd1, nd2):
        """
            Returns the smallest number positive value found in the combined data of both dictionaries.
        """

        # 1. Merging the values of boths dicts in to a generator using the merge function.
        # 2. Converting the generator to a list using list comprehension.
        # 3. Returning the lowest values of this just created list.
        return min([value for value in merge(nd1.values(), nd2.values())])

    def get_dictionary_log_probability(self, d, nd, epsilon):
        """
            returns the log probability of d in nd
        """

        total = 0.0 

        # Looping through each key value pair in d
        for key, value in d.items():
            
            # If char (key) is found in the normalized items we use that value to calculate how much we add to the total
            if key in nd.keys():
                
                total += value * math.log2(nd.get(key))

            # If not we increase the total by the value of epsilon
            else:

                total += value * math.log2(epsilon)

        return total

    def compare_dictionaries(self, d, nd1, nd2):
        """
            Input requirements:
            args nd1, nd2: must be normalised
            arg d: must NOT be normalised
        """

        # Getting our epsilon value
        epsilon = self.smallest_value(nd1, nd2) / 2

        # Returning a list containing the probability of for both normalized dictionaries
        return [self.get_dictionary_log_probability(d, nd1, epsilon), self.get_dictionary_log_probability(d, nd2, epsilon)]

    def create_all_dictionaries(self):
        """
            Creates and assigns all dictionaries.
        """

        self.make_sentence_lengths()
        self.make_word_lengths()
        self.make_words()
        self.make_stems()
        self.make_punctuations()

    def all_properties_have_been_created(self, model): 
        """
            Checks if the .create_all_dictionaries() has been called.
        """

        # We can just check if model.words has any entries.
        return len(model.words) > 0

    def round_result_lists(self, result_list):
        """
            Rounds a list containing one or more float's
        """

        return [round(num, 2) for num in result_list]

    def get_points_for_property(self, property):
        """
            Takes a list for arg property containing 2 result numbers.
            Will return amount of gained points for each in the same order as a list.
        """

        # Draw == both get 1 point
        if property[0] == property[1]:
            return [1, 1]

        # model 2 property < model 1 property == model1 gets a point, model2 does not
        if property[0] < property[1]:
            return [0, 1]

        # if its the otherway around model 2 gets a point and model1 does not.
        else:
            return [1, 0]

    def get_comparison_result(self, comparison_result_dto):
        """
            Compares the results of the comparison and returns a total of how many points each model won (properties in which they had the lowest value)
        """

        model1_points = 0
        model2_points = 0

        # Getting the points for both mdoels for each property
        results = [
            self.get_points_for_property(comparison_result_dto.words),
            self.get_points_for_property(comparison_result_dto.word_lengths),
            self.get_points_for_property(comparison_result_dto.sentence_lengths),
            self.get_points_for_property(comparison_result_dto.stems),
            self.get_points_for_property(comparison_result_dto.punctuations)]

        for result in results:

            # Assigning model 1 and 2 points to the total for each.
            model1_points += result[0]
            model2_points += result[1]

        # returning the result
        return {"model1": model1_points, "model2": model2_points}

    def print_comparison_result(self, comparison_result_dto, comparison_result):
        """
            Prints the comparison results to the console
        """

        print("\nComparison results:\n\n")

        # Using tabulate to nicely format the output
        print(
            tabulate(
            [
                ["words", comparison_result_dto.words[0], comparison_result_dto.words[1]],
                ["word_lengths", comparison_result_dto.word_lengths[0], comparison_result_dto.word_lengths[1]],
                ["sentence_lengths", comparison_result_dto.sentence_lengths[0], comparison_result_dto.sentence_lengths[1]],
                ["stems", comparison_result_dto.stems[0], comparison_result_dto.stems[1]],
                ["punctuation", comparison_result_dto.punctuations[0], comparison_result_dto.punctuations[1]]
            ], 
            headers=["Property", "Model 1", "Model 2"]))

        model1_result = comparison_result["model1"]
        model2_result = comparison_result["model2"]
        print("\n--> Model 1 wins on {} features".format(model1_result))
        print("--> Model 2 wins on {} features\n".format(model2_result))

        if model1_result == model2_result:
            print("+++++\t\tModel 1 and model 2 both match up evenly\t\t+++++")
        
        elif model2_result > model1_result:
            print("+++++\t\tModel 2 is the best match out of the two\t\t+++++")
        
        else:
            print("+++++\t\tModel 1 is the best match out of the two\t\t+++++")

    def compare_text_with_two_models(self, model1, model2):
        """
            Compares the properties of this object (self) with the coresponding properties in model1 and model2
        """

        # checking if dictionaries have been created for each model, if not creating it.
        if not self.all_properties_have_been_created(self):
            self.create_all_dictionaries()

        if not self.all_properties_have_been_created(model1):
            model1.create_all_dictionaries()

        if not self.all_properties_have_been_created(model1):
            model2.create_all_dictionaries()

        # Creating a data transfer object for the result data and filling it.
        comparison_result_dto = ModelComparisonResultDto(

            # filling comparison_result_dto.words
            self.round_result_lists(
                self.compare_dictionaries(
                    self.words, 
                    self.normalize_dictionary(model1.words), 
                    self.normalize_dictionary(model2.words))),

            # filling comparison_result_dto.word_lengths
            self.round_result_lists(
                self.compare_dictionaries(
                    self.word_lengths, 
                    self.normalize_dictionary(model1.word_lengths), 
                    self.normalize_dictionary(model2.word_lengths))),

            # filling comparison_result_dto.sentence_lengths
            self.round_result_lists(
                self.compare_dictionaries(
                    self.sentence_lengths, 
                    self.normalize_dictionary(model1.sentence_lengths), 
                    self.normalize_dictionary(model2.sentence_lengths))),

            # filling comparison_result_dto.stems
            self.round_result_lists(
                self.compare_dictionaries(
                    self.stems, 
                    self.normalize_dictionary(model1.stems), 
                    self.normalize_dictionary(model2.stems))),

            # filling comparison_result_dto.punctuations
            self.round_result_lists(
                self.compare_dictionaries(
                    self.punctuations, 
                    self.normalize_dictionary(model1.punctuations), 
                    self.normalize_dictionary(model2.punctuations)))
        )

        # Getting and finally printing the results of our findings.
        comparison_result = self.get_comparison_result(comparison_result_dto)
        self.print_comparison_result(comparison_result_dto, comparison_result)

# Would normally have done this (and some other stuff as well)
class ModelComparisonResultDto():
    
    def __init__(self):

        self.words = {}
        self.word_lengths = {}
        self.sentence_lengths = {}
        self.stems = {}
        self.punctuations = {}
    
    # overloaded constructor for ease of creation
    def __init__(self, words, word_lengths, sentence_lengths, stems, punctuations):

        self.words = words
        self.word_lengths = word_lengths
        self.sentence_lengths = sentence_lengths
        self.stems = stems
        self.punctuations = punctuations


# ----------------- MAIN TEST ---------------------

print(' +++++++++++ Model 1 +++++++++++ ')
tm1 = TextModel()
tm1.read_text_from_file('model1training.txt')
tm1.create_all_dictionaries()
print(tm1)

print(' +++++++++++ Model 2 +++++++++++ ')
tm2 = TextModel()
tm2.read_text_from_file('model2training.txt')
tm2.create_all_dictionaries() 
print(tm2)

print(' +++++++++++ Onbekende tekst +++++++++++ ')
tm_unknown = TextModel()
tm_unknown.read_text_from_file('testingtext.txt')
tm_unknown.create_all_dictionaries()
print(tm_unknown)

tm = TextModel()
tm_unknown.compare_text_with_two_models(tm1, tm2)

# ----------------- ---------- ---------------------

# From here on it is just a range of tests
d = {'a': 2, 'b': 1, 'c': 1, 'd': 1, 'e': 1}
d1 = {'a': 5, 'b': 1, 'c': 2}
d2 = {'a': 15, 'd': 1}

nd1 = tm.normalize_dictionary(d1)
nd2 = tm.normalize_dictionary(d2)

assert nd1 == {'a': 0.625, 'b': 0.125, 'c': 0.25}
assert nd2 == {'a': 0.9375, 'd': 0.0625}

list_of_log_probs = tm.compare_dictionaries(d, nd1, nd2)

assert list_of_log_probs[0] == -16.356143810225277
assert list_of_log_probs[1] == -19.18621880878296

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

assert tm.smallest_value({'a': 0.625, 'b': 0.125, 'c': 0.25}, {'a': 0.9375, 'd': 0.0625}) == 0.0625

d1 = {'a': 5, 'b': 1, 'c': 2}
d2 = {'a': 15, 'd': 1}

nd1 = tm.normalize_dictionary(d1)
nd2 = tm.normalize_dictionary(d2)

assert nd1 == {'a': 0.625, 'b': 0.125, 'c': 0.25}
assert nd2 == {'a': 0.9375, 'd': 0.0625}

assert tm.smallest_value(nd1, nd2) == 0.0625