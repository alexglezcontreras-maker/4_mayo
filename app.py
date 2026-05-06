
def translate(text):
    translations = {
        "I like soccer": "Me gusta el fútbol",
        "How are you?": "¿Cómo estás?",
        "What time is it?": "¿Qué hora es?"
    }
    return translations.get(text, "Traducción no disponible")

if __name__ == "__main__":
    print("Traductor simple EN -> ES")
    while True:
        txt = input("Ingresa texto (o 'salir'): ")
        if txt.lower() == "salir":
            break
        print("→", translate(txt))
