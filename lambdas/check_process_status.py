import json

def lambda_handler(event, context):

    #Leer informacion de DynamoDB
    #   - Obtener Stage,Status,Timestamp
    #Enviar Failed si el proceso lleva corriendo mas del tiempo permitido

    ##### SE DEBE DE TENER MAPEO DE TODOS LOS DICT QUE SE RECIBIRAN A LO LARGO DEL PROCESO
    
