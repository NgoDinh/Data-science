import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords

class ContentEngine(object):

    def __init__(self, input_file):
        """
        read the input file and calculate tfidf matrix

        Arguments
        - input_file (text)   : input file contains two columns: id and description
        """
        self.df_input = pd.read_csv(input_file)
        print(self.df_input.head(10))
        self.tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df_input["description"])
        print(self.tfidf_matrix)

    def predict(self, id, topK):
        """
        predict similarity, given id of the item

        Arguments
        - id (int)      : id of the item in the data file
        - topK (int)    : top-K similar items to retrieve
        """

        index = self.df_input[self.df_input['id'] == id].index.tolist()[0]
        simscore_matrix = linear_kernel(self.tfidf_matrix[index:index+1], self.tfidf_matrix)[0]
        print(simscore_matrix)
        related_docs_indices = [index_sim for index_sim in simscore_matrix.argsort()[::-1] if index_sim != index]


        print("Input: {}".format(self.df_input.iloc[index]["description"]))
        for index_sim in related_docs_indices[:topK]:
            print("\t{}\t{}".format(index_sim, self.df_input.iloc[index_sim]["description"]))

#==========================================================================
if __name__ == "__main__":
    ce = ContentEngine("./sample-data.csv")
    ce.predict(id=4, topK=5)