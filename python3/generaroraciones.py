from node import Node
from word_embeddings import WordEmbeddings
from ancora import Ancora
from ancora_enum import SRL
from evento import Event

ancora = Ancora("ancora.vbs")
word_embeddings = WordEmbeddings()

def main(node, sn_root_list):
    events_table = {}
    event_extraction(events_table,node,None)
    sentenceList = []

    #soluciono coref
    for event in events_table.values():
        if event.subj is not None and is_pronoun(event.subj):
            event.subj = resolve_coref(event, sn_root_list,node)
    
    #aumento
    for verb_id, event in events_table.items():
        if event.subj is None and event.parent_verb is not None:
            augment_subject(events_table, verb_id, event.parent_verb.id,node)

    list_bow = [(event.bag_of_words(), event) for event in events_table.values()]
    erase_list = []
    for i, duple in enumerate(list_bow):
        for j in range(0, len(list_bow)):
            if i != j:
                if duple[0].issubset(list_bow[j][0]):
                    erase_list.append(i)
    events_list = [duple[1] for idx, duple in enumerate(list_bow) if idx not in erase_list]
    return list(filter(lambda x : x.subj is not None or x.obj is not None,events_list))
        
def event_extraction(events_table, node, parent_verb):
    if verb_not_aux(node):
        events_table[node.id] = Event(node, None, None, parent_verb)
    for child in node.children:
        node_child = child[1]
        relation_child = child[0]
        if verb_not_aux(node):
            current_event = events_table[node.id]
            if relation_child == 'suj':
                current_event.subj = node_child
            elif relation_child == 'cd':
                current_event.obj = node_child
                augment_parent_object(parent_verb, events_table, node_child)
            elif relation_child in ('cpred', 'ci', 'cc', 'creg', 'atr', 'cag'):
                check_majority_obj = ancora.check_majority_rule_category(node.form, node.lemma, SRL.OBJ, node_child.tag[0], node_child.deprel)
                if check_majority_obj and not node.has_relation('cd'):
                    if current_event.obj is None or (abs(current_event.verb.id - current_event.obj.id) > abs(current_event.verb.id - node_child.id)):
                        current_event.obj = node_child
                else:
                    check_majority = ancora.check_majority_rule_category(node.form, node.lemma, SRL.THIRD, node_child.tag[0], node_child.deprel)
                    if is_location_or_time(node_child):
                        current_event.add_circumstance_complements(node_child) 
                    elif check_majority or check_majority == None:
                        current_event.complement = node_child
                    augment_parent_complement(parent_verb, events_table, node_child)
        event_extraction(events_table,node_child,node if node.tag[0] == 'V' else parent_verb) 

def augment_parent_complement(parent_verb, events_table, node_child):
    if parent_verb is not None:
        parent_event = events_table[parent_verb.id]
        if parent_event.complement == None:
            check_unanimity_complement = ancora.check_unanimity_categories_argument_rule(parent_verb.form, parent_verb.lemma, SRL.THIRD, node_child.tag[0], node_child.deprel)
            if check_unanimity_complement:
                parent_event.complement = node_child

def augment_parent_object(parent_verb, events_table, node_child):
    if parent_verb is not None and verb_not_gerunde_nor_participle(parent_verb):
        parent_event = events_table[parent_verb.id]
        if parent_event.obj is None:
            unanimity_valence_obj = ancora.unanimity_argument(parent_verb.form, parent_verb.lemma, SRL.OBJ)
            if unanimity_valence_obj:
                parent_event.obj = node_child
            elif unanimity_valence_obj == None or (unanimity_valence_obj == False and ancora.one_category_argument(parent_verb.form, parent_verb.lemma, SRL.OBJ)):
                if word_embeddings.similar_words(parent_verb.form, node_child.form, THRESHOLD=0.65):
                    parent_event.obj = node_child  

def augment_subject(events_table, events_table_id, father_id, dep_tree):
    if father_id != 0:
        if events_table[father_id].subj == None:
            if events_table[father_id].parent_verb != None:
                augment_subject(events_table, events_table_id, events_table[father_id].parent_verb.id,dep_tree)
        else:
            parent_event = events_table[father_id]
            current_event = events_table[events_table_id]
            if check_concoord(current_event.verb,parent_event.subj, dep_tree):
                # if current_event.obj is not None:
                if (is_verb(current_event.obj) and check_concoord(current_event.obj,parent_event.subj, dep_tree)) or not is_verb(current_event.obj):
                    current_event.subj = parent_event.subj
            if  current_event.subj is None and events_table[father_id].parent_verb != None:
                augment_subject(events_table, events_table_id, events_table[father_id].parent_verb.id,dep_tree)        


def get_parent_verb(root,sn_id,parent_verb):
    for node_child in root.children:
        if node_child[1].id == sn_id:
            return parent_verb if parent_verb.tag[0] == 'V' else None
        else:
            res = get_parent_verb(node_child[1],sn_id,root if root.tag[0] == 'V' else parent_verb)
            if res is not None:
                return res
    return None

def get_det(node):
    return node.get_node_with_relation('spec')

def get_features(det,noun,verb):
    # 0: per, 1: gen, 2: num
    res = [None,None,None]


    if verb is not None and is_verb(verb):
        for node_child in verb.children:
            if node_child[0] == 'v':
                res[0] = verb_per = (node_child[1].tag[4] if node_child[1].tag[4] != '0' else res[0])
                res[2] = verb_num = (node_child[1].tag[5] if node_child[1].tag[5] != '0' else res[2])
                res[1] = verb_gen = (node_child[1].tag[6] if node_child[1].tag[6] not in ['0','C'] else res[1])
        res[0] = verb_per = (verb.tag[4] if verb.tag[4] != '0' else res[0])
        res[2] = verb_num = (verb.tag[5] if verb.tag[5] != '0' else res[2])
        res[1] = verb_gen = (verb.tag[6] if verb.tag[6] not in ['0','C'] else res[1])

    if noun is not None and is_noun(noun):
        res[1] = noun_gen = (noun.tag[2] if noun.tag[2] not in ['0','C'] else res[1])
        res[2] = noun_num = (noun.tag[3] if noun.tag[3] not in ['0','N'] else res[2])

    if det is not None and is_det(det):
        res[0] = det_per = (det.tag[2] if det.tag[2] != '0' else res[0])
        res[1] = det_gen = (det.tag[3] if det.tag[3] not in ['0','C'] else res[1])
        res[2] = det_num = (det.tag[4] if det.tag[4] not in ['0','N'] else res[2])
        
    return res

def check_concoord(verb,node_1,dep_tree):    
    det_1  = get_det(node_1)
    noun_1 = node_1
    verb_1 = get_parent_verb(dep_tree,node_1.id,node_1)
    
    rasgos_coref = get_features(None,None,verb)
    rasgos_node_1 = get_features(det_1,noun_1,verb_1)

    return len([(x,y) for (x,y) in zip(rasgos_coref,rasgos_node_1) if x is not None and y is not None and x != y]) == 0

def resolve_coref(coref_event,sn_root_list,dep_tree,PRIORITY=.2):
    #nos quedamos con los dos anteriores
    new_sn_list = list(filter(lambda x : x.id < coref_event.subj.id,sn_root_list))

    #nosquedmos con los que concueran
    concoord_list = list(filter(lambda x : check_concoord(coref_event.verb,x,dep_tree),new_sn_list))[-2:]

    #we con preferencia al mas cercano 
    if len(concoord_list) == 2:
        closest_sn = concoord_list[-1]
        second_closest_sn = concoord_list[-2]
        if coref_event.obj is not None:
            closest_sn_score = word_embeddings.similarity(coref_event.obj.form,closest_sn.form)
            second_closest_sn_score = PRIORITY+word_embeddings.similarity(coref_event.obj.form,second_closest_sn.form)
        else:
            closest_sn_score = word_embeddings.similarity(coref_event.verb.form,closest_sn.form)
            second_closest_sn_score = PRIORITY+word_embeddings.similarity(coref_event.verb.form,second_closest_sn.form)
        return max(zip(concoord_list,[closest_sn_score,second_closest_sn_score]),key=lambda x : x[1])[0]
    #si concuerda uno me quedo con ese
    elif len(concoord_list) == 1:
        return concoord_list[0]
    #si ninguno concuerdas
    else:
        pass


def is_pronoun(node):
    return node.tag[0:2] == 'PR'

def is_det(node):
    return node.tag[0] == 'D'

def is_noun(node):
    return node.tag[0] == 'N'

def is_verb(node):
    return node is not None and node.tag[0] == 'V'

def verb_not_aux(node):
    return is_verb(node) and node.deprel != 'v'

def verb_not_gerunde_nor_participle(node):
    return node.tag[2] not in ('P', 'G')

def is_location_or_time(node):
    return node.tag[0] == 'W' or node.nec == 'location'
