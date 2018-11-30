#! /usr/bin/python3

### REQUIRES python 3 !!!!

## Run:  ./sample.py
## Reads from stdin and writes to stdout
## For example:
##     ./sample.py <test.txt >test_out.txt

import pyfreeling
import traceback
import sys, os
import conll2tree
import generaroraciones
from spacy_test import cluster_and_labeling
from subprocess import Popen, PIPE
import nltk
from nltk.tokenize import sent_tokenize
from random import shuffle

ruta_archivos = sys.argv[1]

# def get_id_range(ptree):
#     node = ptree.begin()
#     info = node.get_info()

#     min_range = 5000000
#     max_range = -1

#     num_children = node.num_children()
#     if num_children == 0:
#         return (info.get_word().get_position()+1,info.get_word().get_position()+1)
#     else:
#         for i in range(num_children):
#             child_range = get_id_range(node.nth_child_ref(i))
#             min_range = min(min_range,child_range[0])
#             max_range = max(max_range,child_range[1])
#         return (min_range,max_range)
def get_id_range(ptree):
    node = ptree.begin()
    info = node.get_info()

    num_children = node.num_children()
    if num_children == 0:
        return [info.get_word().get_position()+1] if info.get_word().get_tag()[0] == 'N' else []
    else:
        res = []
        for i in range(num_children):
            res += get_id_range(node.nth_child_ref(i))
        return res



def get_sn_id_range_list(ptree):
    node = ptree.begin()
    info = node.get_info()
    
    res = []

    if info.get_label() == 'sn':
        res.append([get_id_range(node),False])
    else:
        for i in range(node.num_children()):
            res += get_sn_id_range_list(node.nth_child_ref(i))
    return res

def sn_root_list(dep_tree,sn_id_range_list):
    res = []
    for node in dep_tree.children:
        for id_range in [elem for elem in sn_id_range_list if not elem[1]]:
            if node[1].id in id_range[0]:
                id_range[1] = True
                res.append(node[1])
                break
        res += sn_root_list(node[1],sn_id_range_list)
    return res

def get_sn_root_list(ptree,dep_tree):
    return sn_root_list(dep_tree,get_sn_id_range_list(ptree))


def printTree(ptree, depth):

    node = ptree.begin();

    print(''.rjust(depth*2),end='');
    info = node.get_info();
    if (info.is_head()): print('+',end='');

    nch = node.num_children();
    if (nch == 0) :
        w = info.get_word();
        print ('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()),end='');

    else :
        print('{0}_['.format(info.get_label()));

        for i in range(nch) :
            child = node.nth_child_ref(i);
            printTree(child, depth+1);

        print(''.rjust(depth*2),end='');
        print(']',end='');
        
    print('');

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

argOE_script='/home/pablo/repos/Linguakit/linguakit'

## Check whether we know where to find FreeLing data files
if "FREELINGDIR" not in os.environ :
   if sys.platform == "win32" or sys.platform == "win64" : os.environ["FREELINGDIR"] = "C:\\Program Files"
   else : os.environ["FREELINGDIR"] = "/usr/local"
   print("FREELINGDIR environment variable not defined, trying ", os.environ["FREELINGDIR"], file=sys.stderr)

if not os.path.exists(os.environ["FREELINGDIR"]+"/share/freeling") :
   print("Folder",os.environ["FREELINGDIR"]+"/share/freeling",
         "not found.\nPlease set FREELINGDIR environment variable to FreeLing installation directory",
         file=sys.stderr)
   sys.exit(1)


# Location of FreeLing configuration files.
DATA = os.environ["FREELINGDIR"]+"/share/freeling/";

# Init locales
pyfreeling.util_init_locale("default");

# create language detector. Used just to show it. Results are printed
# but ignored (after, it is assumed language is LANG)
la=pyfreeling.lang_ident(DATA+"common/lang_ident/ident-few.dat");

# create options set for maco analyzer. Default values are Ok, except for data files.
LANG="es";
op= pyfreeling.maco_options(LANG);
op.set_data_files( "", 
                   DATA + "common/punct.dat",
                   DATA + LANG + "/dicc.src",
                   DATA + LANG + "/afixos.dat",
                   "",
                   DATA + LANG + "/locucions.dat", 
                   DATA + LANG + "/np.dat",
                   DATA + LANG + "/quantities.dat",
                   DATA + LANG + "/probabilitats.dat");

# create analyzers
tk=pyfreeling.tokenizer(DATA+LANG+"/tokenizer.dat");
sp=pyfreeling.splitter(DATA+LANG+"/splitter.dat");
sid=sp.open_session();
mf=pyfreeling.maco(op);

# activate mmorpho odules to be used in next call
mf.set_active_options (False,  # UserMap 
                          True,  # NumbersDetection,  
                          True,  # PunctuationDetection,   
                          True,  # DatesDetection,    
                          True,  # DictionarySearch,  
                          True,  # AffixAnalysis,  
                          False, # CompoundAnalysis, 
                          True,  # RetokContractions,
                          True,  # MultiwordsDetection,  
                          True,  # NERecognition,     
                          True, # QuantitiesDetection,  
                          True); # ProbabilityAssignment  

# create tagger, sense anotator, and parsers
tg=pyfreeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2);
sen=pyfreeling.senses(DATA+LANG+"/senses.dat");
wsd = pyfreeling.ukb(DATA+LANG+"/ukb.dat");
chunker= pyfreeling.chart_parser(DATA+LANG+"/chunker/grammar-chunk.dat")
dep=pyfreeling.dep_txala(DATA+LANG+"/dep_txala/dependences.dat", chunker.get_start_symbol())
parser = pyfreeling.dep_lstm(DATA+LANG+"/dep_lstm/params-es.dat")

resultado = []
for filepath in os.listdir(ruta_archivos):
    print(filepath)
    file = os.path.join(ruta_archivos, filepath)

    #process = Popen([argOE_script, 'rel', 'es', file], stdout=PIPE)
    #(output, err) = process.communicate()
    #exit_code = process.wait()
    #print(output.decode('utf-8'))

    content = open(file, 'r').read()
    for sentence in sent_tokenize(content):    
        l = tk.tokenize(sentence)
        ls = sp.split(l)
        ls = mf.analyze(ls)
        ls = tg.analyze(ls)
        ls = sen.analyze(ls)
        ls = wsd.analyze(ls)
        ls = chunker.analyze(ls)
        ls = parser.analyze(ls)
        
        out = pyfreeling.output_conll()
        res = out.PrintResults(ls)
        #print(res)
        conll_sentences = res.split('\n\n')
        conll_sentences.pop()
        contador = 0
        contador_corre = 0

        for idx,s in enumerate(ls):
            try:
                #print(conll_sentences[idx])
                dep_tree = conll2tree.conll2tree(conll_sentences[idx]).children[0][1]

                #printTree(s.get_parse_tree(),2)

                sn_root_list_1 = get_sn_root_list(s.get_parse_tree(),dep_tree)

                #print(sentence)
                #print(sn_root_list_1)
                list_ev = generaroraciones.main(dep_tree,sn_root_list_1)
                for ev in list_ev:
                    ev.true_label = filepath
                resultado += list_ev
                contador_corre += 1
            except:
                pass
# shuffle(resultado)        
print("CANTIDAD TOTAL DE EVENTOS: " + str(len(resultado)))
cluster_and_labeling(resultado)

    
# clean up       
sp.close_session(sid);
    
