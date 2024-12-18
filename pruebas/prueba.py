#!/usr/bin/env python
#-*-coding:utf-8-*-

"""Genera fichas de domino con numeros en vez de pts"""

def genera(rang):
	for x in range(int(rang)+1):
		print ("\n*********\n")
		for z in range(int(rang)+1):
			print (" ____")
			print ("|",str(x)," |")
			print (" ____")
			print ("|",str(z)," |")
			print (" ____")
		print ("\n*********\n")
	return

def rango():
	rang=input("Determine el numero maximo en ficha: ")
	genera(rang)

rango()