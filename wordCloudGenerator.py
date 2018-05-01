
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
import matplotlib as mpl
import matplotlib.pyplot as plt



def saveWordClouds(genreNames, totGenreLyrics):
    mpl.rcParams['font.size']=12                #10
    mpl.rcParams['savefig.dpi']=100             #72
    mpl.rcParams['figure.subplot.bottom']=.1


    stopwords = set(STOPWORDS)
    stopwords.update(["will", "let", "want"])
    for i in range(len(totGenreLyrics)):
            wordcloud = WordCloud(
                                      background_color='white',
                                      stopwords=stopwords,
                                      max_words=70,
                                      max_font_size=50,
                                      random_state=42
                                     ).generate(totGenreLyrics[i])
            fig = plt.figure(1)
            plt.imshow(wordcloud)
            plt.axis('off')
            #plt.show()
            fig.savefig(genreNames[i]+".png", dpi=900)
