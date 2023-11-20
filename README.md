# Internship tool

Internship tool is a web application that helps supervisors to manage their interns and their tasks. 

It also helps interns to manage their tasks and to communicate with their supervisors.

## Installation and run

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.

```bash
pip install -r requirements.txt
```

Define the environment variables for creating the admin user:

```bash
export ADMIN_NAME=Admin
export ADMIN_EMAIL=admin@email.com
export ADMIN_PASSWORD=123123
```

Run the application:

```bash
python -m flask run
```