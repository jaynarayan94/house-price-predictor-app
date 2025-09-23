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

## Scale Model API replicas
kubectl scale deploy model --replicas=1
kubectl scale deploy model --replicas=3

5️⃣ Update Streamlit & Model Deployment & Rollout
# Update Streamlit deployment with new images
kubectl set image deploy streamlit streamlit=jaylaksh94/streamlit:v2   
kubectl set image deploy streamlit streamlit=jaylaksh94/streamlit:v5  

kubectl set image deployment model house-pricemodel=jaylaksh94/house-pricemodel:latest


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