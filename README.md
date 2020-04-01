# Odoo Docker

This repo contains the nessecary Dockerfiles needed for Odoo. Our chosen solution for the [HRWhitelisting Project](https://github.com/gcdevops/HRWhiteListing). 


## What is Odoo

Odoo is an open source web-based ERP (Enterprise Resource System) built primarly on the Python programming language and PostgreSQL database. Odoo is highly cuhstomizable and configurable through its interface or through the use of modules. You can find more information on Odoo [here](https://www.odoo.com/).


## How to get Odoo running locally

We are using Docker and docker-compose for the core system and mounting custom plugins by copying them from the [add-ons](./add-ons) and [themes](./themes) to the appropriate folders within the containers. 

We have two images in this repo 

<table>
    <thead>
        <tr>
            <td>
                Dockerfile
            </td>
            <td>
                Docker Compose file
            </td>
            <td>
                Link to original image 
            </td>
            <td>
                Purpose
            </td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <a href="./OdooStock-Dockerfile">Odoo Stock Image</a>
            </td>
            <td>
                <a href="./docker-compose.yml"> Odoo Stock Compose File </a>
            </td>
            <td>
                <a href="https://hub.docker.com/_/odoo">DockerHub</a>
                <a href="https://github.com/odoo/docker/tree/6d92142da193f60c161f97eea1079f437dd51d7e/13.0">GitHub</a>
            </td> 
            <td>
                This is used for development purposes only. It is much quicker to build and start the application then the bitnami production image
            </td>   
        </tr>
        <tr>
            <td>
                <a href="./Dockerfile">Bitnami Odoo Image</a>
            </td>
            <td>
                <a href = "./prod-docker-compose.yml">Bitnami Compose File</a>
            </td>
            <td>
                <a href="https://hub.docker.com/r/bitnami/odoo/">Dockerhub</a>
                <a href="https://github.com/bitnami/bitnami-docker-odoo/tree/master/13/debian-10"> GitHub </a>
            </td>
            <td>
                This is used in the production environment as the bitnami image has better support for kubernetes. 
            </td>
        </tr>
    </tbody>
</table>



### Setting up for development

You should use the Odoo stock image for local development as you are able to easily reload changes to modules

Step 1. Start the database container 

```sh
docker-compose up -d db
```

Step 3. Build your odoo container

```sh
docker-compose build --no-cache odoo
```

Step 4. Start odoo container

```sh
docker-compose up -d odoo
```

Step 5. Create the database and your admin credentials. The database name can be whatever you want it to be. For the email, it does not need to actually be an email. You can enter a simple user name like odoo. Be sure to remember what you set for your email and password fields as this will be your login information.

![create database odoo](./images/create-database-odoo.png)

Step 6. Install the HR Module. 

Go to apps and clear the apps filter
![remove apps filter from odoo search](./images/remove-apps-filter.png)
![odoo apps](./images/odoo-apps.png)

Step 7. Search hr_mod and press enter and install the module that appears.

![install the hr module](./images/install_hr_mod.png)


Step 8. Activate developer mode by going to general settings 

![activate developer mode](./images/activate-developer-mode.png)

You should now be ready to develop modules

To take down Odoo completely

```sh
$ docker-compose down
```

#### Loading Data 

You can optionally load in organizational data from GEDS. Please note these data sets were developed using the GEDS Open Data Set. No protected or classified information is contained within these data sets. No protected or classified information should be added to these data sets. If you are interested in how these datasets were created, vist this [repo](https://github.com/gcdevops/HRWhiteListing-data).

Step 1. Ensure you have developer mode activated 

Step 2. Navigate to the ```Employees``` (HR) module by selecting the four squares in the top left corner and clicking Employees. Then click on ```Departments``` as shown

![Employees page with departments highlighted](./images/employees-page-department-highlight.png)

Step 3. Delete any existing data that's there

![Delete existing department](./images/delete-existing-departments.png)

Step 4. Select import and navigate to the department import page and then select ```Load File```
![Department Import Page](./images/department-import-page.png) 

Step 5. Select [odoo-org-csv.csv](./data/org_structure/odoo-org-csv.csv) and import

![import organizational structure](./images/import-org.png)

Step 6. Be patient ! This might take 5-10 minutes depending on your system

![organizational structure import loading](./images/import-org-loading.png)

Once the loading screen stops. You should see the ESDC org structure has been imported 

![org structure imported](./images/imported-org.png)
![org structure visualization](./images/imported-org-visualized.png)

Step 7. Now you will need to load Job Titles. This is the same process as Departments except you navigate to ```Job Positions```

![Jobs page with employees highlighted](./images/employees-page-job-highlighted.png)

Step 8. Similarly, import [odoo-jobs-csv.csv](./data/org_structure/odoo-jobs-csv.csv)

![importing jobs](./images/import-jobs.png)

Step 9. Now import employees by navigating to the ```Employees``` page and then importing [odoo-employees-csv.csv](./data/org_structure/odoo-employees-csv.csv). Note this will take 15-20 minutes due to the large amount of records.

![import employees](./images/import-employees.png)
![imported employees](./images/imported-employees.png)

You should now have the GEDS DataSet for the ESDC Organization imported 

#### Reloading changes 

Step 1. Make sure your code is saved to disk

Step 2. Within the Apps module, update app list from Odoo ( activate developer mode if you do not see this )

![update app list](./images/update-app-list.png)

Step 5. Find your module and upgrade it 

![upgrade module](./images/upgrade-module.png)

Your changes should now be reflected


## Creating Modules 

As stated, almost all Odoo configuration is done through modules. In this way Odoo can almost be infinitely extended. 


To get started learning how to build modules, go through this [tutorial](https://www.odoo.com/documentation/13.0/howtos/backend.html). Note: There is already an open academy module for you to play around with. Be sure to create a new branch id you decide to modify for learning purposes


### Some Notes That May Help You

A couple of things to note that aren't explicitly mentioned in the tutorial. When creating data files in XML, you are actually creating records for different tables in the database.

For example take a look at [openacademy.xml](./add-ons/openacademy/views/openacademy.xml) and specifically at this piece 

```xml
<!--course list view-->
<record model="ir.ui.view" id="course_tree_view">
    <field name="name">course.tree</field>
    <field name="model">openacademy.course</field>
    <field name="arch" type="xml">
        <tree string="Course Tree">
            <field name = "name" />
            <field name = "responsible_id" />
        </tree>
    </field>
</record>
```

It's pretty intuitive, we are creating a record for the ```ir.ui.view``` table ( ir_ui_view in PostgreSQL ) and populating the record with its fields. In this case we are creating a list view for courses based off of the openacademy.course model ( go through the tutorial at least once to understand what I am talking about).


As such you are able to use modules to overwrite data for other modules!

For example, We are using the employees module.








