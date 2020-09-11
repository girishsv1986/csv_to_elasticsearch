# csv_to_elasticsearch
Demonstrates example of importing data from csv file to Elasticsearch using logstash config and/or using a python script inside a docker container.

Sample CSV data used in this repo is downloaded/referenced from [kaggle](https://www.kaggle.com/jmmvutu/summer-products-and-sales-in-ecommerce-wish)

### Import from csv using logstash config
Code for this is available under `using_logstash` directory <br/><br/>
**Pre-requisites:**
1. Logstash is installed
2. Elasticsearch is installed and running
    <br/>
    **NOTE**: If docker is installed, Elasticsearch instance can be run as a container simply by modifying the `using_python_pandas/compose/docker-compose.yml` as below
    1. Remove service named `importer-svc` from yml and related config
    2. Run command `docker stack deploy -c <compose-yml-file-path>/docker-compose.yml <stack_name>` (or use docker-compose command)

**Import using logstack**
1. Make sure to correct the input file path value in `summer_products.conf` file
2. If logstash binary code is available, navigate to logstash bin directory and run command
    `<path_to_logstash_directory>/bin/logstash -f summer_products.conf`
3. If logstash is running as a service, move the config file `summer_products.conf` under `/etc/logstash/config.d/` directory and 
4. restart logstash service

 ### Import from csv using python pandas library
Code for this is available under `using_python_pandas` directory.

This example uses docker containers- 
1. Docker one shot container (Demonstrate how to create and run single run/serve containers).
2. Elasticsearch running(Only 1 node) as a docker container and exposed on port 9200 of host.
3. Docker volume to persist the elasticsearch data
   
**Pre-requisites:**
1. [docker](https://docs.docker.com/engine/install/) version 19 or higher should be installed.

**Import using python script**<br/>
To run this example, all you need is docker and the `using_python_pandas/compose/docker-compose.yml` file, rest of the source code is available just for reference.
yml file downloads the required docker images from docker hub and creates a docker stack with 2 services.
1. data_importer_importer-svc
2. data_importer_es-01

Navigate to directory `using_python_pandas/compose/` and create the docker stack using command<br/>
`docker stack deploy -c docker-compose.yml data_importer`

Wait for elasticsearch instance to come online and script to import the data.
- To check service logs and make sure data is imported use - `docker service logs data_importer_importer-svc -f`
- To browse created indices use Elasticsearch API's. eg: - `http://<localhost or host_name>:9200/_cat/indices`

Additionally, this example/service can be extended to add kibana container, so dataset can be explored easily and 
some valuable visualizations can be created from imported datasets.