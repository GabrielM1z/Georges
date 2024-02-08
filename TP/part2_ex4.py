# PARTIE 1 EXERCICE 2

import numpy as np
import pyaudio
import time
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from scipy.io import wavfile


# Fonction pour quantifier le signal
def quantifier(signal, bits):
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    q = (signal_max - signal_min) / (2**bits - 1)
    return np.round((signal - signal_min) / q) * q + signal_min

def create_lost_packet_signal(signal, taille_paquet, probabilite_perte):
    nb = 0
    signal_paquet = np.array([])
    #temps_modifies = np.arange(len(signal)) / fs  # Créez une copie de votre tableau de temps
    
    for i in range(0, len(signal), taille_paquet):
        if np.random.rand() < probabilite_perte:
            # Ajouter un nouvel élément à temps_modifies au lieu de temps
            nb += 1
            for j in range(0, taille_paquet):
                signal_paquet = np.append(signal_paquet, signal[i-1])
             
        else:
            signal_paquet = np.append(signal_paquet, signal[i:i+taille_paquet])
            
    time_quantized = np.linspace(0, 1/f*len(signal_paquet) /10, len(signal_paquet))
    print("Nombre de retards :", nb)
    
    return signal_paquet, time_quantized


def plot_signal_and_modified_signal(signal, temps, modified_signal, modified_temps, val):
    # Tracer le signal original et le signal modifié
    plt.figure(figsize=(12, 6))
    plt.plot(temps, signal, label='Signal original', color='blue')
    plt.plot(modified_temps, modified_signal, label='Signal avec perte', color='orange')
    plt.xlabel('Temps')
    plt.ylabel('Amplitude')
    plt.title(f'Comparaison du Signal Original xtine et du Signal avec perte ({probabilite_perte*100}%) DPCM')
    plt.legend()
    plt.show()

def save_modified_audio(signal, fs, output_filename):
    signal = np.nan_to_num(signal)
    signal = np.int16((signal + 1) * 32767 / 2)
    write(output_filename, fs, signal)

if __name__ == "__main__":


    duree = 11  # durée du signal (s)
    f = 8000
    fs = 8000
    #importation du signal
    
    #samplerate, signal = wavfile.read('/home/wall-e/EMA/technologie des média/Georges/TP/signaux/dpcm_xtine_noloss_8bits.wav')
    signal = np.loadtxt('/home/wall-e/EMA/technologie des média/Georges/TP/signaux/xtine.dat', dtype=float)
    print(signal[1])

    #Nombre de bits/éch.
    bits = 8
    signal = quantifier(signal, bits)
    print(signal[1])

    # Paramètres de la simulation
    taille_paquet = 4  # taille du paquet en octets
    probabilite_perte = 0.01# probabilité que la latence se produise (1%)
    
    # Créer le signal modifié avec latence
    signal_paquet, time_quantized = create_lost_packet_signal(signal, taille_paquet, probabilite_perte)
    # Tracer le signal original et le signal modifié
    plot_signal_and_modified_signal(signal, time_quantized, signal_paquet, time_quantized, probabilite_perte)

    # Enregistrer le signal audio modifié
    save_modified_audio(signal_paquet, fs, f'TP/signaux/dpcm_xtine_{probabilite_perte}.wav')
