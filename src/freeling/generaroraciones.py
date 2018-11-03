from node import Node
from functools import reduce
from word_embeddings import WordEmbeddings
from ancora import Ancora
from ancora_enum import SRL
from evento import Event

def is_verb(node):
    return node.tag[0] == 'V'

def verb_not_aux(node):
    return is_verb(node) and node.deprel != 'v'

def verb_not_gerunde_nor_participle(node):
    return node.tag[2] not in ('P', 'G')

def is_location_or_time(node):
    return node.tag[0] == 'W' or node.nec == 'location'

def verbs_match_person_n_number(node1, node2):
    return node1.tag[4:6] == node2.tag[4:6] 

def event_extraction(events_table,node,parent_verb):
    ancora = Ancora("ancora.vbs")
    if verb_not_aux(node):
        events_table[node.id] = Event(node, None, None, parent_verb)
    for child in node.children:
        node_child = child[1]
        relation_child = child[0]
        if is_verb(node):
            current_event = events_table[node.id]
            if relation_child == 'suj':
                current_event.subj = node_child
            elif relation_child == 'cd':
                current_event.obj = node_child
                if parent_verb is not None and verb_not_gerunde_nor_participle(parent_verb):
                    parent_event = events_table[parent_verb.id]
                    if parent_event.obj is None:
                        unanimity_valence_obj = ancora.unanimity_argument(parent_verb.form, parent_verb.lemma, SRL.OBJ)
                        if unanimity_valence_obj:
                            parent_event.obj = node_child  
                        elif unanimity_arg == None or (unanimity_arg == False and ancora.one_category_argument(parent_verb.form, parent_verb.lemma, SRL.OBJ)):
                            word_embeddings = WordEmbeddings()
                            if word_embeddings.similar_words(parent_verb.form, node_child.form):
                                parent_event.obj = node_child  
            elif relation_child in ('cpred', 'ci', 'cc', 'creg'):
                check_majority = ancora.check_majority_rule_category(node.form, node.lemma, SRL.THIRD, node_child.tag[0])
                if is_location_or_time(node_child):
                    current_event.add_circumstance_complements(node_child) 
                elif check_majority or check_majority == None:
                    current_event.complement(node_child)
                if parent_verb is not None:
                    parent_event = events_table[parent_verb.id]
                    if parent_event.complement == None:
                        check_unanimity_complement = ancora.check_unanimity_categories_argument_rule(parent_verb.form, parent_verb.lemma, SRL.THIRD, node_child.tag[0])
                        if check_unanimity_complement:
                            parent_event.complement = node_child
        event_extraction(events_table,node_child,node if node.tag[0] == 'V' else parent_verb) 


def augment_subject(events_table, events_table_id, father_id):
    if father_id != 0:
        if events_table[father_id].subj == None:
            augment_subject(events_table, events_table_id, events_table[father_id].id)
        else:
            parent_event = events_table[father_id]
            current_event = events_table[events_table_id]
            if verbs_match_person_n_number(parent_event.verb, current_event.verb):
                current_event.subj = parent_event.subj


def main(node):
    events_table = {}
    event_extraction(events_table,node,None)
    sentenceList=[]
    for verb_id, event in events_table.items():
        if event.subj is None and event.parent_verb is not None:
            augment_subject(events_table, verb_id, event.parent_verb.id)
    for k, event in events_table.items():
        print("Clave: "+str(k))
        if event.subj is not None:
            print(" Suj: "+event.subj.form)
        if event.obj is not None:
            print(" Cd: "+event.obj.form)
        if event.complement is not None:
            print(" Cc: "+event.complement.form)
        if event.verb is not None:
            print(" Verb: "+event.verb.form)
        if event.circumstance_complements != []:
            print(" Circumstance Complements: "+' '.join([event.circumstance_complements.form for circum_compl in event.circumstance_complements]))
        #print(" Padre: "+event.parent_verb.form)
    return events_table.values()
