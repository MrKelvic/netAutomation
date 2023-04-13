# Project Name



## Network Automation (Back End)

- [Project Description](#project-description)
- [Setup Instructions](#setup-instructions)
- [File Structure](#file-structure)
- [Branches](#branches)

## Project Description

This project is a tool built to aid the administration of network devices ie, routers and switches. The current build supports Cisco IOs and Nexus, this source code contains the backend and engine for data spooling. It's enough to get you going if you're comfortable with using the CLI however I'll recommend pulling the front end that interfaces with this for better exp. Still underdevelopment ;) kinldy report any bug found.

## Prerequisite
- python 3.x.x
- pip

## Setup Instructions
- Run `python3 setup.py` for **linux** env you can run `chmod +x setup.sh && ./setup.sh` to create venv and install dependancies
- Run `python3 init.py` **linux** env you can run `chmod +x init.sh && ./init.sh` to run project

## File Structure

This section provides a brief overview of the project's file structure, highlighting key directories and files, and their purposes. It may also include descriptions of any important configuration files, templates, or other relevant files.
./
├── ansible_test
│   ├── ansible.cfg
│   ├── host
│   ├── host.yml
│   ├── playbook.yaml
│   └── runAnsible.py
├── api		#dir for all http API from front-end 
│   └── index.py
├── assets
│   └── TESTDATA.json		#Example of assets inventory
├── basebranchsw.json 		#proposed code description for device config (**ABSOLUTE**)
├── cleaners		#Folder for parsing data to useable formats
│   └── generateInventory.py		#used to generate JSON inventory from `/assets/RAWASSETS.xlsx`
├── constants		# stores fixed variables that do not change but are used in other parts of the code
│   ├── commandsDictionary.py		#fixed dictionary functions to convert device code description to raw config
│   └── commands.py		#fixed cli commands and function props for pulling device config
├── controller		#interactive CLI controls for CLI ui usage
│   ├── initInteract.py		#Handles user CLI interaction
│   └── prompts.py		#Handles user prompts and inputs in CLI mode
├── depend.txt		#list of dependancies for project
├── functions		#main functions for communicating to network devices 
│   ├── code2config.py		#converts device code formated config to raw condif using `/constants/commandsDictionary.py` as a param
│   ├── config2code.py		#converts raw device config to code format using `/constants/commands.py` as a param
│   ├── engineBase.py		#entry point for accessing `engine.py`
│   ├── engine.py		#contains classes responsible for communicating to network devices
│   ├── filter.py		#used to parse response from `engine.py` classes into CLI or Web format (JSON)
│   ├── jinjaGenarator.py		#proposed template generator to convert code config to raw device config (**ABSOLUTE**)
│   ├── params.py		#converts CLI ui inputs to useable format
│   └── web.py (**ABSOLUTE**)
├── helpers		#functions used globaly as helper functions
│   ├── confparser.py		 #Parse raw config to JSON (third-party scripts)
│   ├── digestConfig2code.py		#convert JSON config to code config
│   ├── files.py		#write to files (overwrites)
│   ├── getInventary.py		#perform CRUD functions on inventory at `/assets/TESTDATA.json`
│   ├── interfaceMapper.py		#convert interface name `Gi->GigabitEthernent`
│   ├── parseConfigGetter.py #main function that converts json config into code format (data and control planes)
│   └── writeToExcel.py		#writes WEB and CLI outputs into excel for reporting
├── index.py		#Entry point of application
├── init.sh
├── README.md
├── setup.sh
├── store		#stores all code generated files
│   ├── intents		#stores device code config (`DeviceName_IP`)
│   │   └── OSPF1_192.168.122.230.json		#intents sample
│   │   └── spoke1_192.168.122.207.json
│   ├── temp		#stores temporal files
│   │   ├── configs		#stores raw device config
│   │   │   ├── hubsw.config
│   │   │   └── spoke4.config
│   │   ├── host		#stores temporal variables for ansible
│   │   │   └── host
│   │   └── reports 		#stores reports
│   │       └── 4ad0f8080a154efdb56e143bfe6bca64.xlsx
│   └── templates (**ABSOLUTE**)
│       ├── hubsw.j2
│       └── test.j2
└── testfn.py



## Branches

This section provides information about the branches available in the project repository and their purposes. It may include descriptions of the main branches, such as "master" and "develop", as well as any feature branches or release branches that are commonly used in the project's development workflow.

- `main`: The main branch for production-ready code, may be used for deploying stable releases.
- `dev`: The development branch where ongoing development and integration of features take place.


## Contributing

Welcome

## License

license apache-2.0

---

