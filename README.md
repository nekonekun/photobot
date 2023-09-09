# What it is

Small telegram bot that can work with geolocation

---

# What exactly bot can do

- Store photos
- Add description, hashtags and geolocation
- Search photos by hashtags, ordered by distance from user

---

# How to run bot

### Prepare database
- Install postgresql
- Adjust alembic.ini sqlalchemy.url to your real database URL
- Run `alembic upgrade head` 

### Prepare storage
- Install Redis

### Prepare poetry
`poetry install` should be enough

### Prepare environment
Three environment variables must be set:
 - `NPB_TOKEN` is your bot API token 
 - `NPB_DB_URL` is your postgresql database URL (with asyncpg dialect)
 - `NPB_REDIS_URL` is your redis URL

### Run
`poetry run photobot`