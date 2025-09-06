import requests
from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp

# ----------------------------
# 1️⃣ Configuration Airtable
# ----------------------------
AIRTABLE_API_KEY = "patgGsSMJ46SSixx3.8ad1904157902b874d529c41a675f8e899de3b4f75e80d6ad0ec3b230f74a358"
AIRTABLE_BASE_ID = "appRPc9LeKX4jXhDN"
AIRTABLE_TABLE_ID = "tblvHmeoDYf0qhQps"

# ----------------------------
# 2️⃣ Firecrawl API
# ----------------------------
firecrawl = FirecrawlApp(api_key="fc-6654d042103f407f9f0f5bd160c83193")
url = "https://www.century21.fr/annonces/f/achat/v-paris/"

# ----------------------------
# 3️⃣ Fonctions de parsing
# ----------------------------
def clean_text_block(text_block):
    lines = [line.strip() for line in text_block.splitlines() if line.strip()]
    return "\n".join(lines)

def split_listings(text):
    parts = text.split("Ref :")
    listings = []
    for part in parts[1:]:
        listings.append("Ref :" + clean_text_block(part))
    return listings

def simple_parse(text):
    listings = split_listings(text)
    records = []

    for listing in listings:
        lines = listing.split("\n")
        record = {}

        # Référence
        record['Référence'] = lines[0].replace("Ref :", "").strip()

        # Prix
        price_line = next((l for l in lines if '€' in l), "")
        clean_price = price_line.replace("€", "").replace("\xa0", "").replace(" ", "").strip()
        record['Prix'] = int(clean_price) if clean_price.isdigit() else 0

        # Localisation
        location_line = next((l for l in lines if 'PARIS' in l.upper()), "")
        record['Localisation'] = location_line.strip()

        # Description
        try:
            price_index = lines.index(price_line)
            detail_index = lines.index(next(l for l in lines if 'Voir le détail du bien' in l))
            description = " ".join(lines[price_index + 1:detail_index]).strip()
            record['Description'] = description
        except StopIteration:
            record['Description'] = ""
        
        records.append(record)
    return records

# ----------------------------
# 4️⃣ Vider la table Airtable
# ----------------------------
def clear_airtable_table():
    url_get = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    response = requests.get(url_get, headers=headers)
    data = response.json()

    if "records" in data:
        for rec in data['records']:
            rec_id = rec['id']
            del_response = requests.delete(f"{url_get}/{rec_id}", headers=headers)
            if del_response.status_code in [200, 204]:
                print(f"🗑️ Record supprimé : {rec_id}")
            else:
                print(f"❌ Impossible de supprimer le record {rec_id} : {del_response.text}")

# ----------------------------
# 5️⃣ Scraping via Firecrawl
# ----------------------------
def scrape_page(url):
    scrape_result = firecrawl.scrape(url, formats=["html"])
    plain_html = scrape_result.html
    soup = BeautifulSoup(plain_html, "html.parser")
    return soup.get_text()

# ----------------------------
# 6️⃣ Ajouter les records dans Airtable
# ----------------------------
def add_records_to_airtable(records):
    url_post = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    for record in records:
        response = requests.post(url_post, headers=headers, json={"fields": record})
        if response.status_code in [200, 201]:
            print(f"✅ Record ajouté : {record['Référence']}")
        else:
            print(f"❌ Impossible d'ajouter le record {record['Référence']} : {response.text}")

# ----------------------------
# 7️⃣ Exécution
# ----------------------------
print("🔹 Vider la table Airtable existante...")
clear_airtable_table()

print("🔹 Scraping de la page...")
plain_text = scrape_page(url)

print("🔹 Parsing des annonces...")
records = simple_parse(plain_text)

print(f"🔹 {len(records)} annonces trouvées. Ajout dans Airtable...")
add_records_to_airtable(records)

print("🎉 Terminé !")
