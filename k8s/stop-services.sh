#!/bin/bash

# Script to stop microservices, MongoDB, and Pulsar to reduce costs
# This script scales down deployments and statefulsets to 0 replicas

echo "🛑 Stopping AlpesPartners microservices, MongoDB, and Pulsar cluster..."

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
echo "🔽 Scaling down microservices..."

# Scale down marketing service
echo "  - Scaling down marketing-service..."
kubectl scale deployment marketing-service --replicas=0

# Scale down tracking service
echo "  - Scaling down tracking-service..."
kubectl scale deployment tracking-service --replicas=0

# Scale down atribucion service
echo "  - Scaling down atribucion-service..."
kubectl scale deployment atribucion-service --replicas=0

# Scale down comisiones service
echo "  - Scaling down comisiones-service..."
kubectl scale deployment comisiones-service --replicas=0

# Scale down MongoDB
echo "  - Scaling down mongodb..."
kubectl scale deployment mongodb --replicas=0

echo ""
echo "🔽 Scaling down Pulsar cluster..."

# Stop Pulsar core components
echo "  - Stopping Pulsar core components..."
kubectl scale statefulset pulsar-mini-zookeeper -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-bookie -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-broker -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-proxy -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-toolset -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-pulsar-manager -n pulsar --replicas=0

echo "  - Stopping Pulsar monitoring components..."
kubectl scale deployment pulsar-mini-grafana -n pulsar --replicas=0
kubectl scale deployment pulsar-mini-victoria-metrics-operator -n pulsar --replicas=0
kubectl scale deployment vmagent-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=0
kubectl scale deployment vmsingle-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=0
kubectl scale deployment pulsar-mini-kube-state-metrics -n pulsar --replicas=0

echo ""
echo "⏳ Waiting for pods to terminate..."
sleep 10

echo ""
echo "📊 Final status:"
echo "Microservices:"
kubectl get deployments -o wide
echo ""
echo "Pulsar cluster:"
kubectl get pods -n pulsar

echo ""
echo "✅ All services and Pulsar cluster have been scaled down to 0 replicas."
echo "💡 To restart services, run: ./start-services.sh"
echo "💰 This should significantly reduce your cluster costs!"
