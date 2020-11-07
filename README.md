# Kubernetes config map cleaner

Goal : clean unused config map 
For instance, each time you update your configmap in Kusomize, a new configmap name is generated ending with a sha based on content.

## Run

```
git clone --recursive https://github.com/saugereau/kubernetes-configmap-cleaner.git
cd kubernetes-configmap-cleaner
pipenv install

python main.py -h
   
usage: main.py [-h] [--r RETENTION] [--n NAMESPACE]

Process some integers.

optional arguments:
  -h, --help     show this help message and exit
  --r RETENTION  an integer for the retention
  --n NAMESPACE  namespace
```



