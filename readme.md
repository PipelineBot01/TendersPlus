#### TendersPlus Project Code structure

##### Frontend
```bash
├── src
│   ├── api # all API requests
│   ├── components # JSX components
│   ├── pages # define each page of the webapp
│   ├── store # the redux configuration
|   ├── utils # define data types, and other functions
|   ├── App.tsx
|   └── index.tsx # webapp main entry
|
├── public
│   ├── favicon.ico # the icon of website
│   ├── index.html # the main entry of the website
│   ├── manifest.json
|   └── robots.txt # tells search engine crawlers which URLs the crawler can access on your site
|
├── package.json # records important metadata about a project
├── ts.config.json # records important metadata about a project
├── README.md # It show how to launch the webapp
└──.gitignore
```

##### Backend
```bash
├── app
│   ├── db
|        ├──mysql # structure data, i.e. user infomation
|        ├──mongo # unstructure data, i.e.
|        ├──redis # runtime variable
│   ├── dependencies # define request'dependencies
|   ├── errors # define HTTP exception
|   ├── models # data validation 
|   ├── routers # API/requests
|   ├── scheduler # background timed task
|   ├── utils # extra script/ helper function
|   ├── test # unit test
|   ├── main.py # server entry, launch server here
|   ├── config.py # settings management
|   └── .env # server config, will be passed to config.py
|
├── log
│   ├── stdout.log
│   └── stderr.log
|
├── deploy.sh # deployment script
├── requirements.txt # python package requirements
└── redeme.med # it shows how to launch the server
```
