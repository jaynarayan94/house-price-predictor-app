# 🚀 Kubernetes Deployment Guide
This doc covers building images, running a local cluster, deploying Streamlit + Model API, scaling, rollouts, and troubleshooting.
---

## Prerequisites
- **Docker Desktop:**  
  Install and run (Mac/Windows: launch it, Linux: `sudo systemctl start docker`).

- **kind:**  
  [Install kind](https://kind.sigs.k8s.io/) (e.g., `brew install kind` on Mac).

- **kubectl:**  
  [Install kubectl](https://kubernetes.io/docs/tasks/tools/) (e.g., `brew install kubectl` on Mac).

---

## 1. Start Docker

- **Mac/Windows:** Open Docker Desktop  
- **Linux:**  
sudo systemctl start docker

---

## 2. Start Kubernetes Cluster

kind create cluster

---

## 3. Build & Push Docker Images

- Streamlit
```bash
docker build -t jaylaksh94/streamlit:v1 .
docker push jaylaksh94/streamlit:v1
````
- Model
```bash
docker build -t jaylaksh94/house-pricemodel:latest .
docker push jaylaksh94/house-pricemodel:latest
```
---

## 4. Deploy Everything
```bash
kubectl apply -f streamlit-deploy.yaml
kubectl apply -f streamlit-service.yaml
kubectl apply -f model-deploy.yaml

- Or, if all in a dir:  
kubectl apply -f deployment/kubernetes/
```
---

## 5. Status & Useful Commands
```bash
kubectl get all
kubectl get pods
kubectl get svc
```

---

## 6. Scaling Deployments
```bash
kubectl scale deploy streamlit --replicas=4
kubectl scale deploy model --replicas=3
```
---

## 7. Updates/Rollouts
- Update to a new image tag:
```bash
kubectl set image deployment/model house-pricemodel=jaylaksh94/house-pricemodel:latest
kubectl set image deployment/streamlit streamlit=jaylaksh94/streamlit:v5
```
- Restart (when reusing the same tag for a new image):
```bash
kubectl rollout restart deployment model
kubectl rollout restart deployment streamlit
```
---

## 8. Debugging
```bash
kubectl describe deployment model
kubectl describe deployment streamlit
```

**Common fixes:**  
- If connection errors occur, restart Docker, ensure cluster is running with `kind create cluster`, and check `kubectl cluster-info`.

---

## 9. Generate YAML for Source Control
```bash
kubectl create deployment model --image=jaylaksh94/house-pricemodel:latest --port=8000 --replicas=2 --dry-run=client -o yaml > model-deploy.yaml
kubectl create service nodeport model --tcp=8000 --node-port=30100 --dry-run=client -o yaml > model-service.yaml
kubectl create deployment streamlit --image=jaylaksh94/streamlit:v5 --port=8501 --replicas=2 --dry-run=client -o yaml > streamlit-deploy.yaml
kubectl create service nodeport streamlit --tcp=8501 --node-port=30000 --dry-run=client -o yaml > streamlit-service.yaml
```
---


---
## Full Flow
1. Start Docker & cluster
2. Build and push all images
3. Apply manifests
4. Verify with `kubectl get all`
5. Scale or update as needed

**Commit all .yaml files and this guide for team onboarding and reproducibility.**
