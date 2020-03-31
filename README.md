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

Step 1. Set up .dev.env file according to your system

Windows and MacOS 

```env
HOST=host.docker.internal
USER=odoo
PASSWORD=odoo
PORT=5555
```

Linux including WSL2 or Linux VM

```env
HOST=localhost
USER=odoo
PASSWORD=odoo
PORT=5555
```


Step 2. Start the database container 

```sh
docker-compose up -d db
```

Step 3. Build your odoo container

```sh
docker build -t odoodocker_odoo --no-cache -f OdooStock-Dockerfile . 
```

Step 4. Create a volume 

```sh
docker volume create odoo_dev_volume
```

Step 5. Start odoo container from built image

```sh
docker run --env-file .dev.env -p "8069:8069" --mount type=volume,src=odoo_dev_volume,target=/var/lib/odoo/ odoodocker_odoo:latest
```

Step 6. Create the database and your admin credentials. The database name can be whatever you want it to be. For the email, it does not need to actually be an email. You can enter a simple user name like odoo. Be sure to remember what you set for your email and password fields

![create database odoo](./images/create-database-odoo.png)

Step 7. Install the HR Module. 

Go to apps and clear the apps filter
![remove apps filter from odoo search](./images/remove-apps-filter.png)
![odoo apps](./images/odoo-apps.png)

Step 8. Search hr_mod and press enter and install the module that appears.

![install the hr module](./images/install_hr_mod.png)


Step 9. Activate developer mode by going to general settings 

![activate developer mode](./images/activate-developer-mode.png)

You should now be ready to develop modules 

#### Reloading changes 

Step 1. Exit the running odoo container

Step 2. Rebuild tha image

```sh
docker build -t odoodocker_odoo --no-cache -f OdooStock-Dockerfile .
```

Step 3. Run the container

```sh
docker run --env-file .dev.env -p "8069:8069" --mount type=volume,src=odoo_dev_volume,target=/var/lib/odoo/ odoodocker_odoo:latest
```

Step 4. Update app list from odoo ( activate developer mode if you do not see this )

![update app list](./images/update-app-list.png)

Step 5. Find your module and upgrade it 

![upgrade module](./images/upgrade-module.png)

Your changes should now be reflected



### To get the Bitnami Production Image up and running 

```sh
$ docker-compose -f prod-docker-compose.yml up --build
```

It will take sometime to spin up and the application will be unavailable in the meantime. Once the application is set up, it will be available at http://localhost:8069.

You can log in with the credentials found in the [compose file](./prod-docker-compose.yml). 



## Creating Modules 

As stated, almost all odoo configuration is done through modules. In this way Odoo can almost be infinitely extended. 


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








