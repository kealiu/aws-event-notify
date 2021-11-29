# dependences

1. `aws` cli
2. permissions for cloudformation, sns, health, ec2

# deploy.sh

run with `deploy.sh <deploy-name> <http-webhook-endpoint>`, it will deploy the `HealthEvent.yaml` in all opened aws regions.

after completed, a `xxxx-stackid.log` will record all the stack ids.

# cleanup.sh

just run `./cleanup.sh <stackid.log>`, it will call `aws` cli to delete all the cloudformation stacks.
