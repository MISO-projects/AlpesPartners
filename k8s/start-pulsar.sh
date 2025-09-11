#!/bin/bash
# Script to restart Pulsar cluster by scaling components back up

echo "🚀 Starting Pulsar cluster..."

# Scale up core components in the right order
echo "Starting ZooKeeper..."
kubectl scale statefulset pulsar-mini-zookeeper -n pulsar --replicas=1

echo "Waiting for ZooKeeper to be ready..."
kubectl wait --for=condition=ready pod -l component=zookeeper -n pulsar --timeout=300s

echo "Starting BookKeeper..."
kubectl scale statefulset pulsar-mini-bookie -n pulsar --replicas=1

echo "Waiting for BookKeeper to be ready..."
kubectl wait --for=condition=ready pod -l component=bookkeeper -n pulsar --timeout=300s

echo "Starting Broker..."
kubectl scale statefulset pulsar-mini-broker -n pulsar --replicas=1

echo "Waiting for Broker to be ready..."
kubectl wait --for=condition=ready pod -l component=broker -n pulsar --timeout=300s

echo "Starting Proxy..."
kubectl scale statefulset pulsar-mini-proxy -n pulsar --replicas=1

echo "Starting Toolset..."
kubectl scale statefulset pulsar-mini-toolset -n pulsar --replicas=1

echo "Starting Pulsar Manager..."
kubectl scale statefulset pulsar-mini-pulsar-manager -n pulsar --replicas=1

# Scale up monitoring components
echo "Starting monitoring components..."
kubectl scale deployment pulsar-mini-grafana -n pulsar --replicas=1
kubectl scale deployment pulsar-mini-victoria-metrics-operator -n pulsar --replicas=1
kubectl scale deployment vmagent-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=1
kubectl scale deployment vmsingle-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=1
kubectl scale deployment pulsar-mini-kube-state-metrics -n pulsar --replicas=1

echo "✅ Pulsar cluster startup initiated!"
echo "Check status with: kubectl get pods -n pulsar"
