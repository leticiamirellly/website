while true; do
  echo "Iniciando kubectl port-forward..."
  kubectl port-forward svc/medium-srv 8080:4000
  echo "kubectl port-forward parou. Reiniciando em 2 segundos..."
  sleep 2
done