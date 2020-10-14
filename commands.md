[vault minikube installation](
    https://github.com/avielb/advanced-devops/blob/master/devsecops/vault/00.chart_installation.txt
)
# port forward vault:
```
$ kubectl port-forward vault-0 8200:8200
```
output: (local keys' no vulnerabilities since minikube isn't exposed)
Unseal Key 1: uFfTY0JLvLceK5bDbECRNwm9qY5CbLGNBIqMvjYPovrZ
Unseal Key 2: HIom/f9+VoCZk0cvTLOUU17fxY+qyTmqweBcBjU8ily8
Unseal Key 3: VfLSMkR111A3qy5w6UmGoLy3UmlYAQBJ842S7rsXhxU4
Unseal Key 4: B/wJC/6eFC7xoqVv3lUdjyIJLu92emYGbI6s/GJbmZi5
Unseal Key 5: GftYSTvL++4y8kTwP8XEROFj2xLYJVI1aVxNHSvWM+fD
Initial Root Token: s.A946lZFDo7WOrX9v39d5Gf6h
- - - 
use vault cli: 
```
$ export VAULT_ADDR="http://127.0.0.1:8200"
$ vault login
```

..
(created db secrets via ui)
```
$ vault secrets list -detailed
$ vault kv get kv/db
$ vault kv get -field=dbpwd kv/db 
```
- - -
