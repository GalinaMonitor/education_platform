kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl patch storageclass local-path -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
helm upgrade --install --wait vault-operator oci://ghcr.io/bank-vaults/helm-charts/vault-operator
kubectl kustomize https://github.com/bank-vaults/vault-operator/deploy/rbac | kubectl apply -f -
kubectl apply -f vault.yml
export VAULT_ADDR=https://127.0.0.1:8200
kubectl get secret vault-tls -o jsonpath="{.data.ca\.crt}" | base64 --decode > $PWD/vault-ca.crt
export VAULT_CACERT=$PWD/vault-ca.crt
kubectl create namespace vault-infra
kubectl label namespace vault-infra name=vault-infra
helm upgrade --install --wait vault-secrets-webhook oci://ghcr.io/bank-vaults/helm-charts/vault-secrets-webhook --namespace vault-infra
