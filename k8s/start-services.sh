#!/bin/bash

# Script to start microservices, MongoDB, and Pulsar cluster
# This script scales up deployments and statefulsets to their original replica count

echo "🚀 Starting AlpesPartners microservices, MongoDB, and Pulsar cluster..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed or not in PATH"
    exit 1
fi

# Check if we can connect to the cluster
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig."
    exit 1
fi

echo "📊 Current deployment status:"
kubectl get deployments -o wide
echo ""
echo "📊 Current Pulsar status:"
kubectl get pods -n pulsar

echo ""
echo "� Starting Pulsar cluster first..."

# Scale up Pulsar core components in the right order
echo "  - Starting ZooKeeper..."
kubectl scale statefulset pulsar-mini-zookeeper -n pulsar --replicas=1

echo "  - Waiting for ZooKeeper to be ready..."
kubectl wait --for=condition=ready pod -l component=zookeeper -n pulsar --timeout=300s || echo "    ZooKeeper timeout, continuing..."

echo "  - Starting BookKeeper..."
kubectl scale statefulset pulsar-mini-bookie -n pulsar --replicas=1

echo "  - Waiting for BookKeeper to be ready..."
kubectl wait --for=condition=ready pod -l component=bookkeeper -n pulsar --timeout=300s || echo "    BookKeeper timeout, continuing..."

echo "  - Starting Broker..."
kubectl scale statefulset pulsar-mini-broker -n pulsar --replicas=1

echo "  - Waiting for Broker to be ready..."
kubectl wait --for=condition=ready pod -l component=broker -n pulsar --timeout=300s || echo "    Broker timeout, continuing..."

echo "  - Starting Proxy..."
kubectl scale statefulset pulsar-mini-proxy -n pulsar --replicas=1

echo "  - Starting Toolset..."
kubectl scale statefulset pulsar-mini-toolset -n pulsar --replicas=1

echo "  - Starting Pulsar Manager..."
kubectl scale statefulset pulsar-mini-pulsar-manager -n pulsar --replicas=1

echo "  - Starting monitoring components..."
# kubectl scale deployment pulsar-mini-grafana -n pulsar --replicas=1
# kubectl scale deployment pulsar-mini-victoria-metrics-operator -n pulsar --replicas=1
# kubectl scale deployment vmagent-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=1
# kubectl scale deployment vmsingle-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=1
# kubectl scale deployment pulsar-mini-kube-state-metrics -n pulsar --replicas=1

echo ""
echo "🔼 Starting MongoDB..."

# Scale up MongoDB (microservices depend on it)
echo "  - Scaling up mongodb..."
kubectl scale deployment mongodb --replicas=1

echo "  - Waiting for MongoDB to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/mongodb

echo ""
echo "🔼 Starting microservices..."

# # Scale up marketing service
# echo "  - Scaling up marketing-service..."
# kubectl scale deployment marketing-service --replicas=1

# # Scale up tracking service
# echo "  - Scaling up tracking-service..."
# kubectl scale deployment tracking-service --replicas=1

# # Scale up atribucion service
# echo "  - Scaling up atribucion-service..."
# kubectl scale deployment atribucion-service --replicas=1

# # Scale up comisiones service
# echo "  - Scaling up comisiones-service..."
# kubectl scale deployment comisiones-service --replicas=1

# echo ""
# echo "⏳ Waiting for all microservices to be ready..."
# kubectl wait --for=condition=available --timeout=300s deployment/marketing-service
# kubectl wait --for=condition=available --timeout=300s deployment/tracking-service
# kubectl wait --for=condition=available --timeout=300s deployment/atribucion-service
# kubectl wait --for=condition=available --timeout=300s deployment/comisiones-service

# echo ""
# echo "📊 Final status:"
# echo "Microservices:"
# kubectl get deployments -o wide
# echo ""
# echo "Pulsar cluster:"
# kubectl get pods -n pulsar

# echo ""
# echo "✅ All services and Pulsar cluster are now running!"
# echo "🌐 Your microservices should be accessible again."
