import sys
import click
import time
import lib.database as db
from lib.cli.status.display import supports_color, render_status 
from ClusterShell.NodeSet import NodeSet

def load_nodes():
    #  Load node details

    base_query = db.get_nodes_with_latest_healthchecks()
    field_dict = {}
    query = db.get_query_by_fields(base_query,field_dict)
    nodes = query.all()
    keys = None
    nodes = [db.node_to_dict(node, keys) for node in nodes]
    return nodes

###
# click options and command details
###

@click.command("status")
@click.option(
    "--watch",
    is_flag=True,
    default=False,
    required=False,
    help="Keep status page active and refresh every other second until interrupted."
)
@click.option(
    "--no_color",
    is_flag=True,
    default=False,
    required=False,
    help="Disable color output."
)

###
# Main 'status' command
###

def cmd(watch, no_color):
    """
    Display an overview status of the OCI-HPC Stack

    By default the command runs once and prints the status.
    """

    nodes = load_nodes()

    if not nodes:
        click.echo("No nodes found.", err=True)

    #  Check color option
    no_color = supports_color(sys.stdout) and not no_color

    #  Check watch option, if not then only run once and exit
    if not watch:
        click.echo(render_status(nodes, no_color))
        return

    # Watch mode – clear screen and refresh each second
    try:
        while True:
            click.clear()
            click.echo(render_status(nodes, no_color))
            click.echo("Ctrl-C to exit")
            time.sleep(2)
            nodes = load_nodes()

    except KeyboardInterrupt:
        click.echo("\nStopped watching.")


