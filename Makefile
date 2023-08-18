up:
	kubectl create secret generic app-secrets --from-env-file=.env-prod
	kubectl apply -f ./kubernetes/app-k8s.yaml
	kubectl apply -f ./kubernetes/celery-k8s.yaml
	kubectl apply -f ./kubernetes/flower-k8s.yaml
	kubectl apply -f ./kubernetes/postgres-k8s.yaml
	kubectl apply -f ./kubernetes/redis-k8s.yaml
down:
	kubectl delete -f ./kubernetes/app-k8s.yaml
	kubectl delete -f ./kubernetes/celery-k8s.yaml
	kubectl delete -f ./kubernetes/flower-k8s.yaml
	kubectl delete -f ./kubernetes/postgres-k8s.yaml
	kubectl delete -f ./kubernetes/redis-k8s.yaml
	kubectl delete secret app-secrets