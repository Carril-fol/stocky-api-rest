<h1 align="center"> Invetory Management System API REST</h1>

<h4 align="center">A monolithic REST API for product inventory management. This API allows you to manage products with all their details, as well as their categories.</h4>

<p align="center">
  <a href="https://saythanks.io/to/bullredeyes@gmail.com">
      <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="python">
  </a>
  <a href="https://badge.fury.io/js/electron-markdownify">
    <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white" alt="mongodb">
  </a>
  <a href="https://gitter.im/amitmerchant1990/electron-markdownify">
    <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" alt="flask">
  </a>
  <a>
    <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" alt="docker">
  </a>
  <a>
    <img src="https://img.shields.io/badge/Render-%234f0599.svg?style=for-the-badge&logo=render&logoColor=white" alt="render">
  </a>
</p>

### Contents

- [Features](#features)
- [Tech used](#tech-used)
- [How to get the project](#how-to-get-the-project)
- [Deploy the project in render](#deploy-in-render)
- [Run the project using docker](#run-the-project-using-docker) 
- [API endpoints](#api-endpoints) 

## Features:

- Register account: Users can register their accounts.
- Login account: Users can log in their accounts.
- Log out account: Users can log out from their accounts.
- Create products: Users can create products for they management.
- Update products: Users can modify the details of their products, such as name, price, and quantity.
- Delete products: Users can delete products.
- View product details: Users can view detailed information about a specific product, including all associated details.
- Create categories: Users can create categories for the products.
- Detail categories: Users can get detail from the categories.
- Update categories: Users can modify the categories.
- Delete categories: Users can delete categories.
- Create detail of products: Users can create products that make up the parent product.
- Delete detail of products: Users can delete details from products.
- Get detail products: Users can get the products that make up a parent product.
- Update detail of products: Users can update the products that make up a parent product.

## Tech used:

**Programming language**
- [x] Python

**Framework**
- [x] Flask

**Database**
- [x] MongoDB

**Container**
- [x] Docker


## How to get the project:
#### Using Git (recommended)
1. Navigate & open CLI into the directory where you want to put this project & Clone this project using this command.
   
```bash
git clone https://github.com/Carril-fol/restful-posts.git
```
#### Using manual download ZIP
1. Download repository
2. Extract the zip file, navigate into it & copy the folder to your desired directory

#### Using docker
1. Open Docker Desktop
2. Navigate & open CLI of your preference & use this command.
```bash
docker pull carrilfol/restful-inventory-management-system
```
3. Now you need to run the image you just downloaded in docker, with the following command
```bash
docker run -p [PORT TO EXPOSE]:5000 carrilfol/restful-inventory-management-system
```

## Deploy in render:
You can access the live version of the application here (this can be a bit burdensome since the server has to be initialized): 

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://restful-inventory-management-system.onrender.com)

## API endpoints:

#### *Indication*
- [x] **Authentication required**
- [ ] **Authentication not required**

### User related
- [ ] [Register](docs/auth/UserRegisterResource.md): `POST localhost:[PORT]/users/api/v1/register`
- [ ] [Login](docs/auth/UserLoginResource.md): `POST localhost:[PORT]/users/api/v1/login`
- [x] [Logout](docs/auth/UserLogoutResource.md): `POST localhost:[PORT]/users/api/v1/logout`
- [x] [Get user info](docs/auth/UserDetailsResource.md): `GET localhost:[PORT]/users/api/v1/<user_id>`

### Categories related
- [x] [Create a category](docs/categories/CategoryCreateResource.md): `POST localhost:[PORT]/categories/api/v1/create`
- [x] [Detail from a category](docs/categories/CategoryDetailByNameResource.md): `GET localhost:[PORT]/categories/api/v1/<name>`
- [x] [Get all categories](docs/categories/CategoryAllDetailResource.md): `GET localhost:[PORT]/categories/api/v1/all`
- [x] [Delete a category](docs/categories/CategoryDeleteResource.md): `POST localhost:[PORT]/categories/api/v1/delete/<category_id>`
- [x] [Update a category](docs/categories/CategoryUpdateResource.md): `PUT localhost:[PORT]/categories/api/v1/update/<category_id>`

### Products related
- [x] [Create a product](docs/products/ProductCreateResource.md): `POST localhost:[PORT]/product/api/v1/create`
- [x] [Get details from a product](docs/products/ProductDetailByIdResource.md.md): `GET localhost:[PORT]/product/api/v1/detail/<product_id>`
- [x] [Update a product](docs/products/ProductUpdateResource.md): `PUT localhost:[PORT]/product/api/v1/update/<product_id>`
- [x] [Delete a product](docs/products/.md): `DELETE localhost:[PORT]/product/api/v1/delete/<product_id>`

### Products Detail related
- [x] [Create product details](docs/products/products_details/ProductDetailCreateResource.md): `POST localhost:[PORT]/product/detail/api/v1/create`
- [x] [Get detailed information about the products](docs/products/products_details/ProductDetailGetResource.md): `GET localhost:[PORT]/product/detail/api/v1/<barcode>`
- [x] [Delete a detail from the products](docs/products/products_details/ProductDetailDeleteResource.md): `PUT localhost:[PORT]/product/detail/delete/api/v1/<barcode>`