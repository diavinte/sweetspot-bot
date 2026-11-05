import os
import re
import requests
import tweepy
from google import genai

# ==========================================================
# 1. CONFIGURAÇÕES E CHAVES
# ==========================================================
AMAZON_US_TAG = "sweetspotaler-20"  

# Chaves Gemini e Discord
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Chaves X (Twitter)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

if not GEMINI_API_KEY:
    print("Erro: A chave GEMINI_API_KEY não foi encontrada!")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================================
# 2. RADAR DE PALAVRAS-CHAVE (Pickleball, Padel & Recovery)
# ==========================================================
KEYWORDS_RADAR = {
    "rackets_paddles": [
        # Padel - Top 10 Men (Coello, Tapia, Galan, Chingotto, Lebron...)
        "head extreme pro", "padel", "nox at10 genius", "18k alum", "12k", "adidas metalbone", "metalbone hrd",
        "bullpadel neuron", "babolat technical viper", "siux electra", "bullpadel hack", "bullpadel vertex", "nox la10",
        # Padel - Top 10 Women (Triay, Brea, Bea, Josemaria, Ari Sanchez...)
        "bullpadel elite", "bullpadel vertex w", "bullpadel pearl", "head speed motion", "adidas cross it", "ionic light",
        # Pickleball (Mantido para não perder o nicho original)
        "joola perseus", "six zero", "selkirk", "crbn"
    ],
    "shoes_footwear": [
        # Premier Padel Pro Shoes
        "head motion pro", "nox at10 pro", "adidas barricade", "babolat jet premura",
        "bullpadel hack vibram", "bullpadel vertex shoes", "asics gel resolution padel",
        "asics solution swift", "adidas defiant speed", "babolat movea", "padel shoes"
    ],
    "bags_backpacks": [
        # Premier Padel Pro Bags
        "head coello tour", "nox at10 team", "adidas protour", "adidas promatch", 
        "bullpadel bpp", "babolat rh padel", "padel racket bag", "tour bag", "paletero"
    ],
    "consumables_accessories": [
        # Balls
        "wilson premier padel", "head pro s", "bullpadel premium pro", "padel balls 3-pack", "case of balls",
        "franklin x-40", "dura fast 40", # Pickleball balls
        # Grips & Overgrips
        "hesacore", "nox custom grip", "tourna grip", "yonex super grap", "wilson pro overgrip", "padel overgrip",
        # Wristbands & Extras (inclui o Floky usado pelo Tapia)
        "bullpadel wristband", "adidas wristband", "head wristband", "pascal box", "padel cap", "floky arm sleeve"
    ],
    "apparel_clothing": [
        # Roupas
        "padel shirt", "padel shorts", "padel skirt", "nox sponsor t-shirt", 
        "adidas club 3str", "bullpadel wpt", "premier padel official"
    ],
    "recovery_injury_prevention": [
        "theragun", "hyperice", "normatec", "theraband flexbar", 
        "bauerfeind", "rotator cuff", "tennis elbow", "massage gun", "compression sleeve"
    ]
}

DEAL_TRIGGERS = ["deal", "padel", "sale", "clearance", "off", "drop", "price", "code", "coupon", "atl", "$"]

# ==========================================================
# 3. GERADOR DE LINK AFILIADO
# ==========================================================
def build_us_affiliate_link(url: str) -> str:
    asin_match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", url)
    if asin_match:
        asin = asin_match.group(1)
        return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_US_TAG}"
    return url

# ==========================================================
# 4. ENGENHARIA DE PROMPT
# ==========================================================
def generate_court_insider_copy(product_title: str, price_info: str, category: str) -> str:
    prompt = f"""
    You are an experienced US Pickleball (4.5+ DUPR) and Padel player who runs a gear price-drop radar called SweetSpot Alerts.
    Write a short, punchy 3-line deal alert in native US English for the following item:
    
    Item: {product_title}
    Price/Deal Context: {price_info}
    Category: {category}

    Rules:
    - NO generic sales hype ("Amazing deal!", "Don't miss out!").
    - Use authentic court terminology (e.g., raw carbon grit, sweet spot, swing weight, saving shoulders/rotator cuff, or bulk court stocking).
    - Format: 
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
# 5. BUSCA DE SINAIS
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
# 6. FUNÇÕES DE PUBLICAÇÃO (X e Discord)
# ==========================================================
def post_to_twitter(text: str):
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]):
        print("Aviso: Chaves do X ausentes. A saltar publicação no X.")
        return
    try:
        twitter_client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET
        )
        twitter_client.create_tweet(text=text)
        print("✅ Alerta publicado no X com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao publicar no X: {e}")

def post_to_discord(text: str):
    if not DISCORD_WEBHOOK_URL:
        print("Aviso: Webhook do Discord ausente. A saltar publicação no Discord.")
        return
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": text})
        if response.status_code in [200, 204]:
            print("✅ Alerta publicado no Discord com sucesso!")
        else:
            print(f"❌ Erro no Discord. Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao publicar no Discord: {e}")

# ==========================================================
# 7. EXECUÇÃO PRINCIPAL
# ==========================================================
if __name__ == "__main__":
    print("🎾 SweetSpot Alerts Bot iniciado. Buscando sinais de quadra...")
    
    # O robô agora faz rondas nos dois subreddits!
    deals_pickleball = fetch_court_signals("Pickleball")
    deals_padel = fetch_court_signals("padel")
    
    # Junta as ofertas encontradas nas duas comunidades
    deals = deals_pickleball + deals_padel
    
    if not deals:
        print("Nenhum alerta recente encontrado no momento. O radar está ativo.")
    
    for deal in deals:
        print("\n--- NOVO ALERTA DETECTADO ---")
        copy = generate_court_insider_copy(deal["title"], "Price Drop Alert", deal["category"])
        
        # Junta o texto persuasivo ao link de afiliado
        final_message = f"{copy}\n\nLink: {deal['url']}"
        print(final_message)
        
        # Dispara para as redes!
        post_to_twitter(final_message)
        post_to_discord(final_message)
