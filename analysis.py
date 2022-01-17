# %%
# Importar Librerías   
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords

# %%
# Lectura de Datos
df= pd.read_csv("articles_PlantBasedNews.csv")
df["All"]= df["Title"] + " " + df["Content"]
print(df["Content"].iloc[10])

# %%
# Quitar Contenido nulo
print("Número de Datos nulos: ",df["Content"].isna().sum())
df.dropna(inplace=True)
print("Número de Datos nulos: ",df["Content"].isna().sum())
# %%
# Unir todos los strings
texto=""
for i in range(len(df)):
    texto= texto+ df["All"].iloc[i]
    if(i%100==0):
        print("Número de filas leidas",i)
texto= texto.lower()
print(len(texto))

# %%
# NLTK downloads
#nltk.download('punkt')
#nltk.download('wordnet')
nltk.download('stopwords')
# %%
#Lexical Diversity
lexicalDiversity= nltk.word_tokenize(texto)
print("Lexical Diversity: ",len(lexicalDiversity))

# %%
#Unique Tokens
uniqueTokens= set(lexicalDiversity)
print("Unique Tokens: ", len(uniqueTokens))

# %%
#Verb lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(w) for w in lexicalDiversity]
print("Unique tokens with lemmatization: ",len(set(lemmatized)))

# %%
# Tokens frecuency larger than 3 characters
dist = FreqDist(lemmatized)
dist= dict(sorted(dist.items(), key=lambda item: item[1]))
vocab1 = dist.keys()
freqwords = [w for w in vocab1 if len(w) > 3]
palabras=list(freqwords)
idx = len(palabras) - 1


# %%
# Dictionary to dataframe
df_frequency=pd.DataFrame(columns= ["Word","Frequency"])
while (idx >= 0):
    df_frequency=df_frequency.append({"Word":palabras[idx],"Frequency":dist[palabras[idx]]},ignore_index=True)
    idx = idx - 1
    if(idx%1000==0):
        print("Palabras restantes: ",idx)
# %%
# Fix Form
df_frequency.set_index("Word",inplace=True)
df_frequency.sort_values(by="Frequency",ascending=False,inplace=True)
df_frequency["Frequency"] = pd.to_numeric(df_frequency["Frequency"], downcast="float")
print(df_frequency.head())
# %%
cloud = WordCloud(width=400,height=330,max_words=150,colormap='tab20c',
                  stopwords=stopwords.words('english'),collocations=True).generate_from_text(texto)
plt.figure(figsize=(10,8))
plt.imshow(cloud)
plt.axis('off')
plt.title("Plant Based News", fontsize=13)
plt.show()
# %%
textLemma= " ".join(lemmatized)

# %%
cloud = WordCloud(width=400,height=330,max_words=150,colormap='tab20c',
                  stopwords=stopwords.words('english'),collocations=True).generate_from_text(textLemma)
plt.figure(figsize=(10,8))
plt.imshow(cloud)
plt.axis('off')
plt.title("Plant Based News", fontsize=13)
plt.show()

