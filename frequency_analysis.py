import csv
# CSV of language data from https://en.wikipedia.org/wiki/Letter_frequency

# Class to do frequency analysis
#
# Create an instance of this class and use the @methods on a string
class FreqAnalysis:
    def __init__(self):
        self.langs = []
        self.lang_dict = {}
        self.compare_dict = {}
        self.sum_dict = {}
        self.build_lang_dict()
    
    # Part of __init__, build the lang_dict object from the CSV File
    def build_lang_dict(self):
        with open('language_freq.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            line = 0
            for row in csv_reader:
                if line == 0:
                    # Create the keys in the outer dictionary (languages)
                    for i in row:
                        if i != 'Letter':
                            lang = i.split(' ')[0]
                            self.langs.append(lang)
                            self.lang_dict[lang] = {}
                            self.sum_dict[lang] = 0.0
                else:
                    # Create a dictionary for each language key and append
                    # All the letters for each row from the CSV
                    for i,lang in enumerate(self.langs):
                        self.lang_dict[lang][row[0]] = float(row[i + 1].split('%')[0]) 
                        self.compare_dict[row[0]] = 0
                line += 1

    def get_char_freq(self, string):
        total = 0
        charfreq = {}
        for char in string.lower().replace(' ', ''):
            total += 1.0
            if char in charfreq:
                charfreq[char] += 1.0 
            else:
                charfreq[char] = 1.0
        for entry in charfreq:
            self.compare_dict[entry] = (charfreq[entry]/total) * 100
    
    # Language detection works by first creating a dictionary of the frequency
    # of each character in the input string.
    #
    # Then for each lang: for each char: abs(input_freq[char] -
    # known_freq[char])
    #
    # Then sum up all of these subtractions for each language. The lowest sum
    # will be the closest language match
    #
    # Return the best guess, as well as a dict with languages as keys, and
    # a float as a value. The closer the value is to zero, the more likely
    # it is that value
    def detect_language(self, string):
        self.get_char_freq(string)
        for lang in self.langs:
            for char in self.compare_dict:
                self.sum_dict[lang] += abs(self.compare_dict[char] -
                        self.lang_dict[lang][char])
        best_lang_guess = min(self.sum_dict.keys(), key=(lambda k:
            self.sum_dict[k]))
        return best_lang_guess, self.sum_dict
    
    # Score a string based off of a simple frequency analysis of the letters
    # that appear in the text
    #
    # @arg string to score
    # @arg lang language of the string, if unknown try fa.detect_language
    #
    # Add one to score for each letter found in both input & lang top/bot 6
    def score_string(self, string, lang):
        # First get the char frequency for this input string
        self.get_char_freq(string)
        # Get the top and bottom six most/least frequent chars from wiki
        wiki_non_zero = {x:y for x,y in self.lang_dict[lang].items() if y!=0}
        wiki_top_six = sorted(wiki_non_zero, key=wiki_non_zero.get, reverse=True)[:6]
        wiki_bot_six = sorted(wiki_non_zero, key=wiki_non_zero.get, reverse=True)[-6:]
        # Get the top and bottom six most/least frequent chars from input 
        input_non_zero = {x:y for x,y in self.compare_dict.items() if y!=0}
        input_top_six = sorted(input_non_zero, key=input_non_zero.get, reverse=True)[:6]
        input_bot_six = sorted(input_non_zero, key=input_non_zero.get, reverse=True)[-6:]
        # start score from 0
        score = 0
        for char in wiki_bot_six:
            if char in input_bot_six:
                score += 1
        for char in wiki_top_six:
            if char in input_top_six:
                score += 1
        return score
