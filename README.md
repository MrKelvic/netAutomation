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
`
./
├── ansible_test
│   ├── ansible.cfg
│   ├── host
│   ├── host.yml
│   ├── playbook.yaml
│   └── runAnsible.py
├── api                       # Directory for all HTTP APIs from front-end
│   └── index.py
├── assets
│   └── TESTDATA.json        # Example of assets inventory
├── basebranchsw.json        # Proposed code description for device config (**ABSOLUTE**)
├── cleaners                 # Folder for parsing data to usable formats
│   └── generateInventory.py # Used to generate JSON inventory from `/assets/RAWASSETS.xlsx`
├── constants                # Stores fixed variables that do not change but are used in other parts of the code
│   ├── commandsDictionary.py # Fixed dictionary functions to convert device code description to raw config
│   └── commands.py           # Fixed CLI commands and function props for pulling device config
├── controller               # Interactive CLI controls for CLI UI usage
│   ├── initInteract.py      # Handles user CLI interaction
│   └── prompts.py           # Handles user prompts and inputs in CLI mode
├── depend.txt               # List of dependencies for the project
├── functions                # Main functions for communicating to network devices
│   ├── code2config.py       # Converts device code formatted config to raw config using `/constants/commandsDictionary.py` as a parameter
│   ├── config2code.py       # Converts raw device config to code format using `/constants/commands.py` as a parameter
│   ├── engineBase.py        # Entry point for accessing `engine.py`
│   ├── engine.py            # Contains classes responsible for communicating to network devices
│   ├── filter.py            # Used to parse response from `engine.py` classes into CLI or Web format (JSON)
│   ├── jinjaGenarator.py    # Proposed template generator to convert code config to raw device config (**ABSOLUTE**)
│   ├── params.py            # Converts CLI UI inputs to usable format
│   └── web.py (**ABSOLUTE**)
├── helpers                  # Functions used globally as helper functions
│   ├── confparser.py        # Parse raw config to JSON (third-party scripts)
│   ├── digestConfig2code.py # Convert JSON config to code config
│   ├── files.py             # Write to files (overwrites)
│   ├── getInventary.py      # Perform CRUD functions on inventory at `/assets/TESTDATA.json`
│   ├── interfaceMapper.py   # Convert interface name `Gi->GigabitEthernet`
│   ├── parseConfigGetter.py # Main function that converts JSON config into code format (data and control planes)
│   └── writeToExcel.py      # Writes WEB and CLI outputs into Excel for reporting
├── index.py                 # Entry point of application
├── init.sh
├── README.md
├── setup.sh
├── store                    # Stores all code-generated files
│   ├── intents             # Stores device code config (`DeviceName_IP`)
│   │   └── OSPF1_192.168.122.230.json # Intents sample
│   │   └── spoke1_192.168.122.207.json
│   ├── temp                # Stores temporal files
│   │   ├── configs         # Stores raw device config
│   │   │   ├── hubsw.config
│   │   │   └── spoke4.config
│   │   ├── host            # Stores temporal variables for Ansible

`

## Branches

This section provides information about the branches available in the project repository and their purposes. It may include descriptions of the main branches, such as "master" and "develop", as well as any feature branches or release branches that are commonly used in the project's development workflow.

- `main`: The main branch for production-ready code, may be used for deploying stable releases.
- `dev`: The development branch where ongoing development and integration of features take place.


## Contributing

Welcome

## License

license apache-2.0

---

