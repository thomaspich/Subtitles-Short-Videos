# 🎬 Editeur de sous-titres interactif avec Whisper, Streamlit & MoviePy

Cette application Streamlit permet de :
- Transcrire automatiquement une vidéo avec Whisper,
- Découper et afficher les sous-titres,
- Les corriger dans une interface web conviviale,
- Voir l'aperçu vidéo synchronisé (avec bouton "▶️ aller à X sec"),
- Générer une nouvelle vidéo avec les sous-titres incrustés,
- Télécharger la vidéo finale depuis l’interface.


## 🧰 Prérequis

- Python 3.8 ou plus
- ffmpeg installé et accessible dans le PATH (nécessaire pour MoviePy et Whisper)

### 🔧 Installation

```bash
git clone https://github.com/ton-utilisateur/ton-projet.git
cd ton-projet
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

## 🚀 Lancer l’application

```bash
streamlit run app.py
```

Cela ouvrira automatiquement l’application dans ton navigateur à l’adresse :
👉 http://localhost:8501

## 📂 Structure


├── app.py                  # Application principale Streamlit\
├── requirements.txt        # Dépendances Python\
├── subtitles_edited.json   # (facultatif) Fichier de sous-titres sauvegardés\
├── temp/                   # Fichiers audio/vidéo temporaires


## 🎨 Fonctionnalités

- Interface en 3 colonnes :
- 📝 Édition des sous-titres défilants
-  🎬 Vidéo HTML5 interactive
-  Boutons pour naviguer dans la vidéo à partir d’un sous-titre
- Génération de la vidéo finale avec MoviePy
- Téléchargement direct dans l’interface

## 📁 Exemple de police personnalisée

Place ton fichier .ttf ou .otf dans le dossier fonts et utilise par exemple :

```
/Library/Fonts/insolent.otf     (Mac)
C:\Windows\Fonts\Montserrat.ttf (Windows)
```

## 🔒 Notes
	•	Les sous-titres sont sauvegardés localement dans subtitles_edited.json.
	•	Le modèle Whisper utilisé est large (peut être modifié selon les performances souhaitées).
	•	Le traitement peut être long pour les vidéos de grande taille.

## 📃 Licence

MIT – libre de réutiliser et modifier comme tu le souhaites.