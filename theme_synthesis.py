import os
from googletrans import Translator
import spacy

def theme_synthesis(site_name, summary):
    # Créez un dossier "articles_to_publish" s'il n'existe pas
    articles_folder = 'articles_to_publish'
    if not os.path.exists(articles_folder):
        os.makedirs(articles_folder)

    # Créez un fichier texte par thème avec le nom du site comme préfixe
    theme_filename = os.path.join(articles_folder, f'{site_name}_synthesis.txt')

    # Enregistrez la synthèse dans le fichier texte
    with open(theme_filename, 'a', encoding='utf-8') as file:
        file.write(f"{summary.strip()}\n\n")  # Utilisez strip() pour supprimer les espaces blancs

    # Générez un titre avec spaCy
    generated_title = generate_title(summary)

    # Traduire le résumé en arabe
    translated_summary = translate_to_arabic(summary)
    translated_title = translate_to_arabic(generated_title)

    # Créez un dossier "articles_to_publish_arabic" s'il n'existe pas
    arabic_folder = 'articles_to_publish_arabic'
    if not os.path.exists(arabic_folder):
        os.makedirs(arabic_folder)

    # Créez un fichier texte par thème avec le nom du site comme préfixe (arabe)
    arabic_theme_filename = os.path.join(arabic_folder, f'{site_name}_synthesis_arabic.txt')

    # Enregistrez la synthèse traduite dans le fichier texte (arabe)
    with open(arabic_theme_filename, 'a', encoding='utf-8') as arabic_file:
        arabic_file.write(f"Title: {translated_title.strip()}\n")
        arabic_file.write(f"Summary: {translated_summary.strip()}\n\n")  # Utilisez strip() pour supprimer les espaces blancs

def generate_title(text):
    # Utilisez spaCy pour extraire des entités clés ou effectuer une autre analyse pour générer un titre
    nlp = spacy.load("it_core_news_sm")
    doc = nlp(text)
    
    # Exemple : Obtenez les entités nommées du texte
    entities = [ent.text for ent in doc.ents]
    
    # Utilisez les entités pour générer un titre (vous pouvez personnaliser cette partie)
    generated_title = f"News about {', '.join(entities)}"

    return generated_title

def translate_to_arabic(text):
    # Utiliser la bibliothèque Googletrans pour la traduction
    translator = Translator()
    translation = translator.translate(text, src='auto', dest='ar')
    return translation.text
