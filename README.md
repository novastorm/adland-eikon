### Introduction
Analyze experiments performed and extract features from the data.

### Build and Run
#### Build
```text
docker compose build
```

#### Startup
```text
./up.sh
```

#### shutdown
```text
./down.sh
```

### Usage

#### Run ETL process
```text
curl localhost:9000/trigger_etl -X POST
```

##### ETL Process
```mermaid
sequenceDiagram
    actor console as Console
    participant main as Main
    participant celery as Worker
    participant database as Database
    
    console->>main: trigger ETL process
    main->>celery: start async ETL task
    main->>console: return command accepted message
    celery->>celery: extract feature data
    celery->>celery: transform feature data
    celery->>database: load feature data
```

#### Fecth Report Data
```text
curl localhost:9000/report
```

##### Report Data
```mermaid
sequenceDiagram
    actor console as Console
    participant main as Main
    participant database as Database
    
    console->>main: Fetch Report Data
    main->>database: fetch report data
    database->>main: return data
    main->>main: format data for output
    main->>console: return formatted data
```
