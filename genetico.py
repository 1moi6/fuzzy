import numpy as np
import random


def genetico():
	tpop = 10  
	tcrom = 5  
	nsim = 100  
	ngens = 500
	vgen = [i for i in range(ngens)] 
	pop0 = [list(p) for p in np.random.randint(0,len(vgen),size=(tpop,tcrom))] 
	pop0[-1]=[20,20,20,20,20]

	npais = int(0.4*tpop)  
	ncros = int(0.4*tpop)  
	nmtt = int(0.2*tpop) 
	nmpc = int(0.2*tcrom)  
	ngcrs = int(0.5*tcrom)  
	unico = True

	if unico and len(vgen)<tcrom:
		unico = False

	pars = [npais, ncros ,nmtt ,nmpc , ngcrs , unico]
	#print(pars)

	fvalm = []  
	fvala = []
	for i in range(nsim):
		obj0 = objetivo(pop0) 
		pop1 = nextgen(pop0,obj0,vgen,pars) 
		obj1 = objetivo(pop1)  #print(pop1)
		#input()
		fvalm.append(np.min(obj1))
		fvala.append(np.mean(obj1))
		print([fvalm[-1],fvala[-1]])
		pop0 = pop1

	return pop0,[fvalm,fvala]


def nextgen(pop,val,vgen,pars):
	npais = pars[0]  
	ncros = pars[1] 
	nmuta = pars[2]  
	ngmut = pars[3] 
	ptcrs = pars[4]  
	unico = pars[5]

	vpop = np.array(pop)  
	vval = np.array(val)
 
	lp = len(vpop)  
	lcrm = len(vpop[0])   
	lvg = len(vgen)
	npop = [np.nan]*lp  
	cnt = 0 

	if unico and lvg<lcrm:
		raise Exception("Configuração de ngens e tcrom incompativeis")

	# selecao dos pais
	avals = np.argsort(vval)[0:npais]
	for a in avals:
		if unico:
			la = len(set(vpop[a]))
			xx = list(set(vpop[a]))+random.sample(vgen,lcrm-la) 
		else:
			xx =  vpop[a] 
		npop[cnt] = list(xx)
		cnt = cnt+1
	
	# crosover
	for i in range(ncros):
		idvs = np.random.randint(0,lp,2)
		idv1 = vpop[idvs[0]]  
		idv2 = vpop[idvs[1]] 
		### primeiro metodo de crossover 
		#idv = list(idv1[0:ptcrs])+list(idv2[ptcrs:]) 
		### segundo método de crossover
		crspts = random.sample(range(lcrm),k = ptcrs)
		idv = list(idv1)
		for pts in crspts:
			idv[pts] =  idv2[pts]
		############################
		while len(set(idv))<lcrm and unico:
			gs = np.random.randint(0,lvg,1)[0]
			idv.append(vgen[gs])
			idv = list(set(idv))
		npop[cnt] = list(idv)
		cnt = cnt + 1
	
	# mutacao
	for i in range(nmuta):
		idvs = np.random.randint(0,lp,1)[0] 
		idv = list(vpop[idvs])  #print(len(idv))
		ptm = np.random.randint(0,lcrm,size=(ngmut,))
		for pt in ptm:
			gs = np.random.randint(0,lvg,1)[0]
			idv[pt] = vgen[gs]
		while len(set(idv))<lcrm and unico:
			pt = np.random.randint(0,lcrm,1)[0]
			gs = np.random.randint(0,lvg,1)[0]
			idv.append(vgen[gs])  
			idv = list(set(idv))
		npop[cnt] = list(idv)
		cnt = cnt + 1

	return npop

def objetivo(x):
	#oba = np.array([np.sum(xa)-100 for xa in x])
	#obj = oba**2
	obj = (np.sum(x,axis=1)-100)**2
	return list(obj)
