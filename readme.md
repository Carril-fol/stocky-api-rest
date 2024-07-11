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

#### Using docker pull
1. 

## How to run the tests:

1. To **run tests**, first you need to move to the directory where the api is
   - on windows CMD
        ```bash
        cd api
        ```
   - on bash
        ```bash
        cd api
        ```
2. now run **test command**
    ```bash
    py manage.py test
    ```
    
## API endpoints:

#### *Indication*
- [x] **Authentication required**
- [ ] **Authentication not required**

### User related
- [ ] [Register](docs/users/RegisterView.md): `POST localhost:3000/users/api/register/`
- [ ] [Login](docs/users/LoginView.md): `POST localhost:3000/users/api/login/`
- [x] [Logout](docs/users/LogoutView.md): `POST localhost:3000/users/api/logout/`
- [x] [Refresh tokens](docs/users/RefreshToken.md): `POST localhost:3000/users/api/token/refresh/refresToken`
- [x] [Get user info](docs/users/UserDataView.md): `GET localhost:3000/users/api/user/data/<int:user_id>/`
- [x] [Get users's info](docs/users/UsersDataView.md): `GET localhost:3000/users/api/data/users/`

### Profile related
- [x] [Get detail from a profile](docs/profiles/DetailProfile.md): `POST localhost:3000/profiles/api/detail/<int:profile_id>/`
- [x] [Update a profile from user](docs/profiles/UpdateProfile.md): `PUT localhost:3000/profiles/api/update/<int:profile_id>/`
- [x] [Follow a profile](docs/profiles/FollowingView.md): `POST localhost:3000/profiles/api/follow`
- [x] [Unfollow a profile](docs/profiles/UnfollowView.md): `POST localhost:3000/profiles/api/unfollow/`

### Tag related
- [x] [Create a new tag](docs/tags/CreateTag.md): `POST localhost:3000/tags/api/create/tag/`
- [x] [Get detail from a tag](docs/tags/DetailTag.md): `GET localhost:3000/api/detail/tag/<str:tag_slug>/`
- [x] [Get all tags](docs/tags/ListTags.md): `GET localhost:3000/tags/api/all-tags/`
- [x] [Delete a tag](docs/tags/DeleteTag.md): `GET localhost:3000/tags/api/delete/tag/<str:tag_slug>/`
- [x] [Update a tag](docs/tags/UpdateTag.md): `GET localhost:3000/tags/api/update/tag/<str:tag_slug>/`

### Posts related
- [x] [Create a new posts](docs/posts/CreatePost.md): `POST localhost:3000/posts/api/create/post/`
- [x] [Get a list of all posts with a certain tag](docs/posts/ListPostFilterBySpecificTags.md): `GET localhost:3000/posts/api/posts/<str:slug_tag>/`
- [x] [Get details of a posts](docs/posts/DetailPost.md): `GET localhost:3000/posts/api/detail/<int:post_id>/<str:slug_post>/`
- [x] [Update a posts](docs/posts/UpdatePost.md): `PUT localhost:3000/posts/api/update/<int:post_id>/<str:slug_post>/`
- [x] [Delete a posts](docs/posts/DeletePost.md): `DELETE localhost:3000/posts/api/delete/<int:post_id>/<str:slug_post>`

### Comment related
- [x] [Comment to a post](docs/comments/CreateComment.md): `POST localhost:3000/comments/api/create/comment/<int:post_id>/<str:post_slug>/`
- [x] [Update a comment](docs/comments/UpdateComment.md): `PUT localhost:3000/comments/api/update/comment/<int:comment_id>/`
- [x] [Delete a comment](docs/comments/DeleteComment.md): `DELETE localhost:3000/comments/api/delete/comment/<int:comment_id>/`