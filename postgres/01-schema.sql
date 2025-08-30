-- Database schema for inmobiliario application
-- This script will run when the PostgreSQL container is first initialized

CREATE TABLE IF NOT EXISTS propiedades (
    p_id INTEGER PRIMARY KEY,
    nombre VARCHAR(255),
    fecha_crawl TIMESTAMP WITHOUT TIME ZONE,
    precio INTEGER,
    metros INTEGER,
    habitaciones INTEGER,
    planta INTEGER,
    ascensor INTEGER,
    poblacion VARCHAR(255),
    url VARCHAR(255),
    descripcion VARCHAR(4000),
    estatus VARCHAR(255)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_propiedades_precio ON propiedades (precio);
CREATE INDEX IF NOT EXISTS idx_propiedades_poblacion ON propiedades (poblacion);
CREATE INDEX IF NOT EXISTS idx_propiedades_fecha_crawl ON propiedades (fecha_crawl);

-- Create municipios table for URL storage
CREATE TABLE IF NOT EXISTS municipios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    url VARCHAR(500) UNIQUE NOT NULL,
    spider_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS start_urls (
    id SERIAL PRIMARY KEY,
    municipio_id INT NOT NULL REFERENCES municipios(id) ON DELETE CASCADE,
    spider_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (municipio_id, spider_name)  -- una URL puede estar activa en un solo spider
);