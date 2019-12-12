# fastqc-application

### 0. Contents
```
.
├── Dockerfile
├── README.md
├── app.ini
└── fastqc-0.11.7
    ├── _util
    │   ├── VERSION
    │   └── container_exec.sh
    ├── app.json.j2
    ├── job.json.j2
    ├── runner-template.sh
    └── tester.sh
```

### 1. Clone
```
git clone https://github.com/wjallen/fastqc-application
cd fastqc-application/
```

### 2. Personalize
#### ./app.ini
=> change to your docker username / preferred repo and tag

#### ./fastqc-0.11.7/app.json.j2
=> change `executionSystem`, `deploymentSystem`, and `deploymentPath` if necessary

#### ./fastqc-0.11.7/runner-template.sh
=> change `CONTAINER_IMAGE` to your preferred repo source


### 3. Deploy
```
apps-deploy -E app.ini --test-job fastqc-0.11.7
```

### 4. Test
```
jobs-submit -F deploy-username-job.json
jobs-output-list <jobid>
```
=> job was a success if `read1_fastqc.html` exists

