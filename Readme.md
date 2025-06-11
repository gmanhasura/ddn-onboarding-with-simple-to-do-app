**DDN Onboarding with Simple-Todo-App**

**Setup Postgres Database**

* Use a local docker based or process based postgres server or public provider like neon  
* Run the postgres/setup.sql to create the users and todos tables and initialize these tables with a few rows of data  
* Note down the postgres URL for the database


**Run Python FastAPI server**

* Install the python modules as required by the imports inside python/todo\_fastapi.py using “pip install”  
* modify the database URL in python/todo\_fastapi.py to point to the postgres database
* Run the fastapi server using the command  
  * uvicorn todo\_fastapi:app \--reload

**Setup the DDN Project**

* Create the supergraph  
  * ddn supergraph init ddn-todo-bicevida  
  * cd ddn-todo-bicevida  
* Create subgraphs (postgres, openapi, http)  
  * ddn subgraph init postgres \--dir postgres \--target-supergraph ./supergraph.yaml  
  * ddn subgraph init openapi \--dir openapi \--target-supergraph ./supergraph.yaml  
  * ddn subgraph init http \--dir http \--target-supergraph ./supergraph.yaml  
* Edit the subgraph.yaml file in each of these subgraphs to add unique prefixes.   
  * Example: for postgres subgraph, you can add prefixes like this  
  ```yaml
    kind: Subgraph  
    version: v2  
    definition:  
     name: postgres  
     generator:  
       rootPath: .  
       graphqlRootFieldPrefix: postgres\_  
       graphqlTypeNamePrefix: Postgres\_  
       namingConvention: graphql  
   
* Configure unique prefixes for the other two subgraphs  
* Create postgres connector under postgres subgraph  
  * ddn context set subgraph postgres/subgraph.yaml  
  * ddn connector init \-i todopg  
    * Choose option  **hasura/postgres**  
    * Enter the database URL  
  * ddn connector introspect todopg  
  * ddn connector show-resources todopg  
    * This command shows the available models, commands and relationships based on predefined foreign keys  
  *  ddn model add todopg "\*"  
  *  ddn command add todopg "\*"  
  *  ddn relationship add todopg "\*"  
* Create openapi connector under openapi subgraph  
  * ddn context set subgraph openapi/subgraph.yaml  
  * ddn connector init \-i todoopen  
    * choose **hasura/openapi**  
    * NDC\_OAS\_DOCUMENT\_URI: [http://host.docker.internal:8000/openapi.json](http://host.docker.internal:8000/openapi.json)  
    * NDC\_OAS\_BASE\_URL: [http://host.docker.internal:8000](http://host.docker.internal:8000)  
    * NDC\_OAS\_LAMBDA\_PRETTY\_LOGS: true  
    * NDC\_OAS\_FILE\_OVERWRITE: true  
  * ddn connector introspect todoopen  
  * ddn connector show-resources todoopen  
    * This command shows the available commands for queries and mutations  
  *   ddn command add todoopen "\*"  
* Create http connector under http subgraph  
  *  ddn context set subgraph http/subgraph.yaml  
  *  ddn connector init \-i todohttp  
  *  Add the following lines in config.yaml under connector folder  
  ```yaml
     files:  
     - file: http://127.0.0.1:8000/openapi.json  
       spec: oas3  
   ```    
  *   ddn connector introspect todohttp  
    * This step will prompt for configuring an environment variable for SERVER\_URL  
  *  ddn connector env add \--env SERVER\_URL=http://host.docker.internal:8000 \--connector ./http/connector/todohttp/connector.yaml  
  *  ddn connector show-resources todohttp  
    * This command shows the available commands for queries and mutations  
  *   ddn command add todohttp "\*"  
* Build, run and explore  
  *  ddn supergraph build local  
  *  ddn run docker-start  
  *  ddn console \--local

Exercise1: Data modeling

* Use supergraph explorer to visually explore the commands and models under connectors in different subgraphs   
* Use the graphql explorer to exercise the queries and mutations  
* Add the relationships user-\>todos and todo-\>user manually in the metadata files for the openapi and http subgraphs.  
  * These are added automatically by adding relationships in postgres connector  
  * Rebuild, rerun and observe exercise the added relationships in queries

    

Documentation

* DDN Quick start guide  
  [https://hasura.io/docs/3.0/quickstart/](https://hasura.io/docs/3.0/quickstart/)  
    
* Postgres connector  
  [https://hasura.io/docs/3.0/how-to-build-with-ddn/with-postgresql](https://hasura.io/docs/3.0/how-to-build-with-ddn/with-postgresql)   
  [https://hasura.io/docs/3.0/reference/connectors/postgresql/](https://hasura.io/docs/3.0/reference/connectors/postgresql/)   
  [https://hasura.io/connectors/postgres](https://hasura.io/connectors/postgres)   
  [https://github.com/hasura/ndc-postgres](https://github.com/hasura/ndc-postgres)   
    
* OpenAPI connector  
  [https://hasura.io/docs/3.0/how-to-build-with-ddn/with-openapi](https://hasura.io/docs/3.0/how-to-build-with-ddn/with-openapi) [https://hasura.io/docs/3.0/reference/connectors/openapi-lambda/](https://hasura.io/docs/3.0/reference/connectors/openapi-lambda/) [https://hasura.io/connectors/openapi](https://hasura.io/connectors/openapi) [https://github.com/hasura/ndc-open-api-lambda/](https://github.com/hasura/ndc-open-api-lambda/)   
    
* HTTP Connector  
  [https://hasura.io/docs/3.0/how-to-build-with-ddn/with-http/](https://hasura.io/docs/3.0/how-to-build-with-ddn/with-http/)  
  [https://hasura.io/docs/3.0/reference/connectors/http/](https://hasura.io/docs/3.0/reference/connectors/http/)   
  [https://hasura.io/connectors/http](https://hasura.io/connectors/http)   
  [https://github.com/hasura/ndc-http](https://github.com/hasura/ndc-http) 




