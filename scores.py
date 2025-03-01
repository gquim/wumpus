import pandas as pd

def save_score(name, time):
    data = {"Nombre": [name], "Tiempo": [time]}
    try:
        df = pd.read_csv("scores.csv")
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(data)
    df.to_csv("scores.csv", index=False)
    print("Puntuación guardada")