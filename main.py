from fastapi import FastAPI

app = FastAPI()

llista_usuaris = ["Jeiron", "Junior"]

def diccionari_usuaris():
    ids = range(len(llista_usuaris))
    dicc_usuaris = dict(zip(ids, llista_usuaris))
    return dicc_usuaris

"""
    Cear:            Afegir nou usuari
    Endpoint:        /api/users
    Mètode:          POST
    Funcionalitat:   Crear un nou usuari i afegir-lo a la list de nom users.
    Return:          Retorna informació de la llista mostrant tots els registres en format diccionari.
"""
@app.post("/api/users/{nombre}", response_model=dict)
def crear_usuari(nombre):
    llista_usuaris.append(nombre)

    dicc_usuaris = diccionari_usuaris()

    return dicc_usuaris

"""
    Llegir:          Consultar un usuari
    Endpoint:        /api/users/{id}
    Mètode:          GET
    Funcionalitat:   Haurà de buscar l’usuari de la list amb l’id.
    Return:          Retorna totes les dades de l’usuari buscat en format diccionari.
"""
@app.get('/api/users/{id}', response_model=dict)
def obtener_usuari_id(id):
    id_enter = int(id)

    dicc_usuaris = diccionari_usuaris()

    if id_enter in dicc_usuaris.keys():
        return {id_enter: dicc_usuaris[id_enter]}
    return {"msg": "L'identificador de l'usuari no existeix"}

"""
    Llegir:          Consultar tots els usuaris
    Endpoint:        /api/users
    Mètode:          GET
    Funcionalitat:   Haurà de buscar tots els usuaris de la list.
    Return:          Retorna totes les dades de tots els usuaris en format diccionari.
"""
@app.get('/api/users', response_model=dict)
def mostra_usuaris():
    dicc_usuaris = diccionari_usuaris()

    return dicc_usuaris

"""
    Actualitzar:     Actualització completa
    Endpoint:        /api/users/{id}
    Mètode:          PUT
    Funcionalitat:   Actualitzar totes les dades d’un usuari de la list.
    Return:          Retorna totes les dades de l’usuari actualitzat en format diccionari. 
"""
@app.put('/api/users/{id}', response_model=dict)
def actualitzar_usuari(id, nombre):
    id_enter = int(id)
    dicc_usuaris = diccionari_usuaris()

    if id_enter in dicc_usuaris.keys():
        dicc_usuaris[id_enter] = nombre
        return dicc_usuaris
    return {"msg": "L'identificador de l'usuari no existeix"}

"""
    Eliminar:        Esborrar usuari
    Endpoint:        /api/usuaris/{id}
    Mètode:          DELETE
    Funcionalitat:   Eliminar un producte de la list.
    Return:          Retorna les tota la list d’usuaris en format diccionari.
"""
@app.delete('/api/users/{id}', response_model=dict)
def eliminar_usuari(id):
    id_enter = int(id)

    dicc_usuaris = diccionari_usuaris()

    if id_enter in dicc_usuaris.keys():
        dicc_usuaris.pop(id_enter)
        return dicc_usuaris
    return {"msg": "L'identificador de l'usuari no existeix"}