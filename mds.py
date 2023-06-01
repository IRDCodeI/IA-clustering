import matplotlib.pyplot as plt
import matplotlib as mlt
from sklearn.decomposition import PCA
from nlp import nlpdocument
import json

def mds(file):
    mds = nlpdocument(file)
    pca = PCA(n_components=2)
    pca.fit_transform(mds)

    axis = pca.components_.T

    data = {
        "x": axis[:,0].tolist(),
        "y": axis[:,1].tolist(),
        "dots": axis.tolist()
    }

    return json.dumps(data, indent = 4) 