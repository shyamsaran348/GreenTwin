
class CareAdvisor:
    # Knowledge Base: 60+ Common Plants
    # Water Need: 1 (Low/Drought Tol.), 2 (Medium), 3 (High/Thirsty)
    # Heat Tol: 1 (Low/Sensitive), 2 (Medium), 3 (High/Heat Loving)
    PROFILES = {
        # --- Common ML Species ---
        "Tomato": {"water": 3, "heat": 2, "desc": "Thirsty crop, consistent moisture is key."},
        "Potato": {"water": 2, "heat": 1, "desc": "Keep soil cool, tubers stop growing >30°C."},
        "Pepper, Bell": {"water": 2, "heat": 3, "desc": "Loves heat, but keep soil moist."},
        "Corn (Maize)": {"water": 3, "heat": 3, "desc": "High water user during silking."},
        "Apple": {"water": 2, "heat": 2, "desc": "Deep watering needed for fruit set."},
        "Cherry": {"water": 2, "heat": 1, "desc": "Sensitive to cracking in rain."},
        "Grape": {"water": 1, "heat": 3, "desc": "Deep roots, drought tolerant once established."},
        "Peach": {"water": 2, "heat": 3, "desc": "Needs water for fruit expansion."},
        "Strawberry": {"water": 3, "heat": 1, "desc": "Shallow roots, dries out fast."},
        "Squash": {"water": 3, "heat": 2, "desc": "Big leaves lose water fast."},
        "Blueberry": {"water": 3, "heat": 1, "desc": "Acidic soil, shallow roots, needs steady water."},
        "Raspberry": {"water": 2, "heat": 1, "desc": "Mulch heavily to keep roots cool."},
        "Soybean": {"water": 2, "heat": 3, "desc": "Moderate drought tolerance."},
        "Orange": {"water": 2, "heat": 3, "desc": "Deep watering, allow to dry slightly."},

        # --- Common Houseplants ---
        "Snake Plant": {"water": 1, "heat": 3, "desc": "Thrives on neglect. Let dry completely."},
        "Aloe Vera": {"water": 1, "heat": 3, "desc": "Succulent. Rot prone if overwatered."},
        "Peace Lily": {"water": 3, "heat": 1, "desc": "Wilts dramatically when thirsty."},
        "Spider Plant": {"water": 2, "heat": 2, "desc": "Classic, easy care."},
        "Monstera": {"water": 2, "heat": 2, "desc": "Let top inch dry out."},
        "Pothos": {"water": 2, "heat": 2, "desc": "Forgiving, moderate water."},
        "Fiddle Leaf Fig": {"water": 2, "heat": 3, "desc": "Consistent watering, hates drafts."},
        "ZZ Plant": {"water": 1, "heat": 3, "desc": "Store water in rhizomes. Drought king."},
        "Succulent": {"water": 1, "heat": 3, "desc": "Soak and dry method."},
        "Cactus": {"water": 1, "heat": 3, "desc": "Desert native. Minimal water."},
        "Fern": {"water": 3, "heat": 1, "desc": "Loves humidity, keep soil moist."},
        "Orchid": {"water": 2, "heat": 2, "desc": "Soak roots, mist often."},
        "Bamboo": {"water": 3, "heat": 2, "desc": "Keep water fresh."},

        # --- Garden Flowers ---
        "Rose": {"water": 3, "heat": 2, "desc": "Thirsty, avoid wetting leaves (Black Spot)."},
        "Tulip": {"water": 2, "heat": 1, "desc": "Spring bulb, goes dormant in summer."},
        "Lavender": {"water": 1, "heat": 3, "desc": "Mediterranean native, hates wet feet."},
        "Sunflower": {"water": 2, "heat": 3, "desc": "Drought tolerant once established."},
        "Marigold": {"water": 2, "heat": 3, "desc": "Hardy and heat loving."},
        "Hydrangea": {"water": 3, "heat": 1, "desc": "Wilts in hot sun. Needs shade + water."},
        
        # --- Herbs ---
        "Basil": {"water": 3, "heat": 3, "desc": "Loves sun and water. Wilts fast."},
        "Mint": {"water": 3, "heat": 2, "desc": "Invasive roots, thirsty."},
        "Cilantro": {"water": 2, "heat": 1, "desc": "Bolts (flowers) instantly in heat."},
        "Rosemary": {"water": 1, "heat": 3, "desc": "Woody shrub, drought tolerant."},
        "Thyme": {"water": 1, "heat": 3, "desc": "Ground cover, low water."},
    }

    DEFAULT_PROFILE = {"water": 2, "heat": 2, "desc": "General plant care."}

    @staticmethod
    def get_advice(species: str, temperature: float, condition: str = "Clear", humidity: float = 50.0, wind_speed: float = 0.0) -> dict:
        """
        Generate smart context-aware advice.
        """
        # 1. Normalize Species Name
        profile = CareAdvisor.DEFAULT_PROFILE
        species_name = "Unknown Species"
        
        # Direct lookup
        if species in CareAdvisor.PROFILES:
            profile = CareAdvisor.PROFILES[species]
            species_name = species
        else:
            # Fuzzy lookup
            for key in CareAdvisor.PROFILES:
                if key.lower() in species.lower():
                    profile = CareAdvisor.PROFILES[key]
                    species_name = key
                    break
        
        advice_text = ""
        severity = "info" # info, warning, critical, success

        # 2. Logic Engine
        is_hot = temperature > 30.0
        is_cold = temperature < 10.0
        is_dry_air = humidity < 40.0
        is_humid = humidity > 80.0
        is_windy = wind_speed > 25.0
        is_stormy = wind_speed > 50.0
        is_raining = "rain" in condition.lower() or "drizzle" in condition.lower() or "shower" in condition.lower()

        # PRIORITY 1: DANGEROUS WIND/STORM
        if is_stormy:
             advice_text = f"🌪️ STORM ALERT! Wind is {wind_speed}km/h. Move {species_name} indoors immediately or stake it."
             severity = "critical"
        
        # PRIORITY 2: HEAT LOGIC
        elif is_hot:
            if profile['water'] == 3: # Thirsty plant in Heat
                advice_text = f"🔥 Heat Alert! {species_name} is thirsty. Water DEEPLY today to prevent wilting."
                severity = "critical"
            elif profile['heat'] == 1: # Heat Sensitive
                advice_text = f"🔥 Heat Stress! {species_name} hates heat. Consider moving to shade or misting."
                severity = "warning"
            elif profile['heat'] == 3: # Heat Lover
                advice_text = f"☀️ It's hot, but {species_name} loves it! Just plenty of water."
                severity = "success"
            else:
                advice_text = "☀️ High temperatures detected. Check soil moisture daily."
                severity = "warning"

        # PRIORITY 3: COLD LOGIC
        elif is_cold:
            if profile['heat'] >= 2: # Tropical/Heat lover in Cold
                advice_text = f"❄️ Cold Snap! Bring {species_name} indoors or cover it."
                severity = "warning"
            else:
                advice_text = "❄️ Chilly weather. Reduce watering to prevent root rot."
        
        # PRIORITY 4: DRY AIR (For tropicals)
        elif is_dry_air and profile['water'] >= 2:
             advice_text = f"💧 Air is very dry ({humidity}%). Mist leaves or use a pebble tray."
             severity = "info"

        # PRIORITY 5: RAIN
        elif is_raining:
             advice_text = "🌧️ It's raining. Skip watering today!"
             severity = "success"

        # PRIORITY 6: WINDY (Moderate)
        elif is_windy:
             advice_text = f"💨 Breezy day ({wind_speed}km/h). Watch out for tipping pots."
             severity = "info"

        # NORMAL 
        else:
            # General Profile Tip
            advice_text = f"✅ Conditions are good. Tip: {profile['desc']}"

        return {
            "text": advice_text,
            "severity": severity,
            "profile": profile
        }

care_advisor = CareAdvisor()
