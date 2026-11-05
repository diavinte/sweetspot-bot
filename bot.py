import os
import re
import requests
from google import genai


# 1. CONFIGURAÇÕES E CHAVES (Insira sua tag da Amazon US)
# ==========================================================
AMAZON_US_TAG = "sweetspotaler-20"  # Substitua pela sua tag oficial da Amazon Associates US
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Inicializa o client oficial do Gemini

# 1. CONFIGURAÇÕES E CHAVES
# ==========================================================
AMAZON_US_TAG = "sweetspotaler-20"  

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# TRAVA DE SEGURANÇA: Evita o erro silencioso no GitHub Actions
if not GEMINI_API_KEY:
    print("Erro: A chave GEMINI_API_KEY não foi encontrada pelo GitHub Actions!")
    exit(1)

# Inicializa o client oficial do Gemini apenas uma vez
>>>>>>> d2200f5 (Corrige inicialização da API no SweetSpot bot)
client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================================
# 2. RADAR DE PALAVRAS-CHAVE (Pickleball, Padel & Recovery)
# ==========================================================
KEYWORDS_RADAR = {
    "rackets_paddles": [
        "joola perseus", "six zero", "selkirk", "crbn", 
        "bullpadel vertex", "bullpadel hack", "nox at10", "raw carbon"
    ],
    "consumables_bulk": [
        "franklin x-40", "dura fast 40", "100 pack", "36 pack", 
        "tourna grip", "yonex super grap", "hesacore"
    ],
    "recovery_injury_prevention": [
        "theragun", "hyperice", "normatec", "theraband flexbar", 
        "bauerfeind", "rotator cuff", "tennis elbow", "massage gun"
    ]
}

DEAL_TRIGGERS = ["deal", "sale", "clearance", "off", "drop", "price", "code", "coupon", "atl", "$"]

# ==========================================================
# 3. GERADOR DE LINK AFILIADO (AMAZON US)
# ==========================================================
def build_us_affiliate_link(url: str) -> str:
    """Extrai o ASIN de qualquer link da Amazon.com e reconstrói limpo com a sua Tag US."""
    asin_match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", url)
    if asin_match:
        asin = asin_match.group(1)
        return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_US_TAG}"
    return url

# ==========================================================
# 4. ENGENHARIA DE PROMPT: COPYWRITER "INSIDER DE QUADRA"
# ==========================================================
def generate_court_insider_copy(product_title: str, price_info: str, category: str) -> str:
    """Usa o Gemini para gerar uma chamada curta em inglês nativo com vocabulário técnico."""
    prompt = f"""
    You are an experienced US Pickleball (4.5+ DUPR) and Padel player who runs a gear price-drop radar called SweetSpot Alerts.
    Write a short, punchy 3-line deal alert in native US English for the following item:
    
    Item: {product_title}
    Price/Deal Context: {price_info}
    Category: {category}

    Rules:
<<<<<<< HEAD
    - NO generic sales hype ("Amazing deal!", "Don't miss out!").
    - Use authentic court terminology (e.g., raw carbon grit, sweet spot, swing weight, saving shoulders/rotator cuff, or bulk court stocking).
    - Format: 
=======
- NO generic sales hype ("Amazing deal!", "Don't miss out!").
- Use authentic court terminology (e.g., raw carbon grit, sweet spot, swing weight, saving shoulders/rotator cuff, or bulk court stocking).
- Format: 
>>>>>>> d2200f5 (Corrige inicialização da API no SweetSpot bot)
      1️⃣ Short headline with an emoji.
      2️⃣ One sentence on WHY this gear matters on court.
      3️⃣ One line highlighting the price drop / historic low.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()

# ==========================================================
<<<<<<< HEAD
# 5. MONITOR DE SINAIS (Exemplo via Reddit / Feeds)
=======
# 5. MONITOR DE SINAIS (Reddit / Feeds)
>>>>>>> d2200f5 (Corrige inicialização da API no SweetSpot bot)
# ==========================================================
def fetch_court_signals(subreddit: str = "Pickleball"):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=10"
    headers = {"User-Agent": "SweetSpotRadar/1.0"}
    
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return []

    posts = response.json().get("data", {}).get("children", [])
    matched_deals = []

    for post in posts:
        data = post.get("data", {})
        title = data.get("title", "")
        selftext = data.get("selftext", "")
        ext_url = data.get("url", "")
        full_text = f"{title} {selftext}".lower()

        if any(trigger in full_text for trigger in DEAL_TRIGGERS):
            for category, keywords in KEYWORDS_RADAR.items():
                if any(kw in full_text for kw in keywords):
                    matched_deals.append({
                        "title": title,
                        "url": build_us_affiliate_link(ext_url),
                        "category": category
                    })
                    break
    return matched_deals

# ==========================================================
<<<<<<< HEAD
# 6. TESTE DE EXECUÇÃO LOCAL
=======
# 6. TESTE DE EXECUÇÃO
>>>>>>> d2200f5 (Corrige inicialização da API no SweetSpot bot)
# ==========================================================
if __name__ == "__main__":
    print("🎾 SweetSpot Alerts Bot iniciado. Buscando sinais de quadra...")
    deals = fetch_court_signals("Pickleball")
    
    if not deals:
        print("Nenhum alerta recente encontrado no momento. O radar está ativo.")
    for deal in deals:
        print("\n--- NOVO ALERTA DETECTADO ---")
        copy = generate_court_insider_copy(deal["title"], "Price Drop Alert", deal["category"])
        print(copy)
<<<<<<< HEAD
        print(f"Link Afiliado: {deal['url']}")
=======
        print(f"Link Afiliado: {deal['url']}")
>>>>>>> d2200f5 (Corrige inicialização da API no SweetSpot bot)
