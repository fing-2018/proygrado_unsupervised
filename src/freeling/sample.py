#! /usr/bin/python3

### REQUIRES python 3 !!!!

## Run:  ./sample.py
## Reads from stdin and writes to stdout
## For example:
##     ./sample.py <test.txt >test_out.txt

import pyfreeling
import sys, os

## ------------  output a parse tree ------------
def printDepTree(dtree, depth):

    node = dtree.begin()

    print(''.rjust(depth*2),end='');

    info = node.get_info();
    link = info.get_link();
    #print ('{0}/{1}/'.format(link.get_info().get_label(), info.get_label()),end='');
    print ('{0}/'.format(info.get_label()),end='');

    w = node.get_info().get_word();
    print ('({0} {1} {2})'.format(w.get_form(), w.get_lemma(), w.get_tag()),end='');

    nch = node.num_children();
    if (nch > 0) :
        print(' [');

        for i in range(nch) :
            d = node.nth_child_ref(i);
            if (not d.begin().get_info().is_chunk()) :
                printDepTree(d, depth+1);

        ch = {};
        for i in range(nch) :
            d = node.nth_child_ref(i);
            if (d.begin().get_info().is_chunk()) :
                ch[d.begin().get_info().get_chunk_ord()] = d;
 
        for i in sorted(ch.keys()) :
            printDepTree(ch[i], depth + 1);

        print(''.rjust(depth*2),end='');
        print(']',end='');

    print('');



## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

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
parser = pyfreeling.dep_treeler(DATA+LANG+"/treeler/dependences.dat");

# process input text
lin=sys.stdin.readline();

print ("Text language is: "+la.identify_language(lin)+"\n");

while (lin) :
        
    l = tk.tokenize(lin);
    ls = sp.split(l);

    ls = mf.analyze(ls);
    ls = tg.analyze(ls);
    ls = sen.analyze(ls);
    ls = wsd.analyze(ls)
    ls = parser.analyze(ls);

    ## output results
    for s in ls :
       ws = s.get_words();
       for w in ws :
          print(w.get_form()+" "+w.get_lemma()+" "+w.get_tag()+" "+w.get_senses_string());
       print ("");

       dp = s.get_dep_tree();
       printDepTree(dp, 0)

    lin=sys.stdin.readline();
    
# clean up       
sp.close_session(sid);
    
