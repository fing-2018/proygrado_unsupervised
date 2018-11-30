#! /usr/bin/python3.5

import pyfreeling
import sys, os
import conll2tree
import generaroraciones
from subprocess import Popen, PIPE

ruta_base = sys.argv[1]

## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------
print("Se muere la acer....")

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
tg=pyfreeling.hmm_tagger(DATA+LANG+"/tagger.dat",True,2)

news_sections = ['policiales', 'sociedad', 'politica', 'economia', 'clima']

for section in news_sections:
    section_path = os.path.join(ruta_base, section)
    section_result_file = open(os.path.join(ruta_base, 'corpus_lemma_' + section + '.txt'), 'w')
    for filepath in os.listdir(section_path):
        file = os.path.join(section_path, filepath)
        print(file)
        content = open(file, 'r').read()
            
        l = tk.tokenize(content)
        ls = sp.split(l)
        ls = mf.analyze(ls)
        ls = tg.analyze(ls)
        
        for s in ls:
            noun_verb_lemmas = []
            for lemma in [w.get_lemma() for w in s if w.get_tag()[0] in ('V', 'N')]:
                noun_verb_lemmas += lemma.split('_')
            section_result_file.write(' '.join(noun_verb_lemmas))
            section_result_file.write('\n')
    section_result_file.close()
sp.close_session(sid)
