# Coderr Backend

**Coderr** is a REST API built with Django and Django REST Framework for a freelancer platform that connects customers with service providers. It provides user authentication and supports CRUD operations for offers, orders, profiles and reviews.

This backend is designed to work with the [Coderr Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Coderr), version **1.2.1**.

The frontend is used without modifications. No changes were made to its `config.js`.

## Features

- **User Authentication:** Register users and log in with token-based authentication
- **Offer Management:** Create, browse, update, and manage offers, including offer images and offer details
- **Offer Discovery:** Search offers by title or description, filter by creator, minimum price and delivery time, and sort and paginate results
- **Order Management:** Create and manage orders between customers and businesses
- **Profile Management:** Retrieve and update user profiles, upload profile images and browse business and customer profiles
- **Review System:** Create and manage reviews, with filtering by business or reviewer and sorting by rating or update date
- **Access Control:** Restrict actions according to authentication, user type, and resource ownership

The codebase is organized into modular Django apps:

- `core/` – Project settings and global URL configuration
- `users_app/` – User registration, login and custom user model
- `offers_app/` – Offers, offer details, filters, and pagination
- `orders_app/` – Order management and order counts
- `profiles_app/` – User profiles
- `reviews_app/` – Reviews, filters, and permissions
- `base_info_app/` – Public platform statistics

## Tech Stack

- **Framework:** Django 6.1 and Django REST Framework
- **Language:** Python 3.14.5
- **Database:** SQLite by default
- **Dependencies:** See `requirements.txt`

## Installation & Local Setup

To get a local copy of the project up and running, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/natgian/coderr-backend.git
cd coderr-backend
```

### 2. Set up a virtual environment

**Windows**

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=<YOUR-DJANGO-SECRET-KEY>
DEBUG=true
```

`SECRET_KEY` is required. Keep it private, and disable `DEBUG` in production.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrative user

```bash
python manage.py createsuperuser
```

The Django admin is available at `/admin/`.

### 7. Start the development server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/api/` by default.

## API Endpoints

| Feature            | Endpoint                                         | Method            | Description                                                                 |
| ------------------ | ------------------------------------------------ | ----------------- | --------------------------------------------------------------------------- |
| **Authentication** | `/api/registration/`                             | `POST`            | Register a new user and return an authentication token                      |
|                    | `/api/login/`                                    | `POST`            | Log in and return an authentication token                                   |
| **Platform**       | `/api/base-info/`                                | `GET`             | Retrieve platform statistics                                                |
| **Offers**         | `/api/offers/`                                   | `GET`             | Retrieve the paginated offer list; supports filtering, search, and ordering |
|                    | `/api/offers/`                                   | `POST`            | Create an offer                                                             |
|                    | `/api/offers/<id>/`                              | `GET`             | Retrieve an offer                                                           |
|                    | `/api/offers/<id>/`                              | `PATCH`           | Update an offer                                                             |
|                    | `/api/offers/<id>/`                              | `DELETE`          | Delete an offer                                                             |
|                    | `/api/offerdetails/<id>/`                        | `GET`             | Retrieve offer details                                                      |
| **Orders**         | `/api/orders/`                                   | `GET`, `POST`     | List the authenticated user's orders or create an order                     |
|                    | `/api/orders/<id>/`                              | `PATCH`, `DELETE` | Update or delete an order                                                   |
|                    | `/api/order-count/<business_user_id>/`           | `GET`             | Count in-progress orders for a business                                     |
|                    | `/api/completed-order-count/<business_user_id>/` | `GET`             | Count completed orders for a business                                       |
| **Profiles**       | `/api/profile/<user_id>/`                        | `GET`, `PATCH`    | Retrieve or update a profile                                                |
|                    | `/api/profiles/business/`                        | `GET`             | List business profiles                                                      |
|                    | `/api/profiles/customer/`                        | `GET`             | List customer profiles                                                      |
| **Reviews**        | `/api/reviews/`                                  | `GET`, `POST`     | List or create reviews                                                      |
|                    | `/api/reviews/<id>/`                             | `PATCH`, `DELETE` | Update or delete a review                                                   |

Most endpoints require authentication. Permissions for creating or modifying resources depend on the endpoint and the authenticated user's role.

## Running Tests

Run the test suite with Django:

```bash
python manage.py test
```

## License & Purpose

This project was developed exclusively for educational purposes. You are free to use, modify, and explore this codebase for personal learning and development.

## Contact

For questions or feedback, please contact:

- Email: <contact@natgian.dev>
- GitHub: [natgian](https://github.com/natgian)
