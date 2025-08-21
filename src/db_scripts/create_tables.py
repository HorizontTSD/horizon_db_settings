from src.db_clients.clients import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

tables = {
    "organizations": """
        CREATE TABLE organizations (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            email VARCHAR UNIQUE NOT NULL
        )
    """,
    "users": """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            organization_id INTEGER NOT NULL REFERENCES organizations(id),
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            role VARCHAR NOT NULL DEFAULT 'user' CHECK(role IN ('superuser','admin','user')),
            email VARCHAR UNIQUE NOT NULL,
            nickname VARCHAR UNIQUE,
            password VARCHAR NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP,
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
            is_deleted BOOLEAN NOT NULL DEFAULT FALSE
        )
    """,
    "connection_settings": """
        CREATE TABLE connection_settings (
            id SERIAL PRIMARY KEY,
            organization_id INTEGER NOT NULL REFERENCES organizations(id),
            connection_schema VARCHAR NOT NULL,
            db_name VARCHAR NOT NULL,
            host VARCHAR NOT NULL,
            port INTEGER NOT NULL DEFAULT 5432,
            ssl BOOLEAN NOT NULL DEFAULT TRUE,
            db_user VARCHAR NOT NULL,
            db_password VARCHAR NOT NULL
        )
    """,
    "schedule_forecasting": """
        CREATE TABLE schedule_forecasting (
            id SERIAL PRIMARY KEY,
            organization_id INTEGER NOT NULL REFERENCES organizations(id),
            connection_id INTEGER NOT NULL REFERENCES connection_settings(id),
            data_id INTEGER NOT NULL,
            data_name VARCHAR NOT NULL,
            source_table VARCHAR NOT NULL,
            time_column VARCHAR NOT NULL,
            target_column VARCHAR NOT NULL,
            discreteness INTEGER NOT NULL,
            count_time_points_predict INTEGER NOT NULL,
            target_db VARCHAR NOT NULL DEFAULT 'self_host' CHECK(target_db IN ('user','self_host')),
            methods_predict JSON NOT NULL
        )
    """,
    "organization_access": """
        CREATE TABLE organization_access (
            id SERIAL PRIMARY KEY,
            organization_id INTEGER NOT NULL REFERENCES organizations(id),
            access_level VARCHAR NOT NULL DEFAULT 'basic' CHECK(access_level IN ('basic','standard','premium')),
            max_users INTEGER NOT NULL DEFAULT 10,
            max_forecasts INTEGER NOT NULL DEFAULT 5,
            max_connections INTEGER NOT NULL DEFAULT 3,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN NOT NULL DEFAULT TRUE
        )
    """
}

for table_name, ddl in tables.items():
    cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
    print("="*75)
    print(f"Таблица '{table_name}' удалена (если существовала)")
    cursor.execute(ddl)
    print(f"Таблица '{table_name}' создана")

conn.commit()
conn.close()
