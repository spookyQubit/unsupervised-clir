## Resources
```
    * Unsupervised Cross-Lingual Information Retrieval using Monolingual Data Only
    * Cross-lingual Learning-to-Rank with Shared Representations
```

## Download data/embeddings

```
    * ./download_unzip.sh  -s "madata.bib.uni-mannheim.de/273/1/UnsupCLIREmbeddings.tar.gz"
    * ./download_unzip.sh  -s "www.cs.jhu.edu/~kevinduh/a/wikiclir2018/sasaki18.tgz" -d Data
```

## Download embeddings
```
Embeddings can be gotten from:
    * wget "https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi.en.vec"
    * wget "https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi.fr.vec"
```

## Steps
```
docker build -t shan/python-echo:1.0 .
docker rmi $(docker images -q  --filter "dangling=true")
docker ps -a 
docker rm unsupervised-clir_app_1 
docker rmi $(docker images -q  --filter "dangling=true")
docker-compose up 
docker attach unsupervised-clir_app_1 
```
