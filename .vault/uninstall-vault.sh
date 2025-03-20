helm uninstall vault-secrets-webhook
kubectl delete namespace vault-infra
kubectl delete -f vault.yml
kubectl kustomize https://github.com/bank-vaults/vault-operator/deploy/rbac | kubectl delete -f -
helm uninstall vault-operator
