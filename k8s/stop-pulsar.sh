#!/bin/bash
# Script to stop Pulsar cluster by scaling components down to 0

echo "🛑 Stopping Pulsar cluster to save costs..."

# Scale down all components to 0 replicas
echo "Stopping core components..."
kubectl scale statefulset pulsar-mini-zookeeper -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-bookie -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-broker -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-proxy -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-toolset -n pulsar --replicas=0
kubectl scale statefulset pulsar-mini-pulsar-manager -n pulsar --replicas=0

echo "Stopping monitoring components..."
kubectl scale deployment pulsar-mini-grafana -n pulsar --replicas=0
kubectl scale deployment pulsar-mini-victoria-metrics-operator -n pulsar --replicas=0
kubectl scale deployment vmagent-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=0
kubectl scale deployment vmsingle-pulsar-mini-victoria-metrics-k8s-stack -n pulsar --replicas=0
kubectl scale deployment pulsar-mini-kube-state-metrics -n pulsar --replicas=0

echo "✅ Pulsar cluster stopped!"
echo "Check status with: kubectl get pods -n pulsar"
