import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from googletrans import Translator
import spacy
import schedule
import time
import shutil
from theme_synthesis import theme_synthesis  
from server import get_articles

# Chargez le modèle spaCy italien
nlp = spacy.load("it_core_news_sm")

def scrap_site(site_name, url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Exemple : Extraire le titre de la page
            title = soup.title.string
            print(f"Titre du site ({url}) : {title}")

            # Exemple : Extraire le texte du contenu de la page
            content = soup.find('body').get_text()

            # Traiter le texte avec spaCy
            doc = nlp(content)

            # Obtenir un résumé du texte
            summary = " ".join(sent.text.strip() for sent in doc.sents)[:200]  # Les 200 premiers caractères, avec suppression des espaces blancs

            # Créer le dossier "original" avec la date de l'opération (aujourd'hui)
            general_folder = os.path.join('operations_scraper_'+ datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(general_folder):
                os.makedirs(general_folder)

            # Créer le dossier "original" avec la date de l'opération (aujourd'hui)
            # Créer le dossier "original" avec la date de l'opération (aujourd'hui) dans general_folder

            operations_folder = os.path.join(general_folder,'original_' + datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(operations_folder):
                os.makedirs(operations_folder)

            # Enregistrer le fichier CSV avec le nom du site
            csv_filename = os.path.join(operations_folder, f'{site_name}.csv')
            with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Source', 'Résumé'])  # En-tête du CSV
                csv_writer.writerow([site_name, summary])  # Vous pouvez ajouter plus de colonnes au besoin

            # Appel à la fonction theme_synthesis du fichier theme_synthesis.py
            #theme_synthesis(site_name, summary)

            # Enregistrer le fichier de synthèse dans le dossier "synthesis" avec la date de l'opération (aujourd'hui)
            synthesis_folder = os.path.join(general_folder,'synthesis_' + datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(synthesis_folder):
                os.makedirs(synthesis_folder)
            synthesis_filename = os.path.join(synthesis_folder, f'{site_name}.txt')
            with open(synthesis_filename, 'w', encoding='utf-8') as syn_file:
                # Générez un titre avec spaCy
                generated_title = generate_title(summary)                
                syn_file.write(f"Title: {generated_title.strip()}\n")
                syn_file.write(f"{summary.strip()}\n\n")  # Utilisez strip() pour supprimer les espaces blancs
         
            # Enregistrer le fichier traduit en arabe dans le dossier "translated_arabic" avec la date de l'opération (aujourd'hui)
            translated_folder = os.path.join(general_folder,'translated_arabic_' + datetime.now().strftime('%Y-%m-%d'))
            if not os.path.exists(translated_folder):
                os.makedirs(translated_folder)
            translated_filename = os.path.join(translated_folder, f'{site_name}_arabic.txt')
            with open(translated_filename, 'w', encoding='utf-8') as arabic_file:
                 # Traduire le résumé en arabe
                translated_summary = translate_to_arabic(summary)
                translated_title = translate_to_arabic(generated_title)
                # Placeholder pour le texte traduit en arabe
                arabic_file.write(f"Title: {translated_title.strip()}\n")
                arabic_file.write(f"Summary: {translated_summary.strip()}\n\n")  # Utilisez strip() pour supprimer les espaces blancs


        else:
            print(f"Erreur de requête ({url}) : {response.status_code}")

    except Exception as e:
        print(f"Une erreur s'est produite ({url}) : {e}")

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



def archive_old_operations():
    # Récupérez la date actuelle
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Créez un dossier "archive" s'il n'existe pas
    archive_folder = os.path.join('archive')
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)

    # Obtenez le répertoire de travail actuel
    current_directory = os.getcwd()

    # Parcourez les dossiers dans le dossier du projet
    for folder_name in os.listdir(current_directory):
        if folder_name.startswith("operation_scraper"):  
            operation_date = folder_name.replace("operation_scraper", "")
            # Comparez la date de l'opération avec la date actuelle
            if operation_date < current_date:
                source_path = os.path.join(project_folder_absolute, folder_name)
                destination_path = os.path.join(archive_folder, folder_name)
                shutil.move(source_path, destination_path)

def main_scraping_job():
    # Liste des sites à scraper (nom, URL)
    sites_to_scrape = [
        #("la Repubblica", "https://quotidiano.repubblica.it/"),
        #("La Stampa", "https://www.lastampa.it/"),
        #("Il Sole 24 Ore", "https://www.ilsole24ore.com/"),
        #("il Fatto Quotidiano", "https://www.ilfattoquotidiano.it/"),
        ("La Gazzetta dello Sport", "https://www.gazzetta.it/"),
        #("Il Messaggero", "https://www.ilmessaggero.it/"),
        #("Il Resto del Carlino", "https://www.ilrestodelcarlino.it/"),
        #("La Nazione", "https://www.lanazione.it/"),
        #("Il Secolo XIX", "https://www.ilsecoloxix.it/"),
        ("Il Gazzettino", "https://www.ilgazzettino.it/"),
        #("Il Giornale", "https://www.ilgiornale.it/"),
        #("Corriere dell'Umbria", "https://corrieredellumbria.it/"),
        #("L'Arena", "https://www.larena.it/"),
        #("l'Unità", "https://www.unita.it/"),
        #("La Padania", "https://www.lanuovapadania.it/"),
        #("La Notizia", "https://www.lanotiziagiornale.it/"),
        #("L'Eco di Bergamo", "https://www.ecodibergamo.it/"),
        #("Secolo d'Italia", "https://www.secoloditalia.it/"),
        #("L'Unione Sarda", "https://www.unionesarda.it/"),
        #("Messaggero Veneto  Giornale del Friuli", "https://messaggeroveneto.gelocal.it/"),
        #("Il Mattino", "https://www.ilmattino.it/"),  # Correction de l'URL
        #("Tuttosport", "https://www.tuttosport.com/"),
        #("Avvenire", "https://www.avvenire.it/"),
        #("La Sicilia", "https://www.lasicilia.it/"),
        #("Giornale di Sicilia", "https://gds.it/"),
        #("La Gazzetta del Mezzogiorno", "https://www.lagazzettadelmezzogiorno.it/"),
        #("Il Giornale di Vicenza", "https://www.ilgiornaledivicenza.it/"),
        #("l'Adige", "https://www.ladige.it/"),
        #("Giornale di Brescia", "https://www.giornaledibrescia.it/"),
        #("Gazzetta di Parma", "https://www.gazzettadiparma.it/"),
        #("Gazzetta del Sud", "https://gazzettadelsud.it/"),
        #("Gazzetta di Modena", "https://www.gazzettadimodena.it/"),
        #("Gazzetta di Mantova", "https://gazzettadimantova.gelocal.it/mantova/"),
        #("Libero", "https://www.libero.it/"),
        #("Corriere del Trentino", "https://corrieredeltrentino.corriere.it/"),
        ("Metro", "https://metronews.it/")
    ]

    for site_data in sites_to_scrape:
        print(f"\nScrapping du site : {site_data[0]}")
        scrap_site(*site_data)

    # Une fois le scraping et la traduction terminés, générez la page HTML
    get_articles()

    # Archivez les anciennes opérations
    archive_old_operations()

   

if __name__ == "__main__":
    # Check if the folder for today's date exists
    current_date_folder = os.path.join('operations_scraper', datetime.now().strftime('%Y-%m-%d'))
    
    if not os.path.exists(current_date_folder):
        print(f"Folder for today's date does not exist. Running scraping once to generate initial data.")
        main_scraping_job()  # Run scraping once

    # Planify scraping every day at 5 AM Italian time
    schedule.every().day.at("05:00").do(main_scraping_job)

    # Execute the scheduling in a loop
    while True:
        schedule.run_pending()
        time.sleep(1)
