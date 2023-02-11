from transformers import AutoTokenizer, BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

# Read each line of the "parsed.txt" file
with open("parsed.txt", "r") as file:
    chapters = file.readlines()

# Summarize each chapter
summary_chapters = []
for idx, chapter in enumerate(chapters):
    # Split the chapter into fragments if it is too long
    fragments = []
    MAX_LENGTH = 1024
    if len(chapter) > MAX_LENGTH:
       index = 0

       while(index < len(chapter)):
            fragment = chapter[index: index + MAX_LENGTH]

            dot_index = fragment.rfind(". ")

            if dot_index != -1:
                fragment = chapter[index: index + dot_index + 1]
                index += dot_index + 1
            else:
                index += MAX_LENGTH

            if len(fragment.strip()) != 0:
                fragments.append(fragment)
    else:
        fragments = [chapter]

    # Summarize each fragment
    chapter_summary = ""
    for fragment in fragments:
        inputs = tokenizer([(fragment)], max_length=1024, return_tensors="pt")
        summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=200)
        chapter_summary = chapter_summary +  tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        if chapter_summary[-1] != '.':
            chapter_summary += '. '


    print("ADDED CHAPTER: " + str(idx + 1))
    summary_chapters.append(chapter_summary)

# Write the summarized chapters to the "summary.txt" file
with open("summary_rand.txt", "w") as file:
    for chapter in summary_chapters:
        file.write(chapter + "\n")