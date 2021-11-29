# Health Notification for AWS

AWS Health Event monitor and dispatch demo

1. first, run the `webhook`
2. run the deploy script

if you need test phone call alarm, you must deploy the dependences as `webhook` README

# webhook

This is the demo webhook handler for any SNS notification, more infomation plase check `webhook` README.md

# global-sns

This is the deploy/cleanup scripts for health API. because health event is regional services, we need to add it in every region.

More infomation plase check `global-sns` README.md


