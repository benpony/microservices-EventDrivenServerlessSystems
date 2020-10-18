[openfaas minikube installation](
    https://github.com/avielb/advanced-devops/blob/master/serverless/openfaas/installation.txt
)
# port forward openfaas:
```
$ kubectl port-forward svc/gateway -n openfaas 8080:8080
```

#deploy func
```
$ docker pull functions/alpine:latest
$ faas-cli template pull
$ faas-cli deploy -f faas-word-counter.yaml
```

#output
    ..
    Deployed. 202 Accepted.
    URL: http://127.0.0.1:8080/function/word-counter.openfaas-fn

#test func
```
$ curl --location --header 'Content-Type: text/plain' --data-raw 'pony' \
       --request GET 'http://127.0.0.1:8080/function/word-counter.openfaas-fn' 
```


