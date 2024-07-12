# Invetory-Management-System-API-RESTful

**Inventory Management System RESTful API** is one of my personal projects focused on managing inventory through a RESTful API. This repository contains the backend code for the API.

### Contents

- [Features](#features)
- [Tech used](#tech-used)
- [How to get the project](#how-to-get-the-project) 
- [Run the project using docker](#run-the-project-using-docker) 
- [API endpoints](#api-endpoints) 

## Features:
- Users can create their profiles (JWT authentication)
- Users can edit their profile
- Users can write posts. They can set the tag of their posts
- Registered users can comment on their own or others blog
- Unregistered public users can read blogs but can't comment or react n blogs
- Posts of a particular category can be viewed for unregistered publics users and registered users
- Users can create comments on posts they like
- Users can modify or delete their comments on the respective posts

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
docker run -p [PORT TO EXPOSE]:5000 carrilfol restful-inventory-management-system
```

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