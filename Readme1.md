# Century21 Scraper & Airtable Import

Ce projet permet de **scraper les annonces immobilières** sur le site [Century21 France](https://www.century21.fr/) pour Paris, puis d'importer automatiquement les données dans **Airtable**. Il utilise **Firecrawl** pour le scraping et **BeautifulSoup** pour le parsing du HTML.

---

## Fonctionnalités

- Récupération des annonces immobilières depuis Century21.
- Extraction des informations clés :
  - Référence de l’annonce
  - Prix
  - Localisation
  - Description
- Gestion automatique de plusieurs pages pour récupérer toutes les annonces.
- Vider la table Airtable existante avant d’ajouter les nouvelles annonces.
- Ajout des annonces dans Airtable via l’API.

---

## Technologies utilisées

- Python 3.x
- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Firecrawl](https://firecrawl.com/)
- [Airtable API](https://airtable.com/api)

---

## Prérequis

- Clé API **Firecrawl**
- Clé API **Airtable**
- Base et table Airtable configurées pour recevoir les annonces

---
# Analyse de PDF avec Mistral via Agno

Ce projet permet d'extraire le texte d’un PDF depuis une URL, de générer un résumé automatique et de poser des questions interactives sur le contenu grâce à l'agent Mistral via Agno.

## Fonctionnalités

- Extraction du texte d’un PDF via **Firecrawl**.  
- Résumé automatique des contenus volumineux.  
- Session de Q&A interactive basée sur le contenu du PDF.  
- Analyse intelligente avec un agent **Mistral**.

## Technologies Utilisées

- Python 3.x  
- [Firecrawl](https://firecrawl.com/)  
- [Agno + Mistral](https://www.mistral.ai/)  
- dotenv  
- logging

## Installation


