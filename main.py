import argparse
import logging
import pytz
from datetime import datetime, timedelta
from kubernetes import client, config, watch

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
logger = logging.getLogger(__name__)
utc=pytz.UTC

def main(retention, namespace):

    usedConfigMaps = []

    config.load_kube_config()
    v1 = client.CoreV1Api()
    listPods = v1.list_pod_for_all_namespaces(watch=False, field_selector='metadata.namespace=='+namespace)
    for pod in listPods.items:
        for volume in pod.spec.volumes:
            if volume.config_map:
                usedConfigMaps.append(volume.config_map.name)
    logger.debug(usedConfigMaps)

    logger.debug("*********************")

    listConfigMaps = v1.list_namespaced_config_map(namespace)
    unusedConfigMaps = [{'name': v.metadata.name, 'creationdate':v.metadata.creation_timestamp} for v in listConfigMaps.items 
        if v.metadata.name not in usedConfigMaps]
    
    for e in unusedConfigMaps:
        logger.info("%s created at %s", e.get('name'), e.get('creationdate').strftime("%b %d %Y %H:%M:%S"))

    remove = str(input(' Would you like to remove configmaps older than {} d (y/n): '.format(retention)))
    if remove == 'y':
        listToRemove = [e.get('name') for e in unusedConfigMaps if e.get('creationdate') < (datetime.now(utc) - timedelta(days=retention))]
        logger.info(listToRemove)
        for configM in listToRemove:
            logger.info("deleting %s", configM)
            v1.delete_namespaced_config_map(configM, namespace)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--r', dest='retention', type=int, help='an integer for the retention', default=40)
    parser.add_argument('--n', dest='namespace', help='namespace', default='default')
    args = parser.parse_args()
    #https://www.peterbe.com/plog/vars-argparse-namespace-into-a-function
    main(**vars(args))