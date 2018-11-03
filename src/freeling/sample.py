#! /usr/bin/python3

### REQUIRES python 3 !!!!

## Run:  ./sample.py
## Reads from stdin and writes to stdout
## For example:
##     ./sample.py <test.txt >test_out.txt

import pyfreeling
import sys, os
import conll2tree
import generaroraciones
from subprocess import Popen, PIPE

ruta_archivos = sys.argv[1]

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------
print("Se muere la acer....")

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
parser = pyfreeling.dep_lstm(DATA+LANG+"/dep_lstm/params-es.dat");

for filepath in os.listdir(ruta_archivos):
    file = os.path.join(ruta_archivos, filepath)

    process = Popen([argOE_script, 'rel', 'es', file], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    print(output.decode('utf-8'))

    content = open(file, 'r').read()
        
    l = tk.tokenize(content)
    ls = sp.split(l)
    ls = mf.analyze(ls)
    ls = tg.analyze(ls)
    ls = sen.analyze(ls)
    ls = wsd.analyze(ls)
    ls = parser.analyze(ls)
    
    out = pyfreeling.output_conll()
    res = out.PrintResults(ls)
    conll_sentences = res.split('\n\n')
    conll_sentences.pop()
    for conll_sentence in conll_sentences:
        dep_tree = conll2tree.conll2tree(conll_sentence).children[0][1]
        #dep_tree.display(0)
        sentenceListArgOE=generaroraciones.main(dep_tree)
        #print(sentenceListArgOE)

    
# clean up       
sp.close_session(sid);
    
