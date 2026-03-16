# High-Scale URL Shortener

A production-ready URL shortening service built with Django, featuring both a REST API and a user-friendly web interface, utilizing a deterministic Base62 encoding strategy for collision-free redirection.

## 🎯 Core Philosophy
The system is designed for **high read throughput** and **guaranteed uniqueness**. By leveraging a deterministic Base62 encoding strategy mapped to a relational data store, we eliminate the collision risks inherent in random string generation.

---

## 🏗 System Design & Scalability Path


### I. Current Implementation (MVP)
* **Deterministic Key Mapping:** By encoding the Auto-Incrementing ID, we achieve a one-to-one mapping that guarantees zero collisions—a significant advantage over random string generation, which suffers from the "Birthday Paradox" at scale.
* **Redirect Strategy (302 vs 301):** We utilize **HTTP 302** redirects. This prevents browser caching of the destination, ensuring every click is routed through our service for real-time analytics and tracking.
* **Relational Integrity:** SQLite/PostgreSQL provides ACID compliance, ensuring that a URL is only shortened once the mapping is safely persisted.
* **Web Interface:** A clean, responsive web UI allows users to shorten URLs directly through their browser.

### II. Scaling to 100M+ Requests/Month
To evolve this from a single-instance service to a global platform, the following "Staff-Level" optimizations are proposed:

#### 1. Distributed ID Generation
To avoid the "Single Point of Failure" of a single DB auto-increment, we move to a **Range-Based ID Provider** (similar to Twitter's Snowflake or a centralized Zookeeper-coordinated range allocator). This allows multiple app servers to generate unique short codes statelessly.

#### 2. Multi-Tier Caching
* **L1 (In-Memory):** Implement **Redis** as a "Write-Through" cache. Since $99\%$ of traffic is redirects, hitting Redis instead of Postgres reduces latency from $\approx 50\text{ms}$ to $<5\text{ms}$.
* **L2 (Edge):** Utilize a **CDN** (e.g., Cloudflare) to cache redirects for highly viral links at the network edge, further reducing load on the origin servers.

#### 3. Database Sharding
The database layer will be sharded based on the `short_code` hash. This allows for horizontal storage scaling across multiple clusters as the dataset grows into billions of records.

#### 4. Asynchronous Analytics
Click-tracking is decoupled from the redirect logic via an event-driven architecture. The redirect view pushes a "click event" to a **Kafka** topic, allowing a dedicated worker service to process analytics out-of-band without impacting user latency.


## 🚀 Quick Start

Ensure you have Docker and Python 3.10+ installed.

```bash
# Setup the database
docker run --name shortner-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate and deploy schema changes in DB
python3 manage.py migrate

# Start the server
python3 manage.py runserver
```

### Alternative: Using SQLite
If you prefer to use SQLite instead of PostgreSQL, update the `DATABASES` setting in `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Then run:
```bash
python3 manage.py migrate
python3 manage.py runserver
```

## 📱 Usage

### Web Interface
Visit `http://localhost:8000/` in your browser to access the web interface. Simply enter a URL and click "Shorten URL" to get a shortened link.

### API
```bash
# Shorten a URL
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Response: {"short_url":"http://localhost:8000/1"}
```

### Redirect
Access `http://localhost:8000/{short_code}` to be redirected to the original URL.
make migrate

# Run the server
make run