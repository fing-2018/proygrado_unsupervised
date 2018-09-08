package freeling;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

import edu.upc.Jfreeling.ChartParser;
import edu.upc.Jfreeling.DepTree;
import edu.upc.Jfreeling.DepTxala;
import edu.upc.Jfreeling.HmmTagger;
import edu.upc.Jfreeling.LangIdent;
import edu.upc.Jfreeling.ListSentence;
import edu.upc.Jfreeling.ListSentenceIterator;
import edu.upc.Jfreeling.ListWord;
import edu.upc.Jfreeling.ListWordIterator;
import edu.upc.Jfreeling.Maco;
import edu.upc.Jfreeling.MacoOptions;
import edu.upc.Jfreeling.Nec;
import edu.upc.Jfreeling.ParseTree;
import edu.upc.Jfreeling.SWIGTYPE_p_splitter_status;
import edu.upc.Jfreeling.Senses;
import edu.upc.Jfreeling.Sentence;
import edu.upc.Jfreeling.Splitter;
import edu.upc.Jfreeling.Tokenizer;
import edu.upc.Jfreeling.Ukb;
import edu.upc.Jfreeling.Util;
import edu.upc.Jfreeling.Word;

public class Analyzer {

	// private static final String OS =
	// System.getProperty("os.name").toLowerCase();

	public static void main(String args[]) throws IOException {
		// connect to FreeLing library
		System.loadLibrary("Jfreeling");

		// Check whether we know where to find FreeLing data files
		String FLDIR = System.getenv("FREELINGDIR");
		FLDIR = "/home/pablo/proygrado/freeling";
		// if (FLDIR == null) {
		// if (OS.indexOf("win") >= 0) {
		// FLDIR = "C:\\Program Files";
		// } else {
		// FLDIR = "/usr/local";
		// }
		// System.err.println("FREELINGDIR environment variable not defined,
		// trying " + FLDIR);
		// }

		final File f = new File(FLDIR + "/share/freeling");
		if (!f.exists()) {
			System.err.println("Folder " + FLDIR + "/share/freeling not found.");
			System.err.println(
			        "Please set FREELINGDIR environment variable to FreeLing installation directory");
			System.exit(1);
		}

		// Location of FreeLing configuration files.
		final String DATA = FLDIR + "/share/freeling/";

		// Init locales
		Util.initLocale("default");

		// Create options set for maco analyzer.
		final String LANG = "es";
		final MacoOptions op = new MacoOptions(LANG);

		op.setDataFiles("", DATA + "common/punct.dat", DATA + LANG + "/dicc.src",
		        DATA + LANG + "/afixos.dat", "", DATA + LANG + "/locucions.dat",
		        DATA + LANG + "/np.dat", DATA + LANG + "/quantities.dat",
		        DATA + LANG + "/probabilitats.dat");

		// Create analyzers.

		// language detector. Used just to show it. Results are printed
		// but ignored (after, it is assumed language is LANG)
		final LangIdent lgid = new LangIdent(DATA + "/common/lang_ident/ident-few.dat");

		final Tokenizer tk = new Tokenizer(DATA + LANG + "/tokenizer.dat");
		final Splitter sp = new Splitter(DATA + LANG + "/splitter.dat");
		final SWIGTYPE_p_splitter_status sid = sp.openSession();

		final Maco mf = new Maco(op);
		mf.setActiveOptions(false, true, true, true, // select which among
		                                             // created
		        true, true, false, true, // submodules are to be used.
		        true, true, true, true); // default: all created submodules
		                                 // are used

		final HmmTagger tg = new HmmTagger(DATA + LANG + "/tagger.dat", true, 2);
		final ChartParser parser = new ChartParser(DATA + LANG + "/chunker/grammar-chunk.dat");
		final DepTxala dep = new DepTxala(DATA + LANG + "/dep_txala/dependences.dat",
		        parser.getStartSymbol());
		final Nec neclass = new Nec(DATA + LANG + "/nerc/nec/nec-ab-poor1.dat");

		final Senses sen = new Senses(DATA + LANG + "/senses.dat"); // sense
		                                                            // dictionary
		final Ukb dis = new Ukb(DATA + LANG + "/ukb.dat"); // sense
		                                                   // disambiguator

		// Make sure the encoding matches your input text (utf-8, iso-8859-15,
		// ...)
		final BufferedReader input = new BufferedReader(new InputStreamReader(System.in, "utf-8"));
		String line = input.readLine();

		// Identify language of the text.
		// Note that this will identify the language, but will NOT adapt
		// the analyzers to the detected language. All the processing
		// in the loop below is done by modules for LANG (set to "es" at
		// the beggining of this class) created above.
		final String lg = lgid.identifyLanguage(line);
		System.out.println("-------- LANG_IDENT results -----------");
		System.out.println("Language detected (from first line in text): " + lg);

		while (line != null) {
			// Extract the tokens from the line of text.
			final ListWord l = tk.tokenize(line);

			// Split the tokens into distinct sentences.
			final ListSentence ls = sp.split(sid, l, false);

			// Perform morphological analysis
			mf.analyze(ls);

			// Perform part-of-speech tagging.
			tg.analyze(ls);

			// Perform named entity (NE) classificiation.
			neclass.analyze(ls);

			sen.analyze(ls);
			dis.analyze(ls);
			printResults(ls, "tagged");

			// Chunk parser
			parser.analyze(ls);
			printResults(ls, "parsed");

			// Dependency parser
			dep.analyze(ls);
			printResults(ls, "dep");

			line = input.readLine();
		}

		sp.closeSession(sid);
	}

	private static void printSenses(Word w) {
		final String ss = w.getSensesString();

		// The senses for a FreeLing word are a list of
		// pair<string,double> (sense and page rank). From java, we
		// have to get them as a string with format
		// sense:rank/sense:rank/sense:rank
		// which will have to be splitted to obtain the info.
		//
		// Here, we just output it:
		System.out.print(" " + ss);
	}

	private static void printResults(ListSentence ls, String format) {

		if (format == "parsed") {
			System.out.println("-------- CHUNKER results -----------");

			final ListSentenceIterator sIt = new ListSentenceIterator(ls);
			while (sIt.hasNext()) {
				final Sentence s = sIt.next();
				final ParseTree tree = s.getParseTree();
				printParseTree(0, tree);
			}
		} else if (format == "dep") {
			System.out.println("-------- DEPENDENCY PARSER results -----------");

			final ListSentenceIterator sIt = new ListSentenceIterator(ls);
			while (sIt.hasNext()) {
				final Sentence s = sIt.next();
				final DepTree tree = s.getDepTree();
				printDepTree(0, tree);
			}
		} else {
			System.out.println("-------- TAGGER results -----------");

			// get the analyzed words out of ls.
			final ListSentenceIterator sIt = new ListSentenceIterator(ls);
			while (sIt.hasNext()) {
				final Sentence s = sIt.next();
				final ListWordIterator wIt = new ListWordIterator(s);
				while (wIt.hasNext()) {
					final Word w = wIt.next();

					System.out.print(w.getForm() + " " + w.getLemma() + " " + w.getTag());
					printSenses(w);
					System.out.println();
				}

				System.out.println();
			}
		}
	}

	private static void printParseTree(int depth, ParseTree tr) {
		Word w;
		long nch;

		// Indentation
		for (int i = 0; i < depth; i++) {
			System.out.print("  ");
		}

		nch = tr.numChildren();

		if (nch == 0) {
			// The node represents a leaf
			if (tr.begin().getInformation().isHead()) {
				System.out.print("+");
			}
			w = tr.begin().getInformation().getWord();
			System.out.print("(" + w.getForm() + " " + w.getLemma() + " " + w.getTag());
			printSenses(w);
			System.out.println(")");
		} else {
			// The node is non-terminal
			if (tr.begin().getInformation().isHead()) {
				System.out.print("+");
			}

			System.out.println(tr.begin().getInformation().getLabel() + "_[");

			for (int i = 0; i < nch; i++) {
				final ParseTree child = tr.nthChildRef(i);

				if (!child.empty()) {
					printParseTree(depth + 1, child);
				} else {
					System.err.println("ERROR: Unexpected NULL child.");
				}
			}

			for (int i = 0; i < depth; i++) {
				System.out.print("  ");
			}

			System.out.println("]");
		}
	}

	private static void printDepTree(int depth, DepTree tr) {
		DepTree child = null;
		DepTree fchild = null;
		long nch;
		int last, min;
		Boolean trob;

		for (int i = 0; i < depth; i++) {
			System.out.print("  ");
		}

		System.out.print(tr.begin().getLink().getLabel() + "/" + tr.begin().getLabel() + "/");

		final Word w = tr.begin().getWord();

		System.out.print("(" + w.getForm() + " " + w.getLemma() + " " + w.getTag());
		printSenses(w);
		System.out.print(")");

		nch = tr.numChildren();

		if (nch > 0) {
			System.out.println(" [");

			for (int i = 0; i < nch; i++) {
				child = tr.nthChildRef(i);

				if (child != null) {
					if (!child.begin().isChunk()) {
						printDepTree(depth + 1, child);
					}
				} else {
					System.err.println("ERROR: Unexpected NULL child.");
				}
			}

			// Print chunks (in order)
			last = 0;
			trob = true;

			// While an unprinted chunk is found, look for the one with lower
			// chunk_ord value.
			while (trob) {
				trob = false;
				min = 9999;

				for (int i = 0; i < nch; i++) {
					child = tr.nthChildRef(i);

					if (child.begin().isChunk()) {
						if ((child.begin().getChunkOrd() > last)
						        && (child.begin().getChunkOrd() < min)) {
							min = child.begin().getChunkOrd();
							fchild = child;
							trob = true;
						}
					}
				}
				if (trob && (child != null)) {
					printDepTree(depth + 1, fchild);
				}

				last = min;
			}

			for (int i = 0; i < depth; i++) {
				System.out.print("  ");
			}

			System.out.print("]");
		}

		System.out.println("");
	}
}
