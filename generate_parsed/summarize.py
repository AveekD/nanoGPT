import openai
import requests

# API key for OpenAI
api_key = "b36f53eb-4057-4c1e-91a1-7e3eeacd430c"

# Read each line of the "parsed.txt" file
with open("parsed.txt", "r") as file:
    chapters = file.readlines()

# Summarize each chapter
summary_chapters = []
count = 0
for chapter in chapters:
    if count > 0:
        break
    count = 1
    # Split the chapter into fragments if it is too long
    fragments = []
    if len(chapter) > 2048:
        # Split the chapter into fragments of length 2048
        fragment_size = 2048
        for i in range(0, len(chapter), fragment_size):
            fragments.append(chapter[i : i + fragment_size])
    else:
        fragments = [chapter]

    # Summarize each fragment
    chapter_summary = ""
    for fragment in fragments:
        api_key = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"
        headers = {
            "api-key": api_key
        }

        text = fragment
        url = "https://api.deepai.org/api/summarization"

        data = {
            "text": text
        }

        response = requests.post(url, headers=headers, data=data)
        print(response.json())
        chapter_summary += response.json()['output']

    summary_chapters.append(chapter_summary)

# Write the summarized chapters to the "summary.txt" file
with open("summary_rand.txt", "w") as file:
    for chapter in summary_chapters:
        file.write(chapter + "\n")
