import random

populacao = [] # (custo,individuo)
UNIDADE = 1 # L
custo_papel = 2 # moedas/L_2
ganho_estoque = 18 # moedas/L_3
numero_pop = 80 # individuos
numero_geracoes = 100

class Individuo(object):
	def __init__(self, cromo):
		super(Individuo, self).__init__()
		self.cromo = cromo
	def cruzamento(self,other):
		filho = []
		for i in range(len(self.cromo)):
			filho.append(random.choice([self.cromo[i],other.cromo[i]]))
		return Individuo(cromo=filho)
	def mutacao(self):
		i = random.randint(0,len(self.cromo)-1)
		self.cromo[i] = random.random()
	def superficie(self):
		area = 0
		for i in range(len(self.cromo)):
			area = area + self.cromo[i-1]*self.cromo[i]
		return area*2*UNIDADE**2
	def volume(self):
		volume = 1
		for i in range(len(self.cromo)):
			volume = volume * self.cromo[i]
		return volume*UNIDADE**3
	def funcaoObjetivo(self):
		'''Calculo do saldo de estocagem'''
		return self.volume()*ganho_estoque - self.superficie()*custo_papel
	def __repr__(self):
		retorno = '['
		for i in self.cromo:
			retorno = retorno + f"{round(i,3)}, "
		return retorno[:-2] + ']'
	def __lt__(self,other):
		if self.funcaoObjetivo()<other.funcaoObjetivo():
			return True
		else:
			return False

def gerarCromo(n=3):
	lista = []
	for i in range(n):
		lista.append(random.random())
	return Individuo(cromo=lista)

def selecaoNatural(pop,ind):
	pop.append((ind.funcaoObjetivo(),ind))
	pop.sort()
	excesso = len(pop) - numero_pop
	if excesso>0:
		return pop[excesso:]
	return pop

def main():
	global populacao
	for i in range(numero_pop):
		ind = gerarCromo()
		custo = ind.funcaoObjetivo()
		populacao.append((custo,ind))
	for j in range(numero_geracoes):
		evento = random.choice([2])
		if evento==0: # Cruzamento Aleatório
			a = list(range(len(populacao)))
			pai = random.choice(a)
			del a[pai]
			mae = random.choice(a)
			# Cruzamento aleatório sem nenhum critério
			filho = populacao[pai][1].cruzamento(populacao[mae][1])
			populacao = selecaoNatural(populacao,filho)
		elif evento==1: # Mutacao
			mutante = random.choice(range(len(populacao)))
			# Mutacao aleatório sem nenhum critério
			aux = populacao[mutante]
			del populacao[mutante]
			aux[1].mutacao()
			saldo = aux[1].funcaoObjetivo()
			populacao.append((saldo,aux[1]))
		else: # Cruzamento Real
			populacao.sort()
			principe = populacao[-1][1].cruzamento(populacao[-2][1])
			populacao = selecaoNatural(populacao,principe)
	return populacao

if __name__ == '__main__':
	populacao = main()
	populacao.sort()
	for i in populacao:
		print(f"{round(i[0],2)},	{i[1]}")