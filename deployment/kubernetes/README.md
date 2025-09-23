# Kubernetes Deployment Code 
1️⃣ Build & Push Docker Images
# Build Streamlit images
docker image build -t jaylaksh94/streamlit:v1 .
docker image build -t jaylaksh94/streamlit:v2 .
docker image build -t jaylaksh94/streamlit:v4 .
docker image build -t jaylaksh94/streamlit:v5 .

# Push Streamlit images
docker image push jaylaksh94/streamlit:v1
docker image push jaylaksh94/streamlit:v2
docker image push jaylaksh94/streamlit:v4
docker image push jaylaksh94/streamlit:v5

# Build Model API image
docker image build -t jaylaksh94/house-pricemodel:latest .

# Push Model API image
docker image push jaylaksh94/house-pricemodel:latest

2️⃣ Deploy Streamlit on Kubernetes
# Create Streamlit deployment (v1 image)
kubectl create deployment streamlit --image=jaylaksh94/streamlit:v1 --port=8501  

# Expose Streamlit via NodePort service
kubectl create service nodeport streamlit --tcp=8501 --node-port=30000  

3️⃣ Deploy Model API on Kubernetes
# Deployment
kubectl create deployment model --image=jaylaksh94/house-pricemodel:latest --port=8000 --replicas=2  

# Expose Model API via NodePort
kubectl create service nodeport model --tcp=8000 --node-port=30100  

4️⃣ Scale Deployments
# Scale Streamlit replicas
kubectl scale deploy streamlit --replicas=4
kubectl scale deploy streamlit --replicas=8

# Scale Model API replicas
kubectl scale deploy model --replicas=1
kubectl scale deploy model --replicas=3

5️⃣ Update Streamlit Deployment & Rollout
# Update Streamlit deployment with new images
kubectl set image deploy streamlit streamlit=jaylaksh94/streamlit:v2   
kubectl set image deploy streamlit streamlit=jaylaksh94/streamlit:v5  

# Check rollout status
kubectl rollout status deployment streamlit  

6️⃣ Useful Commands
# Get pods, services, deployments, replicasets
kubectl get pods
kubectl get all

# Describe deployments
kubectl describe deployment streamlit
kubectl describe deployment model

# Watch resources (if 'watch' is installed)
watch kubectl get all  

# Export command history
history > my_commands.txt  

# command won’t actually create the service, but instead prints the YAML spec you could apply.
kubectl create service nodeport model --tcp=8000 --node-port=30100 --dry-run=client -o yaml


7️⃣ Deployment Architecture
flowchart TD
    User([User Browser])
    User -->|Access via NodePort 30000| StreamlitService[Streamlit Service (NodePort:30000)]
    StreamlitService --> StreamlitPods[Streamlit Pods]

    StreamlitPods -->|API Call on NodePort 30100| ModelService[Model Service (NodePort:30100)]
    ModelService --> ModelPods[Model API Pods]

    subgraph Kubernetes Cluster
        StreamlitService
        StreamlitPods
        ModelService
        ModelPods
    end


📌 Explanation:
- User accesses Streamlit at NodePort 30000.
- Streamlit calls the Model API at NodePort 30100.
- Both services run inside the Kubernetes cluster with their own deployments + replicas.
- deployment.apps/streamlit 8/8 → means 8 replica pods of Streamlit are running.
- deployment.apps/model 2/2 → means 2 replica pods of Model API are running.


---

## Declarative Deployment with YAML
Instead of creating resources directly from CLI, we can generate YAML manifests using `--dry-run=client -o yaml`.  
This allows us to store configs in GitHub and apply them any time for reproducible deployments.

### Generated YAML files
- **model-deploy.yaml** → Deployment for `jaylaksh94/house-pricemodel:latest` (2 replicas, port 8000)  
- **model-service.yaml** → NodePort Service exposing Model API on `30100 → 8000`  
- **streamlit-deploy.yaml** → Deployment for `jaylaksh94/streamlit:v5` (2 replicas, port 8501)  
- **streamlit-service.yaml** → NodePort Service exposing Streamlit app on `30000 → 8501`

### Commands used
```bash
kubectl create service nodeport model --tcp=8000 --node-port=30100 \
  --dry-run=client -o yaml > model-service.yaml

kubectl create deployment model --image=jaylaksh94/house-pricemodel:latest \
  --port=8000 --replicas=2 --dry-run=client -o yaml > model-deploy.yaml

kubectl create deployment streamlit --image=jaylaksh94/streamlit:v5 \
  --port=8501 --replicas=2 --dry-run=client -o yaml > streamlit-deploy.yaml

kubectl create service nodeport streamlit --tcp=8501 --node-port=30000 \
  --dry-run=client -o yaml > streamlit-service.yaml
```

### Apply manifests
```bash
- kubectl apply -f model-deploy.yaml
- kubectl apply -f model-service.yaml
- kubectl apply -f streamlit-deploy.yaml
- kubectl apply -f streamlit-service.yaml
```
## Verfy
```bash
- kubectl get deployments
- kubectl get pods
- kubectl get svc
```


## Updating Model Deployment

There are two common ways to update or refresh the model deployment:

### 1. Update the image explicitly
Use this when you build and push a new image version (with a different tag).
```bash
kubectl set image deployment/model house-pricemodel=jaylaksh94/house-pricemodel:latest
```

- deployment/model → deployment name
- house-pricemodel → container name inside the deployment
- jaylaksh94/house-pricemodel:latest → new image
- This triggers a rollout only if the image tag differs.

### 2. Restart the deployment
- Use this when you push a new image with the same tag (e.g., latest) and want pods to redeploy.

```bash
kubectl rollout restart deployment model
```
- This forces Kubernetes to kill existing pods and start new ones, pulling the same image tag again