import boto3
import click
import botocore

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')
ec2client = session.client('ec2')

def filter_instances(project):
    instances = []
    if project:
        instances = ec2.instances.filter(Filters=[{'Name': 'tag:Project', 'Values': [project]}])
    else:
        instances = ec2.instances.all()
    return instances

def has_pending_snapshot(volume):
    snapshots = list(volume.snapshots.all())
    return (snapshots and snapshots[0].state == "pending")

#def filter_volumes(project):
#    volumes = []
#    if project:
#        volumes = ec2.volumes.filter(Filters=[{'Name': 'tag:Project', 'Values': [project]}])
#    else:
#        volumes = ec2.volumes.all()
#    return volumes

############################################################################

@click.group()
def cli():
    "shotty manages snapshots"

@cli.group('volumes')
def volumes():
    "Commands for volumes"

@cli.group('instances')
def instances():
    "Commands for instances"

@cli.group('snapshots')
def snapshots():
    "Commands for snapshots"

############################################################################
    
@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print(', '.join((i.instance_id, i.instance_type, i.placement['AvailabilityZone'], i.state['Name'], i.public_dns_name, str(i.tags))))
    return

@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as error:
            print(" Could not start instance {0}. ".format(i.id) + str(error))
            continue #not necessary as the loop will continue either way
    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"
    instances = filter_instances(project)
    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as error:
            print(" Could not stop instance {0}. ".format(i.id) + str(error))
            continue #not necessary as the loop will continue either way
    return

@instances.command('snapshot')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    instances = filter_instances(project)
    for i in instances:
        print("Stopping instance {0}".format(i.id))
        i.stop()
        i.wait_until_stopped()
        volumes = i.volumes.all()
        for v in volumes:
            if has_pending_snapshot(v):
                print(" Skipping {0}, snapshot already in progress".format(v.id))
            else:
                print(" Creating snapshot of {0}".format(v.id))
                v.create_snapshot(Description="Created by SnapshotAlyzer 30000")
        print("Starting instance {0}".format(i.id))
        i.start()
        i.wait_until_running()
    print("Job's done!!!")
    return

############################################################################

#@volumes.command('list')
#@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")    
#def list_volumes(project):
#    "List EC2 volumes"
#    volumes = filter_volumes(project)
#    for i in volumes:
#        print(', '.join((i.volume_id, i.snapshot_id, i.availability_zone, str(i.tags))))
#    return

@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")    
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)
    for i in instances:
        volumes = i.volumes.all()
        for v in volumes:
            print(', '.join((v.volume_id, v.snapshot_id, v.availability_zone, str(v.tags))))
    return

############################################################################

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project (tag Project:<name>)")
@click.option('--all', 'list_all', default=False, is_flag=True, help="List all snapshots for each volume, not just the most recent")
def list_snapshots(project, list_all):
    "List EC2 snapshots"
    instances = filter_instances(project)
    for i in instances:
        volumes = i.volumes.all()
        for v in volumes:
            snapshots = v.snapshots.all()
            for s in snapshots:
                print(', '.join((i.id, s.id, s.volume_id, s.start_time.strftime("%c"), s.state, s.progress)))
                if not list_all and s.state == 'completed': break
    return


if __name__ == '__main__':
    cli()
