Flask + MongoDB on Kubernetes (Minikube)
Project Overview
This project demonstrates deploying a Python Flask application connected to MongoDB on a Kubernetes cluster using Minikube. It covers containerization, persistent storage, autoscaling, service discovery, and resource management.
Key Components
• Flask REST API with / and /data endpoints
• MongoDB with authentication
• Dockerized Flask application
• Kubernetes Deployment, StatefulSet, Services, HPA
• Persistent Volumes for MongoDB
Dockerfile
Uses python:3.9-slim base image, installs dependencies, and runs the Flask application.
Kubernetes Deployment
Flask is deployed using a Deployment with 2 replicas and resource limits.
MongoDB Setup
MongoDB is deployed as a StatefulSet with persistent storage and authentication enabled.
DNS Resolution
Flask connects to MongoDB using Kubernetes service DNS (mongodb:27017).
Resource Management
Requests and limits ensure fair scheduling and stable cluster performance.
Autoscaling
HPA scales Flask pods based on CPU usage beyond 70%.
Testing
Data insertion and retrieval verified via REST API. Autoscaling tested using load generator.


Kubernetes provides built-in DNS-based service discovery that allows pods to communicate with each other without using hardcoded IP addresses.
?? How DNS Works in This Project
* Every Kubernetes Service is assigned a DNS name
* DNS format:
* <service-name>.<namespace>.svc.cluster.local
* In this project:
o MongoDB Service name: mongodb
o Namespace: default
o Full DNS name:
o mongodb.default.svc.cluster.local
?? Flask ? MongoDB Communication Flow
1. Flask pod tries to connect to MongoDB using:
2. mongodb:27017
3. Kubernetes DNS (CoreDNS) resolves mongodb to the MongoDB Service IP
4. The Service forwards traffic to the MongoDB pod
5. If the MongoDB pod restarts, DNS automatically resolves the new IP
Design Choices & Justification
?? MongoDB as StatefulSet
Chosen because:
* Requires persistent storage
* Needs stable network identity
* Supports Persistent Volume Claims (PVC)
Alternative Considered: Deployment
Rejected because: Deployments do not guarantee stable storage or pod identity.

?? ClusterIP Service for MongoDB
Chosen because:
* MongoDB should be accessible only inside the cluster
* Improves security
Alternative Considered: NodePort
Rejected because: Exposes database externally (security risk).

?? NodePort Service for Flask
Chosen because:
* Simple external access in Minikube
* Easy testing via browser or curl
Alternative Considered: Ingress
Rejected because: Overkill for local Minikube setup.

?? Horizontal Pod Autoscaler (HPA)
Chosen because:
* Automatically scales based on CPU usage
* Efficient resource utilization
Alternative Considered: Manual scaling
Rejected because: Not dynamic or efficient.




Cookie Point – Testing Scenarios
?? Database Interaction Testing
Steps Performed
1. Sent POST request to /data endpoint
2. Retrieved data using GET /data
3. Restarted MongoDB pod
4. Verified data persistence
Result
* Data successfully stored and retrieved
* Data persisted even after pod restart (PVC working)

?? Autoscaling Testing (High Traffic Simulation)
Load Generation
Terminal:
 kubectl run -i --tty load --image=busybox – sh
sh:
while true; do wget -q -O- http://flask-service:5000; done



Author: Rohit Shah
