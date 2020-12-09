# Snapshotalyzer-30000
Project to manage AWS EC2 instance snapshots

## About

This project is a demo, and uses boto3 to manage AWS EC2 instance snapshots.

## Configuring

shotty uses the configuration file created by the AWS CLI. e.g.

'aws configure --profile shotty'

## Running

'pipenv run python .\shotty\shotty.py <command> <subcommand> <--project=PROJECT_NAME>'

*command* is instances, volumes or snapshots
*subcommand* depends on the command
*project* is optional