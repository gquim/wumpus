import pandas as pd

def save_score(name, time):
    data = {"Nombre": [name], "Tiempo": [time]}
    try:
        df = pd.read_csv("scores.csv")
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame(data)
    df.to_csv("scores.csv", index=False)
    print("partida guardada")

def load_scores():
    try:
        return pd.read_csv("scores.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Nombre", "Tiempo"])
