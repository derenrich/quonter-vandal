Quonter Vandal
--------------


Run dev server
```
poetry run uvicorn quonter_vandal.server:app
```

To reboot
```
webservice stop && webservice start
```

To investigate

```
kubectl get pods
kubectl exec --stdin --tty qop-746cb8c766-dd5k4 -- /bin/bash
```