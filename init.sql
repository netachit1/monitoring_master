CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    node_name VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_percent FLOAT,
    memory_percent FLOAT,
    disk_percent FLOAT,
    connections INTEGER,
    boot_time BIGINT
);

CREATE INDEX idx_node_timestamp ON system_metrics(node_name, timestamp);
