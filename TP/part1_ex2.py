# PARTIE 1 EXERCICE 2

import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


# Fonction pour quantifier le signal
def quantifier(signal, bits):
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    q = (signal_max - signal_min) / (2**bits - 1)
    return np.round((signal - signal_min) / q) * q + signal_min


# Fonction pour creer un signal modifié avec de la latence
def create_modified_signal(signal, taille_paquet, probabilite_latence, latence):
    nb = 0
    signal_paquet = np.array([])
    
    for i in range(0, len(signal), taille_paquet):
        if np.random.rand() < probabilite_latence:
            # Ajouter un nouvel élément à temps_modifies au lieu de temps
            nb += 1
            for j in range(latence):
                signal_paquet = np.append(signal_paquet, np.nan)
            signal_paquet = np.append(signal_paquet, signal[i-1])
        
        signal_paquet = np.append(signal_paquet, signal[i:i+taille_paquet])
    time_quantized = np.linspace(0, 1/frequence*len(signal_paquet) /10, len(signal_paquet))
    print("Nombre de retards :", nb)
    
    return signal_paquet, time_quantized


def plot_signal_and_modified_signal(nb_p_plot, signal, temps, modified_signal, modified_temps):
    # Tracer le signal original et le signal modifié
    periode = 1 / frequence
    plt.figure(figsize=(12, 6))
    plt.plot(temps, signal, label='Original Signal', color='blue')
    plt.plot(modified_temps, modified_signal, label='Modified Signal', color='orange')
    plt.xlabel('Temps (s)')
    plt.xlim(0, nb_p_plot * periode)  # Limiter l'axe des x à 3 périodes
    plt.ylabel('Amplitude')
    plt.title('Original and Modified Signals')
    plt.legend()
    plt.show()

def save_modified_audio(signal, fs, output_filename):
    signal = np.nan_to_num(signal)
    signal = np.int16((signal + 1) * 32767 / 2)
    write(output_filename, fs, signal)





# Paramètres de création du signal
frequence = 2000  # Hz
duree = 3  # secondes
echantillon_periode = 10
frequence_echontillonage = frequence * echantillon_periode


# Création du signal
t = np.linspace(0, duree, int(frequence_echontillonage * duree), endpoint=False)
signal = np.sin(2 * np.pi * frequence * t)


#Nombre de bits/éch.
bits = 8
signal = quantifier(signal, bits)


# Paramètres de la simulation
taille_paquet = 2  # taille du paquet en octets
probabilite_latence = 0.01  # probabilité que la latence se produise (1%)
latence = 1  # Limite le temps de latence à 1 paquet 

# Créer le signal modifié avec latence
signal_paquet, temps_modifies = create_modified_signal(signal, taille_paquet, probabilite_latence, latence)

# Tracer le signal original et le signal modifié
plot_signal_and_modified_signal(2, signal, np.arange(len(signal)) / frequence_echontillonage, signal_paquet, temps_modifies)

# Enregistrer le signal audio modifié
save_modified_audio(signal_paquet, frequence_echontillonage, 'TP\signaux\latence_signal.wav')