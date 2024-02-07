# PARTIE 1 EXERCICE 1

############# 1/ Creation d'une tonalité sinusoidale ;
#############       - fréquence = 2kHz
#############       - durée = 3s
#############       - échantillon par période = 10


#lib utile
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Paramètres de création du signal
frequence = 2000  # Hz
duree = 3  # secondes
echantillon_periode = 10
frequence_echontillonage = frequence * echantillon_periode

# Création du signal
t = np.linspace(0, duree, int(frequence_echontillonage * duree), endpoint=False)
signal = np.sin(2 * np.pi * frequence * t)

# Convertir le signal en format audible
signal_int16 = np.int16((signal + 1) * 32767 / 2)

# Visualisation - Affichage limité à 3 périodes
periode = 1 / frequence

plt.figure()
plt.plot(t, signal, label='Original')

plt.xlim(0, 3 * periode)  # Limiter l'axe des x à 3 périodes
plt.legend()
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.title(f'Signal normal')
plt.show()


# Enregistrer le signal au format WAV
write('TP\signaux\signal_sinus.wav', frequence_echontillonage, signal_int16)



############# 1/a/ Creation d'unsignal quantifier à 8bits/éch :

# Fonction pour quantifier le signal
def quantifier(signal, bits):
    signal_min = np.min(signal)
    signal_max = np.max(signal)
    q = (signal_max - signal_min) / (2**bits - 1)
    return np.round((signal - signal_min) / q) * q + signal_min


#Nombre de bits/éch.
bits = 8

signal_quantifie_8 = quantifier(signal, bits)
signal_quantifie_int16 = np.int16((signal_quantifie_8 + 1) * 32767 / 2)

# Visualisation - Affichage limité à 3 périodes
periode = 1 / frequence
plt.figure()
plt.plot(t, signal, label='Original')
plt.plot(t, signal_quantifie_8, label=f'Quantifié à 8 bits')
plt.xlim(0, 2 * periode)  # Limiter l'axe des x à 3 périodes
plt.legend()
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.title(f'Quantification à 8 bits')
plt.show()

# Sauvegarder le signal quantifié
write(f'TP/signaux/signal_quantifie_8bits.wav', frequence_echontillonage, signal_quantifie_int16)

"""
On peut voir avec la création de ce signal echantilloné à 8bits/ech
aucune difference visuelle (sur le graph) sans zoomer et aucune 
différence n'est perseptible à l'oreille entre le signal 
sinusoidal et celui ci
"""



############# 1/b/ Creation d'un signal quantifier à :
#############           - 6bits/ech
#############           - 4bits/ech
#############           - 3bits/ech
#############           - 2bits/ech


# Création du signal
for bits in [6, 4, 3, 2]:
    signal_quantifie = quantifier(signal, bits)
    signal_quantifie_int16 = np.int16((signal_quantifie + 1) * 32767 / 2)    
    
    # Visualisation - Affichage limité à 3 périodes
    periode = 1 / frequence
    plt.figure()
    plt.plot(t, signal, label='Original')
    plt.plot(t, signal_quantifie, label=f'Quantifié à {bits} bits')
    plt.xlim(0, 2 * periode)  # Limiter l'axe des x à 3 périodes
    plt.legend()
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitude')
    plt.title(f'Quantification à {bits} bits')
    plt.show()
    
    # Sauvegarder le signal quantifié
    write(f'TP\signaux\signal_quantifie_{bits}bits.wav', frequence_echontillonage, signal_quantifie_int16)
    
    # Pause entre les lectures
    time.sleep(1)

"""
Dans ce cas la on commence a voir visuellement la différence à partir du 4
et auditivement à partir du 6 meme si cela est presque imperceptible.
Plus nous diminuons le nombre de bit par échantillons, moins le signal 
sera de bonne qualité et plus le bruit de quantification sera élevé.
"""



############# 1/c/ Creation d'un signal quantifier à :
#############           - 1bit/ech


#Nombre de bits/éch.
bits = 1

signal_quantifie = quantifier(signal, bits)
signal_quantifie_int16 = np.int16((signal_quantifie + 1) * 32767 / 2)

# Visualisation - Affichage limité à 3 périodes
periode = 1 / frequence_echontillonage
plt.figure()
plt.plot(t, signal, label='Original')
plt.plot(t, signal_quantifie, label=f'Quantifié à 1 bits')
plt.xlim(0, 2 * periode)  # Limiter l'axe des x à 3 périodes
plt.legend()
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude')
plt.title(f'Quantification à 1 bits')
plt.show()


# Sauvegarder le signal quantifié
write(f'TP\signaux\signal_quantifie_1bit.wav', frequence_echontillonage, signal_quantifie_int16)

"""
Dans ce dernier cas la différence en deviens inratable.
Visuellement par le fait qu'il s'agit plus d'une 
séquence de valeur binaire alternante qu'une sinusoidale.
Auditivement le bruit de quantification est vraiment 
présent et tres elevé.
"""