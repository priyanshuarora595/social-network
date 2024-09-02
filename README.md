# Social Networking Application

This project is a social networking application built with Django and Django REST Framework. It includes features such as user authentication, friend requests, and search functionality.

## Table of Contents

- [Social Networking Application](#social-networking-application)
  - [Table of Contents](#table-of-contents)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Running the Project](#running-the-project)
  - [API Endpoints](#api-endpoints)
    - [User Login/Signup](#user-loginsignup)
    - [Search Users](#search-users)
    - [Friend Request Management](#friend-request-management)
    - [Friendship Management](#friendship-management)
  - [License](#license)

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Setup

1. **Clone the Repository:**

   `git clone https://github.com/priyanshuarora595/social-network.git`
   `cd socal-network`

2. **Build and Start the Containers:**

   `docker-compose up --build`

   This command will build the Docker images and start the containers for both the Django application and PostgreSQL database.


3. **Create a Superuser (Optional):**

   If you want to create a superuser for accessing the Django admin interface:

   `docker-compose exec social_network python manage.py createsuperuser`

## Running the Project

Once the containers are running, you can access the Django application at `http://127.0.0.1:8000`.


## API Endpoints

### User Login/Signup

- **Login**
  - **Endpoint:** '/api/login/'
  - **Method:** 'POST'
  - **Request Body:**

   ```
    {
      'email': 'user@example.com',
      'password': 'yourpassword'
    }
   ```
  - **Response:**

   ```
    {
      'refresh': 'your-refresh-token',
      'access' : 'your-access-token',
    }
   ```
- **Signup**
  - **Endpoint:** '/api/signup/'
  - **Method:** 'POST'
  - **Request Body:**

```
    {
      'username': 'username',
      'email': 'user@example.com',
      'password': 'yourpassword'
    }
```
  - **Response:**

```
   {
    "id": "uuid",
    "username": "user",
    "email": "user@example.com",
    "first_name": "",
    "last_name": ""
   }
```
### Search Users

- **Endpoint:** '/api/search/'
- **Method:** 'GET'
- **Query Parameters:**
  - 'q' - The search keyword (email or part of the name).

- **Response:**
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "uuid",
            "username": "username",
            "email": "user@example.com",
            "first_name": "",
            "last_name": ""
        }
    ]
}
```

### Friend Request Management

- **Send Friend Request**
  - **Endpoint:** '/api/friend-request/'
  - **Method:** 'POST'
  - **Request Body:**
```
    {
      'receiver_id': 'receiver-uuid'
    }
```
  - **Response:**
```
{
    "id": uuid,
    "sender": {
        "id": "sender-uuid",
        "username": "sender-username",
        "email": "sender-email@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "receiver": {
        "id": "receiver-uuid",
        "username": "receiver-username",
        "email": "receiver-email@gmail.com",
        "first_name": "",
        "last_name": ""
    },
    "status": "pending",
    "timestamp": "2024-09-01T15:04:50.165245Z"
}
```
- **Handle Friend Request**
  - **Endpoint:** '/api/friend-request/<pk>/<action>/'
  - **Method:** 'POST'
  - **URL Parameters:**
    - 'pk' - The UUID of the friend request.
    - 'action' - Either 'accept' or 'reject'.
  - **Request Body:** (empty)
  - **Response:**
```
    {
      'status': 'accepted'  // or 'rejected'
    }
```
### Friendship Management

- **List Friends**
  - **Endpoint:** '/api/friends/'
  - **Method:** 'GET'
  - **Response:**
```
[
    {
        "friend": {
            "id": "friend-uuid",
            "username": "friend-username",
            "email": "friend-email@gmail.com",
            "first_name": "",
            "last_name": ""
        }
    }
]
```

## License

This project is licensed under the MIT License.