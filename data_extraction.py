import requests
from bs4 import BeautifulSoup
import json
import os

transcripts = [
    {
        "url": "https://lexfridman.com/yann-lecun-3-transcript",
        "full_video":"Yann Lecun | Lex Fridman Podcast #416_(https://www.youtube.com/watch?v=5t1vTLU7s40)",
        "filename": "yann_lecun_transcript.json"
    },
    {
        "url": "https://lexfridman.com/sam-altman-2-transcript/", 
        "full_video":"Sam Altman| L ex Fridman Podcast #419_(https://www.youtube.com/watch?v=jvqFAi7vkBc)",
        "filename": "sam_altman_transcript.json"
    },
    {
        "url": "https://lexfridman.com/elon-musk-4-transcript/",
        "full_video":"Elon Musk | Lex Fridman Podcast #400_(https://www.youtube.com/watch?v=JN3KPFbWCy8)",
        "filename": "elon_musk_transcript.json"
    },
    {
        "url": "https://lexfridman.com/ben-shapiro-destiny-debate-transcript/",
        "full_video":"Ben Shapiro vs Destiny Debate | Lex Fridman Podcast #410_(https://www.youtube.com/watch?v=tYrdMjVXyNg)",
        "filename": "ben_shapiro_destiny_debate_transcript.json"
    }
]

headers = {"User-Agent": "Mozilla/5.0"}

for transcript in transcripts:
    url = transcript["url"]
    output_file = transcript["filename"]
    full_video = transcript["full_video"]
    
    print(f"Processing {url}...")
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        sections = soup.find_all("h2")

        extracted_data = []

        for i, section in enumerate(sections):
            if section.has_attr("id"):
                current_section = section.get_text(strip=True)

                next_section = sections[i + 1] if i + 1 < len(sections) else None
                
                current_elem = section.next_sibling
                while current_elem and current_elem != next_section:
                    if isinstance(current_elem, str):  # Skip text nodes
                        current_elem = current_elem.next_sibling
                        continue
                        
                    if current_elem.get("class") == ["ts-segment"]:
                        # Extract speaker name
                        speaker_elem = current_elem.find("span", class_="ts-name")
                        speaker = speaker_elem.get_text(strip=True) if speaker_elem else ""
                        
                        # Extract timestamp and YouTube link
                        timestamp_elem = current_elem.find("span", class_="ts-timestamp")
                        if timestamp_elem and timestamp_elem.find("a"):
                            youtube_link = timestamp_elem.find("a")["href"]
                            timestamp = timestamp_elem.find("a").get_text(strip=True)
                        else:
                            youtube_link = ""
                            timestamp = ""
                        
                        # Extract spoken text
                        text_elem = current_elem.find("span", class_="ts-text")
                        spoken_text = text_elem.get_text(strip=True) if text_elem else ""

                        # Store data in structured format
                        extracted_data.append({
                            "full_video": full_video,
                            "section_topic": current_section,
                            "speaker": speaker,
                            "speech": spoken_text,
                            "youtube_link": youtube_link,
                            "timestamp": timestamp
                        })

                    current_elem = current_elem.next_sibling

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(extracted_data, file, indent=4, ensure_ascii=False)

        print(f"Transcript extracted successfully! Data saved to '{output_file}'")

    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
