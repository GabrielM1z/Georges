import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Fonction pour quantifier le signal
def quantifier(signal, bits):
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    q = (signal_max - signal_min) / (2**bits - 1)
    return np.round((signal - signal_min) / q) * q + signal_min




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
print('len==',signal.shape)
# Paramètres de la simulation
taille_paquet = 2  # taille du paquet en octets

# Fonction pour compter le nombre de paquets
def nombre_paquets(signal, taille_paquet):
    nb = 0
    for i in range(0, len(signal), taille_paquet):
        nb += 1
    print("Nombre de paquets :", nb)

def perte_paquets(signal, taille_paquet,probabilite_perte):
    nb = 0
    signal_perte = np.array([])
    for i in range(0, len(signal), taille_paquet):
        if np.random.rand() < probabilite_perte:
            signal_perte = np.append(signal_perte, [0,0])
            nb += 1
        else:
            signal_perte = np.append(signal_perte, signal[i:i+taille_paquet])
    print("Nombre de pertes :", nb)
    return signal_perte

#Fonction pour simuler l'envoi de paquets avec latence
def envoyer_paquets(signal_bytes, taille_paquet,probabilite_perte,signal_perte):
    nb = 0
    for i in range(0, len(signal_bytes), taille_paquet):
        if np.random.rand() > probabilite_perte :
            signal_perte.extend(signal_bytes[i:i+taille_paquet])
        else:
            print("ko",signal[i:i+taille_paquet])
            signal_perte.extend([0, 0])
            nb += 1
    print("Nombre de perte",nb)
    
def save_modified_audio(signal, fs, output_filename):
    signal = np.nan_to_num(signal)
    signal = np.int16((signal + 1) * 32767 / 2)
    write(output_filename, fs, signal)

def plot_signal_and_modified_signal(nb_p_plot, signal, signal_perte, fs, probabilite_perte):
    temps = np.linspace(0, len(signal) / fs, len(signal))
    temps_perte = np.linspace(0, len(signal_perte) / fs, len(signal_perte))

    periode = 1 / frequence
    plt.figure(figsize=(10, 6))
    plt.plot(temps, signal, label='Signal Original', color='blue')
    plt.plot(temps_perte, signal_perte, label='Signal avec Perte', color='red', alpha=0.7)
    plt.xlim(0, nb_p_plot * periode)  # Limiter l'axe des x à 3 périodes
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Comparaison du Signal Original et du Signal avec Perte ({probabilite_perte*100}%)')
    plt.legend()
    plt.grid(True)
    plt.show()

    
# Tester avec différentes probabilités de perte
for probabilite_perte in [0.001, 0.01, 0.1]:
    print(f"Test avec une probabilité de perte de {probabilite_perte*100} %.")
    nombre_paquets(signal, taille_paquet)
    signal_perte = perte_paquets(signal, taille_paquet,probabilite_perte)
    plot_signal_and_modified_signal(10, signal, signal_perte, frequence_echontillonage, probabilite_perte)
    #    Convertir le signal en format audible
    signal_int16 = np.int16((signal_perte + 1) * 32767 / 2)
    save_modified_audio(signal_int16, frequence_echontillonage, f'TP\signaux\perte_{probabilite_perte}_signal.wav')