import numpy as np
import simpleaudio as sa

# Paramètres du son
fréquence = 2000  # Fréquence en Hertz
durée = 3  # Durée en secondes
échantillons_par_période = 10

# Calculer la fréquence d'échantillonnage
fréquence_échantillonnage = 44100

# Générer les échantillons audio
t = np.linspace(0, durée, int(durée * fréquence_échantillonnage), False)  # Temps
note = np.sin(fréquence * t * 2 * np.pi)  # Générer le signal sonore (onde sinusoïdale)
audio = note * (2**15 - 1) / np.max(np.abs(note))  # Normaliser à 16-bit range

# Convertir en type de données requis par simpleaudio
audio = audio.astype(np.int16)

# Jouer le son
play_obj = sa.play_buffer(audio, 1, 2, fréquence_échantillonnage)
play_obj.wait_done()  # Attendre la fin du son
