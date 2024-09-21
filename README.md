# Projet-de-Web-Scraping-avec-Django
Ce projet utilise des techniques de web scraping pour extraire des données de produits à partir de sites tels qu'Amazon, eBay et Alibaba. Les données sont ensuite prétraitées pour obtenir des informations pertinentes sur les produits.
#**Technologies Utilisées**
  - Python
  - Django
  - Scrapy
  - BeautifulSoup
  - Selenium
#**Prérequis:**
Avant de commencer, assurez-vous d'avoir installé les éléments suivants :
  - Python 3.x
  - pip (pour installer les dépendances)

**#Installation :**
1- Clonez le dépôt :
```
git clone https://github.com/ayoub-elmarchoum/Projet-de-Web-Scraping-avec-Django.git
cd Projet-de-Web-Scraping-avec-Django
```
2-Créez un environnement virtuel :
```
python -m venv env
source env/bin/activate  # Pour macOS/Linux
.\env\Scripts\activate   # Pour Windows
```
#**Installez les dépendances :**
```
pip install -r requirements.txt
```

**#Configuration de Django :**
1.Configurer les paramètres :

Ouvrez le fichier settings.py et configurez votre base de données ainsi que d'autres paramètres selon vos besoins.
2.Migrer la base de données :
```
python manage.py migrate
```
3.Démarrer le serveur :
```
python manage.py runserver
```
**#Exécution du Web Scraper :**
1.Accédez au dossier du scraper Scraping_algs :
```
cd "chemin/vers/le/dossier/scraping_algs "
```
2.Exécutez le script Scrapy :
nom_du_spider: choisir entre ce qui dans les fichier dans Scraping_algs
```
scrapy crawl nom_du_spider 
```
**#Data Preprocessing :**
Après l'extraction des données, un simple prétraitement est effectué pour nettoyer et organiser les informations des produits. Cela inclut :

  - Suppression des doublons
  - Normalisation des valeurs
  - Filtrage des données inutiles
**Contribuer:**
Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.













