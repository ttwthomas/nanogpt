import os
import requests
import tiktoken
import numpy as np
import glob


def parcourir_dossiers_et_recuperer_js(chemin, fichier_sortie, dossiers_a_exclure=[]):
    fichiers_js = []
    all=""
    def parcourir_dossier_actuel(chemin_actuel):
        fichiers = os.listdir(chemin_actuel)
        #print(chemin_actuel)
        for fichier in fichiers:
            chemin_fichier = os.path.join(chemin_actuel, fichier)
            if os.path.isdir(chemin_fichier):
                if fichier not in dossiers_a_exclure:
                    parcourir_dossier_actuel(chemin_fichier)
            elif fichier.endswith('.js'):
                fichiers_js.append(chemin_fichier)

    parcourir_dossier_actuel(chemin)
    print(fichiers_js)
    with open(fichier_sortie, 'w') as sortie:
        for fichier_js in fichiers_js:
            with open(fichier_js, 'r') as fichier:
                print(fichier_js)
                contenu_js = fichier.read()
               # sortie.write(f"====== {fichier_js} ======\n")
                sortie.write(contenu_js + '\n')
                all+=contenu_js
    return all




dossiers_a_exclure = []
# download the tiny shakespeare dataset
input_file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
#if not os.path.exists(input_file_path):
    
    #parcourir_dossiers_et_recuperer_js("d:\\", input_file_path,dossiers_a_exclure)
  




    

data = parcourir_dossiers_et_recuperer_js("d:\\", input_file_path,dossiers_a_exclure)
n = len(data)
train_data = data[:int(n*0.9)]
val_data = data[int(n*0.9):]

# encode with tiktoken gpt2 bpe
enc = tiktoken.get_encoding("gpt2")
train_ids = enc.encode_ordinary(train_data)
val_ids = enc.encode_ordinary(val_data)
print(f"train has {len(train_ids):,} tokens")
print(f"val has {len(val_ids):,} tokens")

# export to bin files
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

# train.bin has 301,966 tokens
# val.bin has 36,059 tokens
