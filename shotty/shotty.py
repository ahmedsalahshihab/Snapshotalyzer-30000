import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')
ec2client = session.client('ec2')

@click.group()
def instances():
    "Commands for instances"

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = []
    if project:
        for i in ec2.instances.filter(Filters=[{'Name': 'tag:Project', 'Values': [project]}]):
            print(', '.join((i.instance_id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name, str(i.tags))))
    else:
        for i in ec2.instances.all():
            print(', '.join((i.instance_id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name, str(i.tags))))
    return

@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"
    instances = []
    if project:
        for i in ec2.instances.filter(Filters=[{'Name': 'tag:Project', 'Values': [project]}]):
            print("Starting {0}...".format(i.id))
            i.start()
    else:
        for i in ec2.instances.all():
            print("Starting {0}...".format(i.id))
            i.start()
    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"
    instances = []
    if project:
        for i in ec2.instances.filter(Filters=[{'Name': 'tag:Project', 'Values': [project]}]):
            print("Stopping {0}...".format(i.id))
            i.stop()
    else:
        for i in ec2.instances.all():
            print("Stopping {0}...".format(i.id))
            i.stop()
    return
             
if __name__ == '__main__':
    instances()
