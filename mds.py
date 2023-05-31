import matplotlib.pyplot as plt
import matplotlib as mlt
from sklearn.decomposition import PCA
from nlp import nlpdocument

mds = nlpdocument(file)

pca = PCA(n_components=2)
pca.fit_transform(mds)
V = pca.components_