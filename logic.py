import urllib
import bs4 as bs
import openai

openai.api_key = "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"

source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Taj_Mahal').read()

soup = bs.BeautifulSoup(source, 'lxml')

text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text + "\n"

system_message = "You are a research assistant summarizing the article about the Taj Mahal. Your summary should avoid incomplete sentences and be clear and concise."
prompt = f"{system_message}\nSummarize the most important details and main information from the entire text:\n{text[:1300]}"

response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=400
)

summary = response.choices[0].text.strip()

# Remove content after the last full stop
last_period_index = summary.rfind('.')
final_summary = summary[:last_period_index + 1]

# Remove extra spaces between words
final_summary = " ".join(final_summary.split())

print("Generated Summary:")
print(final_summary)




# import nltk
# import urllib
# import bs4 as bs

# source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Taj_Mahal').read()

# soup = bs.BeautifulSoup(source, 'lxml')

# text = ""
# for paragraph in soup.find_all('p'):
#     text += paragraph.text

# print(text)