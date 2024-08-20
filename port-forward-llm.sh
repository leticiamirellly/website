while true; do
  echo "Iniciando kubectl port-forward..."
  kubectl port-forward svc/llm-srv 4001:4001
  echo "kubectl port-forward parou. Reiniciando em 2 segundos..."
  sleep 2
done