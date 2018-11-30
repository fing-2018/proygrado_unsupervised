from functools import reduce
from ancora_enum import SRL
from verb_transitivity import VerbTransitivity

class Ancora:
   
    def __init__(self, filename):
        self._conjugated_category = {}
        self._infinitive_category = {}
        with open(filename, 'r') as ancora_file:
            for line in ancora_file:
                line_split = line.strip().split()
                infinitive = line_split[0]
                category = line_split[1]
                conjugated = line_split[2]
                self._fill_dict(self._conjugated_category, conjugated, category)
                self._fill_dict(self._infinitive_category, infinitive, category)
    
    def unanimity_argument(self, conjugated, infinitive, srl):
        categories = self.categories(conjugated, infinitive)
        if categories != None:
            for category in categories:
                if not self.has_category_argument(category, srl):
                    return False
        return True if categories != None else None

    def one_category_argument(self, conjugated, infinitive, srl):
        categories = self.categories(conjugated, infinitive)
        if categories != None:
            for category in categories:
                if self.has_category_argument(category, srl):
                    return True
        return False

    def check_majority_rule_category(self, conjugated, infinitive, srl, pos_srl, relation):
        majority_category = self.category(conjugated, infinitive)
        if majority_category != None:
            return self.check_category_argument_rule(majority_category, srl, pos_srl, relation)
        return None 

    def check_unanimity_categories_argument_rule(self, conjugated, infinitive, srl, pos_srl, relation):
        categories = self.categories(conjugated, infinitive)
        if categories is None:
            return None
        for category in categories:
            if not self.check_category_argument_rule(category, srl, pos_srl, relation):
                return False
        return True

    def check_category_argument_rule(self, category, srl, pos_srl, relation):
        verb_transitivity = VerbTransitivity()
        return verb_transitivity.check_category_argument_rule(category, srl, pos_srl, relation)
        

    def has_category_argument(self, category, srl):
        verb_transitivity = VerbTransitivity()
        return verb_transitivity.has_category_argument(category, srl)

    def categories(self, conjugated, infinitive):
        try:
            return self._conjugated_category[conjugated] if conjugated in self._conjugated_category else self._infinitive_category[infinitive]
        except KeyError:
            return None

    def category(self, conjugated, infinitive):
        result_category = self._max_freq_category(self._conjugated_category, conjugated)
        if result_category == None:
            result_category = self._max_freq_category(self._infinitive_category, infinitive)
        return result_category

    def _max_freq_category(self, verb_category, verb):
        max_category = None
        if verb in verb_category:
            verb_categories = verb_category[verb]
            max_category = reduce(lambda x,key : x if x[1] > verb_categories[key] else (key, verb_categories[key]), verb_categories, (None,0))[0]
        return max_category
                        
    def _fill_dict(self, verb_category, verb, category): 
        if verb not in verb_category:
            verb_category[verb] = dict()
        if category not in verb_category[verb]:
            verb_category[verb][category] = 0
        verb_category[verb][category] = verb_category[verb][category] + 1

