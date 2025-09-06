import logging
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.mistral import MistralChat
from firecrawl import FirecrawlApp

# Configuration du logging
logging.basicConfig(level=logging.INFO)

# Charger les variables d'environnement
load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Vérification des clés
if not FIRECRAWL_API_KEY:
    raise ValueError("⚠️ FIRECRAWL_API_KEY manquant dans .env")
if not MISTRAL_API_KEY:
    raise ValueError("⚠️ MISTRAL_API_KEY manquant dans .env")

# Initialiser Firecrawl
firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)

# Initialiser l'agent avec Mistral
agent = Agent(
    model=MistralChat(id="mistral-medium", api_key=MISTRAL_API_KEY),
    system_message="You are a professional assistant. Read documents carefully, summarize, and answer questions based on the content."
)

# URL du PDF à analyser
url_to_crawl = "https://www.pwc.com/gx/en/issues/analytics/assets/pwc-ai-analysis-sizing-the-prize-report.pdf"

# Extraire le contenu du PDF avec Firecrawl
response = firecrawl.crawl(url_to_crawl)
output_data = dict(response)
pdf_text_content = output_data.get("data")

if pdf_text_content:
    logging.info("✅ PDF content extracted.")

    # Étape 1 : Résumé automatique
    print("\n📌 Résumé automatique du PDF :\n")
    agent.print_response(
        f"Summarize the following PDF content:\n\n{pdf_text_content[:20000]}",
        stream=True
    )

    # Étape 2 : Q&A interactif
    while True:
        question = input("\nPose ta question sur le contenu du PDF (ou tape 'exit' pour quitter) : ")
        if question.lower() == "exit":
            break
        agent.print_response(
            f"Answer the following question based on the PDF content:\n\n{question}\n\nContext:\n{pdf_text_content[:20000]}",
            stream=True
        )
else:
    logging.warning("⚠️ Aucun contenu extrait du PDF.")
