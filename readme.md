# Stoky API REST

**Stoky API REST** Is an API developed in Flask that enables efficient management of products categorized by type, supplier registration, 
and stock control, ensuring an organized and accessible inventory system.

## 📋 Contents
- [Features](#features)
- [Tech used](#tech-used)
- [How to get the project:](#how-to-get-the-project)
    - [Using Git (recommended)](#using-git-recommended)
    - [Using manual download ZIP](#using-manual-download-zip)
    - [Using docker](#using-docker)
- [Deploy in render](#deploy-in-render)

## Features

### 📦 Category Management
* Create, update, and delete product categories.
* View category details.
### 🏭 Supplier Management
* Register, update, and delete suppliers.
* Retrieve supplier details.
### 📊 Stock Management
* Add, update, and remove products from inventory.
* Track stock levels and availability.
* Generate Excel reports of current stock levels.

## Tech used 

**Programming language**
- Python 

**Framework**
- Flask

**Database**
- PostgreSQL

**Container**
- Docker

## How to get the project
#### Using Git (recommended)
1. Navigate & open CLI into the directory where you want to put this project & Clone this project using this command.
   
```bash
git clone https://github.com/Carril-fol/restful-inventory-manager.git
```
#### Using manual download ZIP
1. Download repository
2. Extract the zip file, navigate into it & copy the folder to your desired directory

#### Using docker
1. Open Docker Desktop
2. Navigate & open CLI of your preference & use this command.
```bash
docker pull carrilfol/restful-inventory-manager
```
3. Now you need to run the image you just downloaded in docker, with the following command
```bash
docker run -p [PORT TO EXPOSE]:8000 carrilfol/restful-inventory-manager
```

## Deploy in render
You can access the live version of the application here and make requests from Postman or Insomnia.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://restful-inventory-manager.onrender.com)

>Note: The server may take time to start because it is hosted on the free layer.

<p align="center">
  Developed with ❤️ by <a href="https://github.com/Carril-fol" target="_blank">Folco Carril</a>
</p>