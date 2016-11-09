env=""

production:
	terraform plan -var-file="secrets.tfvars" -var-file="production.tfvars" -state="production.tfstate"

production-destroy:
	terraform destroy -var-file="secrets.tfvars" -var-file="production.tfvars" -state="production.tfstate"

production-apply:
	terraform apply -var-file="secrets.tfvars" -var-file="production.tfvars" -state="production.tfstate"

.PHONY: production production-destroy production-apply
