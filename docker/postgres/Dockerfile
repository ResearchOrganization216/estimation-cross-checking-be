# Using the pgvector image that includes PostgreSQL 16 as the base image
FROM pgvector/pgvector:pg16

# Installing PostGIS
RUN apt-get update && \
    apt-get install -y postgis postgresql-16-postgis-3 && \
    rm -rf /var/lib/apt/lists/*
