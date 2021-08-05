
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import wikipedia
import en_core_web_sm
 
# Get wiki content.
wikisearch = wikipedia.page("Amitabh Bachchan")
wikicontent = wikisearch.content
nlp = en_core_web_sm.load()
doc = nlp(wikicontent)
 
# Save the wiki content to a file
# (for reference).
f = open("wikicontent.txt", "w")
f.write(wikicontent)
f.close()
 
# Summary (0.5% of the original content).
summ_per = summarize(wikicontent, ratio = 0.05)
print("Percent summary")
print(summ_per)
 
# Summary (200 words)
summ_words = summarize(wikicontent, word_count = 200)
print("Word count summary")
print(summ_words)