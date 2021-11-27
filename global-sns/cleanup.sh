#!/bin/bash -x

stackidlog=$1

if [ -z "${stackidlog}" ] ; then
	    echo "usage $0 <stackidlog> "
	        exit -1
fi

if ! command -v aws &> /dev/null
then
    echo "`aws` cli could not be found, please install it"
    exit
fi

if ! command -v cut &> /dev/null
then
    echo "`cut` cli could not be found, please install it"
    exit
fi

for record in $(cat ${stackidlog})
do
    region=$(echo ${record} | cut -d ',' -f 1 | tr -d '"')
    stackid=$(echo ${record} | cut -d ',' -f 2 | tr -d '"')
    echo "deleting ${record}"
    aws --region ${region} cloudformation delete-stack --stack-name ${stackid}
done
