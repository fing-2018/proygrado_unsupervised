ADVERB="R"
PREP="S"
CPRED="cpred"
ADJETIVE="A"

from ancora_enum import SRL

class VerbTransitivity:

	def __init__(self):
		self.dicc=self.create_dicctionary()
	
	def create_dicctionary(self):
		
		dicc={}
		dicc_gral={}
		dicc[SRL.SUBJ]=None
		diccAux = dicc.copy()
		dicc_gral["B22"]=diccAux
		dicc_gral["D11"]=diccAux
		dicc_gral["D21"]=diccAux
		dicc_gral["D31"]=diccAux
	
		dicc[SRL.OBJ]=None
		diccAux = dicc.copy()
		dicc_gral["A11"]=diccAux 
		dicc_gral["A13"]=diccAux 
		dicc_gral["A21"]=diccAux 
		
		dicc[SRL.THIRD]=[PREP]
		diccAux = dicc.copy()
		dicc_gral["A31"]=dict(diccAux)
		dicc_gral["A32"]=diccAux
		dicc_gral["A34"]=diccAux
		dicc_gral["A35"]=diccAux
		
		diccAux = dicc.copy()
		diccAux[SRL.THIRD] = [PREP,ADVERB]
		dicc_gral["B12"]=diccAux
		
		diccAux = dicc.copy()
		diccAux[SRL.THIRD]=None
		dicc_gral["A12"]=diccAux
		
		dicc[SRL.THIRD]=""
		diccAux = dicc.copy()
		diccAux[SRL.OBJ]=[PREP]
		dicc_gral["B23"]=diccAux
		dicc_gral["C42"]=diccAux
		dicc_gral["C41"]=diccAux
		dicc_gral["A22"]=diccAux
		dicc_gral["A23"]=diccAux
		
		diccAux = dicc.copy()
		diccAux[SRL.OBJ] = [PREP,ADVERB]
		dicc_gral["B11"]=diccAux
		dicc_gral["C31"]=diccAux
		
		diccAux = dicc.copy()
		diccAux[SRL.OBJ] = [PREP,ADVERB,CPRED]
		dicc_gral["B21"]=diccAux
		dicc_gral["C11"]=diccAux
		
		diccAux = dicc.copy()
		diccAux[SRL.OBJ]=[PREP]
		diccAux[SRL.THIRD]=[PREP,ADVERB]
		dicc_gral["A33"]=diccAux
		
		dicc[SRL.OBJ] = [ADJETIVE]
		dicc[SRL.THIRD]=""
		diccAux = dicc.copy()
		dicc_gral["C21"]=diccAux
		return dicc_gral
	
	def has_category_argument(self,category,srl):
		cat = category[0:3]
		print("cat: "+cat)
		try:
			print("srl: "+str(srl))
			return self.dicc[cat][srl] != ""
		except KeyError:
			return False
			
	def check_category_argument_rule(self, category, srl, pos_srl):
		cat = category[0:3]
		print("pos_srl: "+pos_srl)
		try:
			srl_options=self.dicc[cat][srl]
			return self.dicc[cat][srl] == pos_srl or self.dicc[cat][srl] == None
		except KeyError:
			return False	
