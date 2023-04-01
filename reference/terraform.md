# Terraform Reference
----

# General Commands
Run the following in a directory containing a single terraform configuration (main.tf and variables.tf)

```bash
# initialize your work directory by downloading the necessary providers/plugins.
terraform init
# formats your configuration files so that the format is consistent.
terraform fmt
# returns a success message if the configuration is valid and no errors are apparent.
terraform validate
# creates a preview of the changes to be applied against a remote state, allowing you to review the changes before applying them.
terraform plan
# applies the changes to the infrastructure
terraform apply
# removes your stack from the infrastructure.
terraform destroy
```

# Execution Steps
```bash
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"

# Delete infra after your work, to avoid costs on any running services
terraform destroy
```