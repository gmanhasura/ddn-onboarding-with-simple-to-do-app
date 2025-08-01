**DDN Onboarding with Simple-Todo-App**

**Setup Postgres Database**

* Use a local docker based or process based postgres server or public provider like neon  
* Run the postgres/setup.sql to create the users and todos tables and initialize these tables with a few rows of data  
* Note down the postgres URL for the database


**Run Python FastAPI server**

* Install the python modules as required by the imports inside python/todo\_fastapi.py using “pip install”  
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
    ![][image1]  
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
    ![][image2]  
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

**Data modeling Exercises**

* Use supergraph explorer to visually explore the commands and models under connectors in different subgraphs   
* Use the graphql explorer to exercise the queries and mutations  
* Add the relationships user-\>todos and todo-\>user manually in the metadata files for the openapi and http subgraphs.  
  * These are added automatically by adding relationships in postgres connector  
  * Rebuild, rerun and observe exercise the added relationships in queries

**Business Logic Setup**

* Create a subgraph for business logic  
  * ddn subgraph init blogic \--dir blogic  \--target-supergraph ./supergraph.yaml  
  * add subgraph prefixes by editing blogic/subgraph.yaml  
* Create NodeJS Lambda connector  
  * ddn context set subgraph blogic/subgraph.yaml  
  * ddn connector init \-i blogicty  
    * choose **hasura/nodejs**  
    * Note that this creates a new connector folder blogic/connnector/blogicty with several files  
    * You will be adding business logic functions in [functions.ts](http://functions.ts) file  
    * You may need to modify package.json file if your functions have any typescript module dependencies  
      

**Business Logic Exercises**

* Add custom logic queries and mutations  
  * Copy the 2 functions uuid() and encode() along with the comments from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
  * ddn connector introspect blogicty  
  * ddn connector show-resources blogicty  
    * This will show one query command and one mutation command as available to add  
  * ddn command add blogicty "\*"  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console –local  
  * Explore the exposed graphql **query** **uuid** and the **mutation encode**  
* Extend a model  
  * Copy the function capitalise() with the comments from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
  * ddn connector introspect blogicty  
  * ddn connector show-resources blogicty  
  * ddn command add blogicty “\*”  
  * add relationship from **Todos** model in postgres subgraph metadata to the newly added command Capitalise in blogic subgraph metadata , name the relationship as '**title\_caps**'  
    * See the file blogic/todo.hml for the content as example  
  * ddn command add blogicty "\*"  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console –local  
  * Explore the graphql queries involving **postgres\_todos** and you will notice that this model has been extended by adding a new field “**title\_caps**” which shows the capitalised version of the existing title field.   
* Error handling  
  * Copy the following import statement from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
    * import \* as sdk from "@hasura/ndc-lambda-sdk";  
  * Copy the 3 functions updateResource(), createResource(), divide() along with the comments from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
    * Notice the different forms of error generating functions from the ndc-lambda-sdk module.  
  * ddn connector introspect blogicty  
  * ddn connector show-resources blogicty  
    * This will show the commands for the new error generating functions  
  * ddn command add blogicty "\*"  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console –local  
  * Exercise the newly exposed queries with proper values and observe the errors that are generated   
* Forwarding http headers  
  * Copy the function forwardedHeader() along with the comments from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
  * ddn connector introspect blogicty  
  * Modify blogic/metadata/blogicty.hml to add the required contents for http header forwarding  
    * See the example file blogic/blogicty.hml  
    * Refer to the doc [https://hasura.io/docs/3.0/business-logic/tutorials/http-header-forwarding](https://hasura.io/docs/3.0/business-logic/tutorials/http-header-forwarding)   
  * ddn command add blogicty "\*"  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console –local  
  * Exercise the newly exposed query forwardedHeader by passing different header files from DDN console  
* Returning http headers  
  * Copy the function returnHeader() along with the comments from blogic/[functions.ts](http://functions.ts) file into your [functions.ts](http://functions.ts) file  
  * ddn connector introspect blogicty  
  * Modify blogic/metadata/blogicty.hml to add the required contents for returning http headers  
    * See the example file blogic/blogicty.hml  
    * Refer to the doc [https://hasura.io/docs/3.0/business-logic/tutorials/http-header-forwarding](https://hasura.io/docs/3.0/business-logic/tutorials/http-header-forwarding)   
  * ddn command add blogicty "\*"  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console –local  
  * Exercise the newly exposed query returnHeader and observe the response which includes the new http headers added by the function inside the code

**CI/CD Pipeline Setup**

* Setup github repository for the local ddn project ‘ddn-todo-bicevida’  
  * echo "\# ddn-todo-bicevida" \>\> [README.md](http://README.md)  
  * git init  
  * git add .  
  * git commit \-m "first commit"  
  * git branch \-M main  
  * git remote add origin https://github.com/\<github-account\>/ddn-todo-bicevida.git  
  * git push \-u origin main  
* Create branches dev, staging, prod derived from the main branch  
* Create a feature branch ‘dev-yourname’ derived from dev branch  
* Create a project for development  
  * ddn context set-context default   
  * ddn project init ddn-todo-bicevida-dev  
  * ddn supergraph build create  
    * Note down the \<build-version\> from the output  
  * ddn supergraph build apply \<build-version\>  
  * ddn console  
  * Explore the development project on the console  
  * Create a service account from project settings and save the token  
    * Name: cicd  
    * Copy token and save it safely  
    * Set access level ‘Admin’  
    * Create a github secret with name ‘HASURA\_DEV\_PAT’  
* Create a project for staging  
  * ddn context create-context staging  
  * ddn context set supergraph "supergraph.yaml"  
  * ddn context set subgraph "http/subgraph.yaml"  
  * cp .env .env.staging  
  * ddn context set localEnvFile ".env.staging"  
  * ddn project init ddn-todo-bicevida-staging \--env-file-name ".env.staging.cloud"  
  * ddn supergraph build create  
    * Note down the \<build-version\> from the output  
  * ddn supergraph build apply \<build-version\>  
  * ddn console  
  * Explore the staging project on the console  
  * Create a service account from project settings and save the token  
    * Name: cicd  
    * Copy token and save it safely  
    * Set access level ‘Admin’  
    * Create a github secret with name ‘HASURA\_STAGING\_PAT’

* Create a project for prod  
  * ddn context create-context prod  
  * ddn context set supergraph "supergraph.yaml"  
  * ddn context set subgraph "http/subgraph.yaml"  
  * cp .env .env.prod  
  * ddn context set localEnvFile ".env.prod"  
  * ddn project init ddn-todo-bicevida-prod \--env-file-name ".env.prod.cloud"  
  * ddn supergraph build create  
    * Note down the \<build-version\> from the output  
  * ddn supergraph build apply \<build-version\>  
  * ddn console  
  * Explore the prod project on the console  
  * Create a service account from project settings and save the token  
    * Name: cicd  
    * Copy token and save it safely  
    * Set access level ‘Admin’  
    * Create a github secret with name ‘HASURA\_PROD\_PAT’

* Create Github actions  
  * Build subgraph and apply to latest supergraph build  
    * Copy cicd/appy-http.yaml from this github repo to .github/worflows in your ddn-todo-bicevida repo in your main branch and sync to dev branch  
  * Build supergraph and apply to development project api  
    * Copy cicd/deploy-dev.yaml from this github repo to .github/worflows in your ddn-todo-bicevida repo in your main branch and sync to dev branch  
  * Build supergraph and apply to staging project api  
    * Copy cicd/deploy-staging.yaml from this github repo to .github/worflows in your ddn-todo-bicevida repo in your main branch and sync to staging branch  
  * Build supergraph and apply to prod project api  
    * Copy cicd/deploy-prod.yaml from this github repo to .github/worflows in your ddn-todo-bicevida repo in your main branch and sync to prod branch  
      

**CI/CD Pipeline Exercises**

* Run apply-http.yaml workflow from github ui or trigger a git push from dev branch after making some changes under http in dev branch  
  * Notice the new subgraph build created for http subgraph on development project ddn console  
  * Notice the new supergraph build created on development project ddn console  
  * You can run the build api on ddn console to test any changes you made  
* Run deploy-dev.yaml workflow from github ui or trigger a git push from dev branch after making some changes in dev branch  
  * Notice the new supergraph build created on development project ddn console  
  * Notice that this build also has been applied to the development project api  
  * Explore the project api to verify any changes made  
* Run deploy-staging.yaml workflow from github ui or create a pull request from main to  staging branch after some changes  
  * Notice the new supergraph build created on staging project ddn console  
  * Notice that this build also has been applied to the staging project api  
  * Explore the project api to verify any changes  
* Run deploy-prod.yaml workflow from github ui or create a pull request from main to  prod branch after some changes  
  * Notice the new supergraph build created on prod project ddn console  
  * Notice that this build also has been applied to the prod project api  
  * Explore the project api to verify any changes

**Observability setup with Datadog**

* Local Testing  
  * Example files config.yaml and otel-collector-config.yaml are included in observability/otel-collector/local folder  
  * Changes to .env file in your local project  
    * Add environment variable DD\_API\_KEY=\<your-datadog-api-key\>  
  * Changes to compose.yaml file in your local project  
    * Change the otel-collector image to use otel/opentelemetry-collector-contrib  
    * Add the following under otel-collector environment   
      * DD\_API\_KEY: ${DD\_API\_KEY}  
  * Changes to otel-collector-config.yaml in your local project  
    * Add data dog exporter   
    * Add custom attributes for distinguishing DDN project traces in your datadog  
      * [ddn.id](http://ddn.id)\=\<your-data-plane-id\>  
      * Any other custom attributes you find useful  
    * Optional: add spanmetrics connector if you want to generate metrics out of spans in otel collector  
  * Restart the otel collector  
    * You should see the log message “API key validation successful”  
* Explore traces in datadog trace explorer  
  * Example filter to use:  
    resource\_name:execute\_query   
    \-@operation\_name:IntrospectionQuery   
    @[ddn.id](http://ddn.id):\<your-dataplane-id\>  
* Generate metrics out of traces in datadog  
  * Follow the data dog doc: [https://docs.datadoghq.com/tracing/trace\_pipeline/generate\_metrics/](https://docs.datadoghq.com/tracing/trace_pipeline/generate_metrics/)   
      
* Hasura Cloud  
  * File a support ticket by sending email to [support@hasura.io](mailto:support@hasura.io) or using zendesk portal [https://support.hasura.io/hc/en-us/requests/new](https://support.hasura.io/hc/en-us/requests/new) with the following information  
    * Datadog site for your organization (ex:- [datadoghq.com](http://datadoghq.com),  [us3.datadoghq.com](http://us3.datadoghq.com), etc)  
    * Datadog api key  
    * Any other custom configuration for the otel collector (see an example otel collector configuration used by our SRE team in the file observability/otel-collector/cloud/otel-collector-config.yaml. 

**Authentication and Authorization Setup and Exercises**

* Add authentication and authorization for postgres subgraph with webhook  
  * Create webhook with nodejs and express   
    * install nodejs (if you already dont have it)  
      brew install node (on macbook)  
    * mkdir auth-webhook  
    * cd auth-webhook  
    * npm init \-y  
    * npm install express  
    * Copy provided auth/webhook/[index.js](http://index.js) into this folder auth-webhook  
    * node [index.js](http://index.js)  
  * Configure alternate mode for postgres   
    * Copy the yaml content for ‘postgres’ from the provided auth/auth-config.yaml into your globals/auth-config.yaml  
  * Add the following in your .env file  
    * POSTGRES\_SUBGRAPH\_AUTH\_WEBHOOK\_URL="[http://host.docker.internal:3000/authorize](http://host.docker.internal:3000/authorize)"  
  * Add the following in your globals/subgraph.yaml under envMapping  
    * POSTGRES\_SUBGRAPH\_AUTH\_WEBHOOK\_URL:  
        fromEnv: POSTGRES\_SUBGRAPH\_AUTH\_WEBHOOK\_URL  
  * Configure the authorization for ToDos and Users models  
    * Copy the TypePermissions and CommandPermissions from the ToDos.hml and User.hml files under the provided folder auth/permissions/postgres into the corresponding files in your postgres subgraph metadata folder  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console \--local  
  * Configure headers DDN console  
    * x-hasura-auth-mode=postgres  
    * user-id=1 (or any other existing user id in your Users table)  
  * You will notice that only graphql schema related to ToDos and Users model accessible for postgres user will be displayed   
  * When you exercise queries for the Users table, you will see that only the columns you allowed under TypePermissions will be displayed and queryable  
  * When you exercise queries for the ToDos table, you will see the entries belonging to only the user in user-id field and not other users.   
      
* Add authentication and authorization for openapi subgraph with JWT  
  * Create a random 256 bit secret key and save it  
    * openssl rand \-base64 32  
    * Add the following in your .env file  
      OPENAPI\_SUBGRAPH\_JWT\_SECRET\_KEY="\<your-secret-key\>"   
    * Add the following in your globals/subgraph.yaml under envMapping  
      OPENAPI\_SUBGRAPH\_JWT\_SECRET\_KEY:  
            fromEnv: OPENAPI\_SUBGRAPH\_JWT\_SECRET\_KEY  
  * Create a jwt token for the claims in the provided auth/jwt/openapi-jwt-claims.txt file  
  * Configure alternate mode for openapi   
    * Copy the yaml content for ‘openapi’ from the provided auth/auth-config.yaml into your globals/auth-config.yaml  
  * Configure the authorization for some commands  
    * Copy the TypePermissions and CommandPermissions from the following files under the provided folder auth/permissions/postgres into the corresponding files in your postgres subgraph metadata folder  
      * GetTodosGetAllTodosTodosGet.hml			  
      * GetUsersGetTodosByUserUsersUserIdTodosGet.hml  
      * GetTodosReadTodoTodosTodoIdGet.hml  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console \--local  
  * Configure headers DDN console  
    * x-hasura-auth-mode=openapi  
    * Auth-Token=\<jwt-token-created-above\>  
  * You will notice that only the commands where ‘openuser’ role has been given access are displayed on the graphql explorer   
  * GraphQL queries involving the exposed schema should all succeed  
      
* Add authentication and authorization for http subgraph with JWT  
  * Create a random 256 bit secret key and save it  
    * openssl rand \-base64 32  
    * Add the following in your .env file  
      HTTP\_SUBGRAPH\_JWT\_SECRET\_KEY="\<your-secret-key\>"   
    * Add the following in your globals/subgraph.yaml under envMapping  
      HTTP\_SUBGRAPH\_JWT\_SECRET\_KEY:  
            fromEnv: HTTP\_SUBGRAPH\_JWT\_SECRET\_KEY  
  * Create a jwt token for the claims in the provided auth/jwt/http-jwt-claims.txt file  
  * Configure alternate mode for http   
    * Copy the yaml content for ‘httpi’ from the provided auth/auth-config.yaml into your globals/auth-config.yaml  
  * Configure the authorization for some commands  
    * Copy the TypePermissions and CommandPermissions from the following files under the provided folder auth/permissions/postgres into the corresponding files in your postgres subgraph metadata folder  
      * GetAllTodosTodosGet.hml			  
      * ReadTodoTodosTodoIdGet.hml  
      * GetTodosByUserUsersUserIdTodosGet.hml  
  * ddn supergraph build local  
  * ddn run docker-start  
  * ddn console \--local  
  * Configure headers DDN console  
    * x-hasura-auth-mode=http  
    * Authorization=Bearer \<jwt-token-created-above\>  
  * You will notice that only the commands where ‘httpuser’ role has been given access are displayed on the graphql explorer   
  * GraphQL queries involving the exposed schema should all succeed

**Documentation**

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
    
* Business Logic  
  [https://hasura.io/docs/3.0/business-logic/overview/](https://hasura.io/docs/3.0/business-logic/overview/)   
    
* NodeJS Lambda connector  
  [https://hasura.io/connectors/nodejs](https://hasura.io/connectors/nodejs)   
  [https://github.com/hasura/ndc-nodejs-lambda/](https://github.com/hasura/ndc-nodejs-lambda/)   
  [https://hasura.io/blog/introducing-typescript-functions-on-hasura-ddn](https://hasura.io/blog/introducing-typescript-functions-on-hasura-ddn)   
    
* DDN Projects and CI/CD Pipelines  
  [https://hasura.io/docs/3.0/project-configuration/overview/](https://hasura.io/docs/3.0/project-configuration/overview/)   
  [https://hasura.io/docs/3.0/project-configuration/tutorials/manage-multiple-environments](https://hasura.io/docs/3.0/project-configuration/tutorials/manage-multiple-environments)   
  [https://hasura.io/docs/3.0/project-configuration/tutorials/work-with-multiple-subgraphs](https://hasura.io/docs/3.0/project-configuration/tutorials/work-with-multiple-subgraphs)   
  [https://hasura.io/docs/3.0/project-configuration/tutorials/work-with-multiple-repositories](https://hasura.io/docs/3.0/project-configuration/tutorials/work-with-multiple-repositories)   
  [https://hasura.io/docs/3.0/project-configuration/project-management/manage-contexts](https://hasura.io/docs/3.0/project-configuration/project-management/manage-contexts)   
  [https://hasura.io/docs/3.0/project-configuration/project-management/manage-collaborators](https://hasura.io/docs/3.0/project-configuration/project-management/manage-collaborators)   
  [https://hasura.io/docs/3.0/project-configuration/project-management/service-accounts](https://hasura.io/docs/3.0/project-configuration/project-management/service-accounts)   
  [https://hasura.io/docs/3.0/deployment/hasura-ddn/ci-cd/](https://hasura.io/docs/3.0/deployment/hasura-ddn/ci-cd/)   
  [https://github.com/hasura/ddn-deployment/](https://github.com/hasura/ddn-deployment/)   
    
* Observability  
  [https://hasura.io/docs/3.0/observability/overview/](https://hasura.io/docs/3.0/observability/overview/)   
  [https://opentelemetry.io/docs/collector/](https://opentelemetry.io/docs/collector/)   
  [https://docs.datadoghq.com/opentelemetry/setup/collector\_exporter/](https://docs.datadoghq.com/opentelemetry/setup/collector_exporter/)   
  [https://last9.io/blog/convert-opentelemetry-traces-to-metrics-using-spanconnector/](https://last9.io/blog/convert-opentelemetry-traces-to-metrics-using-spanconnector/)   
  [https://docs.datadoghq.com/tracing/trace\_pipeline/generate\_metrics/](https://docs.datadoghq.com/tracing/trace_pipeline/generate_metrics/)   
  [https://github.com/hasura/graphql-engine/tree/master/community/boilerplates/observability/enterprise](https://github.com/hasura/graphql-engine/tree/master/community/boilerplates/observability/enterprise) 

* Authentication and Authorization  
  [https://hasura.io/docs/3.0/auth/overview/](https://hasura.io/docs/3.0/auth/overview/)   
  [https://hasura.io/docs/3.0/reference/metadata-reference/auth-config](https://hasura.io/docs/3.0/reference/metadata-reference/auth-config)   
  [https://hasura.io/docs/3.0/auth/permissions](https://hasura.io/docs/3.0/auth/permissions)    
  [https://hasura.io/docs/3.0/reference/metadata-reference/permissions](https://hasura.io/docs/3.0/reference/metadata-reference/permissions)   
     
    
    
    
    
  




[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>