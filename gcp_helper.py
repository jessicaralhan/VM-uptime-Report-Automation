from __future__ import annotations
import logging
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
import json
from google.cloud import compute_v1
from google.oauth2 import service_account
import os

# credential_path = "/home/jessica-ralhan/Downloads/gcp-running-vms-f8e375ec0bea.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def gcp_report(
    project_id: str, logger, 
) -> dict[str, Iterable[compute_v1.Instance]]:
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        logger.warning("GOOGLE_APPLICATION_CREDENTIALS is not set. Set it via .env or in code.")
        return {}

    """
    Returns a dictionary of all running instances present in a project, grouped by their zone.

    Args:
        project_id: Google Cloud project ID.
        logger: Logger object for logging events.

    Returns:
        A dictionary with zone names as keys (in form of "zones/{zone_name}") and
        iterable collections of Instance objects as values.
    """
    # credentials = service_account.Credentials.from_service_account_info(gcp_creds)

    instance_client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest(project=project_id, max_results=50)

    day = datetime.today().strftime('%Y-%m-%d')
    gcp_info = []

    all_instances = defaultdict(list)
    logger.info("Fetching instances...")

    try:
        agg_list = instance_client.aggregated_list(request=request)

        for zone, response in agg_list:
            if response.instances:
                all_instances[zone].extend(response.instances)
                for instance in response.instances:
                    if instance.status:
                        logger.info(f"Running VM: {instance.name} in {zone}")
                        vm_info = {
                            "VM Name": instance.name,
                            "Zone": zone,
                            "Machine Type": instance.machine_type,
                            "Status": instance.status,
                            "Creation Timestamp": instance.creation_timestamp,
                        }
                        gcp_info.append(vm_info)

        report_filename = f"gcp_{day}.json"
        file = open(report_filename, "w")
        file.write(json.dumps(gcp_info, indent=4))
        file.close()

        logger.info(f"GCP report saved to {report_filename}")

    except Exception as e:
        logger.error(f"An error occurred while fetching instances: {e}")

  

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#     logger = logging.getLogger("GCP_Report")
    
#     PROJECT_ID = "gcp-running-vms"
#     gcp_report(PROJECT_ID, logger) 
