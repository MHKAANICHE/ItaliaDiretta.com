from flask import Flask, render_template
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    articles = get_articles()  # Fonction pour récupérer les articles traduits
    return render_template('index.html', articles=articles)

@app.route('/archives')
def archives():
    archive_folders = get_archive_folders()  # Fonction pour récupérer la liste des dossiers d'archive
    html_content = "<h1>Archives</h1>"
    for archive_folder in archive_folders:
        html_content += f'<p><a href="/archives/{archive_folder}">{archive_folder}</a></p>'
    return html_content

@app.route('/archives/<archive_folder>')
def view_archive(archive_folder):
    summaries = get_summaries_from_archive(archive_folder)  # Fonction pour récupérer les résumés d'une archive spécifique
    html_content = "<h1>Archive</h1>"
    for summary in summaries:
        html_content += f"<div><p>{summary}</p><hr></div>"
    return html_content


def get_articles():
    articles = []
    general_folder = 'operations_scraper_' + datetime.now().strftime('%Y-%m-%d')
    articles_folder = os.path.join(general_folder, 'translated_arabic_'+ datetime.now().strftime('%Y-%m-%d'))
    
    for filename in os.listdir(articles_folder):
        with open(os.path.join(articles_folder, filename), 'r', encoding='utf-8') as file:
            # Récupérer le titre de l'article
            title = filename.replace('_arabic.txt', '')
            
            # Lire le contenu de l'article
            content = file.read()
            
            # Ajouter l'article à la liste des articles
            articles.append({"title": title, "content": content})
    
    return articles

def generate_html_page():
    articles = get_articles()
    html_content = render_template('index.html', articles=articles)
    with open('templates/index.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

def get_archive_folders():
    return sorted(os.listdir('archive'), reverse=True)

def get_summaries_from_archive(archive_folder):
    summaries = []
    archive_path = os.path.join('archive', archive_folder)
    for filename in os.listdir(archive_path):
        with open(os.path.join(archive_path, filename), 'r', encoding='utf-8') as file:
            summary = file.read()
            summaries.append(summary)
    return summaries

if __name__ == '__main__':
    app.run(debug=True)
