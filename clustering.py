import numpy as np
import pandas as pd
import random
import json
from nlp import nlpdocument
from database import connection as db
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import silhouette_score
from database import r

cursor = db.cursor()

def clustering(ai, clusters = 1, **kwargs):

    sql = f"SELECT * FROM ai_abstract WHERE model = '%s';" %(ai)
    res = cursor.execute(sql)

    if(res != 0):        

        data = cursor.fetchall()
        dataset = pd.DataFrame(data, columns=["id","title","abstract", "abstract_generate", "model"])

        abstracts_original = nlpdocument(dataset[["abstract"]]).transpose()
        abstracts_generate = nlpdocument(dataset[["abstract_generate"]]).transpose()

        pcaO = PCA(n_components= 2)
        pcaO.fit_transform(abstracts_original)

        pcaG = PCA(n_components= 2)
        pcaG.fit_transform(abstracts_generate)

        points_original = pcaO.components_.T.round(3)
        points_generate = pcaG.components_.T.round(3)

        for arg in kwargs.items():
            if arg[0] == "algorithm" and arg[1] == "kmeans":
                kM = KMeans(n_clusters= clusters, init="random", n_init="auto").fit(np.array(points_original, dtype= object))            
                labels_original = kM.labels_
                centroids_original = kM.cluster_centers_ #TODO >> Plot in the web system

                kM = KMeans(n_clusters= clusters, init="random", n_init="auto").fit(np.array(points_generate, dtype= object))            
                labels_generate = kM.labels_
                centroids_generate = kM.cluster_centers_ #TODO >> Plot in the web system

                datasets_aO = []
                datasets_aG = []
                key = ["x", "y"]                

                for label in set(labels_original):

                    datasets_aO.append({
                        "label": f"Group {label+1}",
                        "data": [dict(zip(key, p)) for p in points_original[[i for i,l in enumerate(labels_original) if l == label]].tolist()],
                        "backgroundColor": f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},0.5)'
                    })      

                for label in set(labels_generate):

                    datasets_aG.append({
                        "label": f"Group {label+1}",
                        "data": [dict(zip(key, p)) for p in points_generate[[i for i,l in enumerate(labels_generate) if l == label]].tolist()],
                        "backgroundColor": f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},0.5)'
                    })    

                dfO = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_original, dtype=object)], axis=1 , ignore_index = True)
                dfO = dfO.assign(Model = "chatgpt")
                dfO.columns = ["title", "label", "model"]                

                dfG = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_generate, dtype=object)], axis=1 , ignore_index = True)
                dfG = dfG.assign(Model = "chatgpt")
                dfG.columns = ["title", "label", "model"]

                label_kmeans = {
                    "original": dfO["label"].values.tolist(),
                    "generate": dfG["label"].values.tolist()
                }

                rval = json.dumps(label_kmeans)    

                r.set('label_kmeans', rval)

                #r.hset('kmeans_abstract_g', zlib.compress(pickle.dumps(dfG)))

                return {"datasets_aO": datasets_aO, "datasets_aG": datasets_aG}
            
            elif arg[0] == "algorithm" and arg[1] == "dhc":                
                aC = AgglomerativeClustering(distance_threshold= None, n_clusters= clusters, linkage="complete").fit(np.array(points_original, dtype= object))
                labels_original = aC.labels_

                aC = AgglomerativeClustering(distance_threshold= None, n_clusters= clusters, linkage="complete").fit(np.array(points_generate, dtype= object))
                labels_generate = aC.labels_

                datasets_aO = []
                datasets_aG = []
                key = ["x", "y"]

                for label in set(labels_original):
                    datasets_aO.append({
                        "label": f"Group {label+1}",
                        "data": [dict(zip(key, p)) for p in points_original[[i for i,l in enumerate(labels_original) if l == label]].tolist()],
                        "backgroundColor": f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},0.5)'
                    })      

                for label in set(labels_generate):
                    datasets_aG.append({
                        "label": f"Group {label+1}",
                        "data": [dict(zip(key, p)) for p in points_generate[[i for i,l in enumerate(labels_generate) if l == label]].tolist()],
                        "backgroundColor": f'rgba({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)},0.5)'
                    })                     

                label_dhc = {
                    "original": labels_original.tolist(),
                    "generate": labels_generate.tolist()
                }                            

                rval = json.dumps(label_dhc)    

                r.set('label_dhc', rval)

                return {"datasets_aO": datasets_aO, "datasets_aG": datasets_aG}                                  

            else:
                print("No selected Model")
    else:
        print("No data on database")

def labels_cluster(abstract, ai, clusters, **kwargs):
    sql = f"SELECT * FROM ai_abstract WHERE model = '%s';" %(ai)
    res = cursor.execute(sql)

    if(res != 0):        

        data = cursor.fetchall()
        dataset = pd.DataFrame(data, columns=["id","title","abstract", "abstract_generate", "model"])

        abstracts_original = nlpdocument(dataset[["abstract"]]).transpose()
        abstracts_generate = nlpdocument(dataset[["abstract_generate"]]).transpose()

        pcaO = PCA(n_components= 2)
        pcaO.fit_transform(abstracts_original)

        pcaG = PCA(n_components= 2)
        pcaG.fit_transform(abstracts_generate)

        points_original = pcaO.components_.T.round(3)
        points_generate = pcaG.components_.T.round(3)

        for arg in kwargs.items():
            if arg[0] == "algorithm" and arg[1] == "kmeans":
                kM = KMeans(n_clusters= clusters, init="random", n_init="auto").fit(np.array(points_original, dtype= object))            
                labels_original = kM.labels_
                centroids_original = kM.cluster_centers_ #TODO >> Plot in the web system

                kM = KMeans(n_clusters= clusters, init="random", n_init="auto").fit(np.array(points_generate, dtype= object))            
                labels_generate = kM.labels_
                centroids_generate = kM.cluster_centers_ #TODO >> Plot in the web system

                datasets_aO = []
                datasets_aG = []             

                dfO = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_original, dtype=object)], axis=1 , ignore_index = True)
                dfO = dfO.assign(Model = "chatgpt")
                dfO.columns = ["title", "label", "model"]                

                dfG = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_generate, dtype=object)], axis=1 , ignore_index = True)
                dfG = dfG.assign(Model = "chatgpt")
                dfG.columns = ["title", "label", "model"]  
                                
                if (abstract == "original"):
                    return dfO[["title","label"]].to_dict("records")
                    #return {"title": dfO["title"].to_list(), "labels": dfO["label"].to_list()} 
                elif (abstract == "generate"):
                    return dfG[["title","label"]].to_dict("records")            
            
            elif arg[0] == "algorithm" and arg[1] == "dhc":                
                aC = AgglomerativeClustering(distance_threshold= None, n_clusters= clusters, linkage="complete").fit(np.array(points_original, dtype= object))
                labels_original = aC.labels_

                aC = AgglomerativeClustering(distance_threshold= None, n_clusters= clusters, linkage="complete").fit(np.array(points_generate, dtype= object))
                labels_generate = aC.labels_

                datasets_aO = []
                datasets_aG = []                        

                dfO = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_original, dtype=object)], axis=1 , ignore_index = True)
                dfO = dfO.assign(Model = "chatgpt")
                dfO.columns = ["title", "label", "model"]                

                dfG = pd.concat([pd.DataFrame(dataset["title"]), pd.DataFrame(labels_generate, dtype=object)], axis=1 , ignore_index = True)
                dfG = dfG.assign(Model = "chatgpt")
                dfG.columns = ["title", "label", "model"]               

                if (abstract == "original"):
                    return dfO[["title","label"]].to_dict("records")
                elif (abstract == "generate"):
                    return dfG[["title","label"]].to_dict("records")

            else:
                print("No selected Model")
    else:
        print("No data on database")

def validation_cluster(ai ,n ,cluster):

    sql = f"SELECT * FROM ai_abstract WHERE model = '%s';" %(ai)
    res = cursor.execute(sql)
    data = cursor.fetchall()
    dataset = pd.DataFrame(data, columns=["id","title","abstract", "abstract_generate", "model"])
    silhouette_df = nlpdocument(dataset[["abstract_generate"]])

    if(res != 0):
        if cluster == "kmeans":

            labels = json.loads(r.get('label_kmeans'))
            l_original = labels["original"]
            l_generate = labels["generate"]
                    
            sls = silhouette_score(silhouette_df, l_generate)
            ars = adjusted_rand_score(l_original, l_generate)

            return {"ars": round(float(ars), 3), "sls": round(float(sls), 3)}
        
        elif cluster == "dhc":
            labels = json.loads(r.get('label_dhc'))
            l_original = labels["original"]
            l_generate = labels["generate"]

            sls = silhouette_score(silhouette_df, l_generate)
            ars = adjusted_rand_score(l_original, l_generate)
            
            return {"ars": round(float(ars), 3), "sls": round(float(sls), 3)}
    