# Github Readme Stats
Inspirado en el repositorio ![anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats)

**Github Readme Stats** es una **API** creada en **Python** utilizando **FastAPI** con la cual puedes mostrar distintos badges y estadisticas visualmente en los readme de tu github

## Funciones
### **/repos/pin**

<img width="411" height="157" alt="image" src="https://github.com/user-attachments/assets/b5e59c62-c8cb-47ad-a720-07ed93417392" />

Este endpoint permite mostrar una targeta con informacion basica de un repositorio
<br>
Argumentos que recibe el endpoint:
```
Obligatorios:
username      # nombre del usuario al que pertenece el repo
repo          # nombre del repositorio

Opcionales:
bgColor       # color del fondo de la targeta ej: bgColor=FFFFFF
color         # color del texto de la targeta
borderColor   # color del borde ej: borderColor=000000
borderWidth   # ancho del borde
borderHide    # si quieres mostrar el borde
```
Ejemplos de uso:
```
repos/pin?username=ropydev&repo=github-readme-stats&bgColor=000000&color=FFFFFF&borderColor=FFFFFF
repos/pin?username=ropydev&repo=github-readme-stats&bgColor=000000&color=FFFFFF&borderHide=True
repos/pin?username=ropydev&repo=github-readme-stats&bgColor=FFFFFF&color=606060&borderWidth=10
```

### **/stats/commits-activity**

<img width="662" height="313" alt="screenshot" src="https://github.com/user-attachments/assets/69b40e71-ef9c-4385-a040-9bc372f97f6d" />

Este endpoint permite mostrar una grafica estetica segun los ultimos 30 dias de commits del usuario
<br>
Argumentos que recibe el endpoint:
```
Obligatorios:
username      # el nombre del usuario deseado

Opcionales:
title         # el titulo a mostrar de la grafica (por defecto "Commits Activity")
```
Ejemplos de uso:
```
/stats/commits-activity?username=ropydev
/stats/commits-activity?username=ropydev&title=Example
```

## Instalacion y Uso
```
git clone https://github.com/ropydev/github-readme-stats
cd github-readme-stats
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Esos comandos de consola descargan el repositorio usando git, instala sus dependencias y abre la api en local en 
<code>http://127.0.0.1:8000/</code>
