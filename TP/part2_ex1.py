# PARTIE 1 EXERCICE 2

import numpy as np
import pyaudio
import time
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt

# Fonction pour quantifier le signal
def quantifier(signal, bits):
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    q = (signal_max - signal_min) / (2**bits - 1)
    return np.round((signal - signal_min) / q) * q + signal_min

def create_modified_signal(signal, fs, taille_paquet, probabilite_latence, latence):
    nb = 0
    signal_paquet = np.array([])
    #temps_modifies = np.arange(len(signal)) / fs  # Créez une copie de votre tableau de temps
    
    for i in range(0, len(signal), taille_paquet):
        if np.random.rand() < probabilite_latence:
            # Ajouter un nouvel élément à temps_modifies au lieu de temps
            nb += 1
            for j in range(latence):
                signal_paquet = np.append(signal_paquet, signal[i-1])
        signal_paquet = np.append(signal_paquet, signal[i:i+taille_paquet])
    time_quantized = np.linspace(0, 1/frequence*len(signal_paquet) /10, len(signal_paquet))
    print("Nombre de retards :", nb)

    return signal_paquet, time_quantized

def plot_signal_and_modified_signal(nb_p_plot, signal, temps, modified_signal, modified_temps):
    # Tracer le signal original et le signal modifié
    plt.figure(figsize=(12, 6))
    plt.plot(temps, signal, label='Signal original ', color='blue')
    plt.plot(modified_temps, modified_signal, label='Signal avec latence', color='orange')
    plt.xlabel('Temps (s)')
    plt.xlim(0, nb_p_plot * periode)  # Limiter l'axe des x à 3 périodes
    plt.ylabel('Amplitude')
    plt.title(f'Comparaison du Signal Original et du Signal avec latence ({probabilite_latence*100}%) DPCM')
    plt.legend()
    plt.show()

def save_modified_audio(signal, fs, output_filename):
    signal = np.nan_to_num(signal)
    signal = np.int16((signal + 1) * 32767 / 2)
    write(output_filename, fs, signal)

if __name__ == "__main__":


    # Paramètres de création du signal
    frequence = 2000  # fréquence de la tonalité (Hz)
    duree = 3  # durée du signal (s)
    ech_periode = 10  # échantillons par période
    fs = frequence * ech_periode  # fréquence d'échantillonnage
    
    # Création du signal
    t = np.linspace(0, duree, int(fs * duree), endpoint=False)
    signal = np.sin(2 * np.pi * frequence * t)
    
    # Convertir le signal en format audible
    signal_int16 = np.int16((signal + 1) * 32767 / 2)
    
    # Visualisation - Affichage limité à 3 périodes
    periode = 1 / frequence

    #Nombre de bits/éch.
    bits = 8
    signal = quantifier(signal, bits)

    # Paramètres de la simulation
    taille_paquet = 2  # taille du paquet en octets
    probabilite_latence = 0.1  # probabilité que la latence se produise (1%)
    latence = 1  # Limite le temps de latence à 1 paquet 
    
    # Créer le signal modifié avec latence
    signal_paquet, temps_modifies = create_modified_signal(signal, fs, taille_paquet, probabilite_latence, latence)
    
    # Tracer le signal original et le signal modifié
    plot_signal_and_modified_signal(5, signal, np.arange(len(signal)) / fs, signal_paquet, temps_modifies)
    
    # Enregistrer le signal audio modifié
    save_modified_audio(signal_paquet, fs, f'TP/signaux/dpcm_latence_signal.wav')