#!/bin/bash

# $1 stackname
# $2 webhook
# $3 yaml file (optional), default = HealthEvent.yaml

stackname=$1
webhook=$2
cfyaml=$3

if [ -z "${stackname}" ] || [ -z "${webhook}" ] ; then
    echo "usage $0 <stackname> <webhook> [HealthEvent.yaml]"
    exit -1
fi

if [ -z "${cfyaml}" ] ; then
    cfyaml="HealthEvent.yaml"
fi

if ! command -v jq &> /dev/null
then
    echo "`jq` could not be found, please install it"
    exit
fi

if ! command -v aws &> /dev/null
then
    echo "`aws` cli could not be found, please install it"
    exit
fi

tempnamegen=$(mktemp -u -t ${stackname}XXXXXXXX)
tempname=$(basename ${tempnamegen,,})
tempbucket=sns-temp-cf-bucket-${tempname}
cfyamlUrl=http://${tempbucket}.s3.amazonaws.com/${cfyaml}
stackidlog=${tempname}-stackid.log

echo > ${stackidlog}
aws s3 mb s3://${tempbucket}
aws s3 cp ${cfyaml} s3://${tempbucket}

for region in $(aws ec2 describe-regions | jq -r '.Regions[] | .RegionName')
do
    stackid=$(aws --region ${region} cloudformation create-stack --stack-name ${tempname} --template-url ${cfyamlUrl} --parameters ParameterKey=NamePrefix,ParameterValue=${tempname} ParameterKey=WebhookURL,ParameterValue=${webhook} | jq -r '.StackId')
    echo "${region},${stackid}" >> ${stackidlog}
done

aws s3 rm s3://${tempbucket}/${cfyaml}
aws s3 rb s3://${tempbucket}
