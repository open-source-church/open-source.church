import os
import requests
import datetime
import re
import unicodedata
import json
import yaml

# Configuration
API_URL = "https://opensourcechurch.getgrist.com/api/docs/3XxwRnvDfrfWuvWHp7jjVP/tables/Events/records"
CONTENT_DIR = "content/french/event/grist"
TEMPLATES_DIR = "scripts/templates"

def slugify(value):
    """Transforme un titre en slug propre pour un nom de fichier."""
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

def format_duration(seconds):
    """Convertit des secondes en format HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours:02d}:{minutes:02d}:00"

_templates = {}
def get_template(t):
  # Depuis le cache
  if t in _templates: return _templates[t]
  # Depuis les fichiers
  templateName = os.path.join(TEMPLATES_DIR, t)
  if os.path.exists(templateName):
      with open(templateName, encoding="utf-8") as f:
          template = json.load(f)
          _templates[t] = template
      return _templates[t]
  else:
      print("Trouvé une template qui n'existe pas: ", templateName)


def fetch_and_save_events():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        return

    for record in data.get('records', []):
        fields = record.get('fields', {})
        
        # Extraction et conversion des dates
        start_unix = fields.get('Depart')
        end_unix = fields.get('Fin')
        
        if not start_unix:
            continue

        dt_start = datetime.datetime.fromtimestamp(start_unix)
        dt_end = datetime.datetime.fromtimestamp(end_unix) if end_unix else dt_start

        # Variables de formatage
        iso_date = dt_start.strftime('%Y-%m-%d')
        year = dt_start.strftime('%Y')
        month = dt_start.strftime('%m')
        
        # Gestion du titre et du nom de fichier
        titre = fields.get('Titre', 'Sans titre')
        titre = titre.replace('"', '\"')
        slug = slugify(titre)
        filename = f"{iso_date}-{slug}.md"
        
        # Chemin du dossier : content/event/grist/YYYY/MM
        target_dir = os.path.join(CONTENT_DIR, year, month)
        os.makedirs(target_dir, exist_ok=True)

        # Calcul de la durée
        duration_str = format_duration(end_unix - start_unix) if end_unix else "00:00:00"

        # Image
        image = ""
        if fields.get("Image"):
          image = f'https://opensourcechurch.getgrist.com/api/docs/3XxwRnvDfrfWuvWHp7jjVP/attachments/{fields.get("Image")[1]}/download'
        elif fields.get("ImageURL"):
          image = fields.get("ImageURL")
        
        # Light / featured
        light = "display: light\n"
        if fields.get("Featured"): light = ""

        # Templates
        templates = { "activity": "''" }
        if "Twitch" in fields.get("Lieu", []):
          templates |= get_template("twitch.json")
        if "Taverne" in fields.get("Lieu", []):
          templates |= get_template("taverne.json")
        if "Discord" in fields.get("Lieu", []):
          templates |= get_template("discord.json")
        if "12h" in fields.get("Titre"):
          templates |= get_template("12h.json")

        # Préparation du Frontmatter Hugo
        # Note: On utilise des guillemets simples pour éviter les problèmes avec certains caractères
        content = f"""---
M: '{month}'
Y: '{year}'
date: '{dt_start.isoformat()}'
duration: '{duration_str}'
end: '{dt_end.isoformat()}'
image: {image or ""}
isodate: '{iso_date}'
start: '{dt_start.isoformat()}'
start-unix: {float(start_unix)}
title: "{ titre }"
type: event
{light}
{yaml.dump(templates, sort_keys=False, allow_unicode=True)}
---
{fields.get('Description', '')}
"""

        # Écriture du fichier
        file_path = os.path.join(target_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Généré : {file_path}")

if __name__ == "__main__":
    fetch_and_save_events()