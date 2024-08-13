import pandas as pd
import tkinter as tk
from tkinter import ttk,font
from datetime import datetime

#Backend
def visitas_anteriores(visitante,direccion):
    xfile = open(direccion,"r").readlines()
    lista = []
    for line in xfile:
        if line.split(";")[0] == visitante:
            lista.append(line.split(";")[2]+", de "+line.split(";")[3]+" a "+line.split(";")[4])
    return lista

def tomar_datos(nombre,ordenarPor): #Le pasas un archivo y te devuelve el dataframe
	dataframe = pd.read_csv(nombre , sep=";" , encoding='latin-1')
	if(ordenarPor==""):
		return dataframe
	return dataframe.sort_values(by=ordenarPor)

def buscar_ubicacion_visita_pendiente(datos,direccion): #Igual que buscar_ubicacion, pero devolviendo solo la visitas pendientes
	ubicacion = 0
	planilla = open(direccion,"r")
	data = planilla.readlines()
	for line in data:
		if line.split(";")[4] == "" and line.split(";")[0] == datos.split(";")[0]:
			print("exito")
			return ubicacion
		ubicacion += 1
	0/0

def editar(datosAGuardar,ubicacion,direccion): #Reemplaza la linea de texto pisando la ubicación del archivo original
	planilla = open(direccion,"r")
	data = planilla.readlines()
	data[ubicacion] = datosAGuardar
	planilla = open(direccion,"w")
	planilla.writelines(data)
	planilla.close()

def guardar_nuevo(datosAGuardar,direccion):
	planilla = open(direccion,"a")
	planilla.writelines(datosAGuardar)
	planilla.close()

def obtener_datos_especificos(pista,direccion):
	try:
		lista = []
		planilla = open(direccion,"r")
		data = planilla.readlines()
		shorten = pista.split(";")[0]
		for line in data:
			if line.find(shorten) != -1:
				lista.append(line)
		return lista[-1]
	except:
		print("error obtener datos")
		return("")

#Menu e interface
def arreglo_visual(menu):
	lista = [0,3,5,7,9,11,13]
	for i in lista:
		menu.rowconfigure(i,weight=0)
		tk.Label(menu).grid(column=0,row=i,sticky="ew",columnspan=7)
	tk.Label(menu, bg ="black").grid(column=0,row=0,sticky="nsew",columnspan=7,rowspan=15)

def opciones(menu):
	datos = tomar_datos(".datos/listadoDeVisitantes.csv","DNI")
	listado=[]
	for index, row in datos.iterrows():
		listado.append(row["Nombre y Apellido"])
	listado = list(set(listado))
	arreglo_visual(menu)
	tk.Label(menu,text="FECHA", bg ="grey").grid(column=2,row=4,sticky="nwes")
	tk.Label(menu,text="Hora de ingreso", bg ="grey").grid(column=4,row=3,sticky="nwes")
	tk.Label(menu,text="Hora de egreso", bg ="grey").grid(column=5,row=3,sticky="nwes")
	tk.Label(menu,text="NOMBRE Y APELLIDO", bg ="grey").grid(column=2,row=6,sticky="nwes")
	tk.Label(menu,text="DNI", bg ="grey").grid(column=2,row=8,sticky="nwes")
	tk.Label(menu,text="DEPARTAMENTO", bg ="grey").grid(column=2,row=10,sticky="nwes")
	tk.Label(menu,text="OBSERVACIONES", bg ="grey").grid(column=2,row=14,sticky="nwes")
	tk.Label(menu,text=datetime.today().strftime('%Y-%m-%d'),bg="white").grid(column=3,row=4,sticky="nwes")
	nombre = tk.StringVar()
	tk.Entry(menu,textvariable = nombre).grid(column=3,row=6,sticky="nwes",columnspan=3)
	dni = tk.StringVar()
	tk.Entry(menu,textvariable = dni).grid(column=3,row=8,sticky="nwes")
	dept = tk.StringVar()
	tk.Entry(menu,textvariable = dept).grid(column=3,row=10,sticky="nwes")
	ingr = tk.StringVar()
	ingr.set(datetime.today().strftime('%H:%M'))
	tk.Entry(menu,textvariable = ingr).grid(column=4,row=4,sticky="nwes")
	egr = tk.StringVar()
	tk.Entry(menu,textvariable = egr).grid(column=5,row=4,sticky="nwes")
	obs = tk.StringVar()
	tk.Entry(menu,textvariable = obs).grid(column=3,row=14,sticky="nwes",columnspan=3)
	
	legible = ttk.Combobox(menu,state="readonly", values=listado)
	legible.grid(column=2,row=1,sticky="nwes")
	
	tk.Button(menu, text="BUSCAR",bg ="#00ffff",command=lambda:cargar(menu,legible.get(),nombre,dni,dept,ingr,egr,obs)).grid(column=3,row=1,sticky="nwes")
	tk.Button(menu, text="GUARDAR",bg ="#00ffff",command=lambda:guardar(menu,nombre,dni,dept,ingr,egr,obs)).grid(column=5,row=10,sticky="nwes")
	tk.Button(menu, text="BORRAR",bg ="#00ffff",command=lambda:borrar(nombre,dni,dept,ingr,egr,obs)).grid(column=6,row=14,sticky="nwes")
	
def cargar(menu,dato,nm,dn,dpt,ing,egr,obs):
	datos = obtener_datos_especificos(dato,".datos/listadoDeVisitantes.csv").split(";")
	dn.set(datos[0])
	nm.set(datos[1])
	ing.set(datos[3])
	egr.set(datos[4])
	obs.set(datos[5])
	caja_de_visitas(menu,dn.get())

def caja_de_visitas(menu,dato):
	legibleV = ttk.Combobox(menu,state="readonly", values=visitas_anteriores(dato,".datos/listadoDeVisitantes.csv"))
	legibleV.grid(column=5,row=1,sticky="nwes")
	tk.Button(menu, text="Ver visitas pasadas",bg ="red").grid(column=6,row=1,sticky="nwes")

def cleaner(menu):
	for widget in menu.winfo_children():
		widget.destroy()

def borrar(nm,dn,dpt,ing,egr,obs):
	lst = [nm,dn,dpt,ing,egr,obs]
	for i in lst:
		i.set("")

def guardar(menu,nm,dn,dpt,ing,egr,obs):
	fecha = datetime.today().strftime('%Y-%m-%d')
	dni = dn.get()
	nombre = nm.get()
	ingreso = ing.get()
	egreso = egr.get()
	observacion = obs.get()
	datosAGuardar = f"{dni};{nombre};{fecha};{ingreso};{egreso};{observacion}"
	try:
		num = buscar_ubicacion_visita_pendiente(datosAGuardar,".datos/listadoDeVisitantes.csv")
		editar(datosAGuardar,num,".datos/listadoDeVisitantes.csv")
	except:
		print("error editar datos")
		if dni != "":
			guardar_nuevo(datosAGuardar, ".datos/listadoDeVisitantes.csv")
	cleaner(menu)
	opciones(menu)

def menu_visitantes(menu):
	menu.rowconfigure(0,weight=0)
	opciones(menu)

def config_col_row(menu,cols,rows):
	for i in range(cols):
		menu.columnconfigure(i, weight=1)
	for i in range(rows):
		menu.rowconfigure(i, weight=1)

#Aplicacion
class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry("600x600")
		self.title("Gestor del edificio")
		self.defaultFont = font.nametofont("TkDefaultFont")
		self.defaultFont.configure(weight=font.BOLD,size=15)        
		config_col_row(self,7,15)
		menu_visitantes(self)

if __name__ == "__main__":
	app=App()
	app.mainloop()