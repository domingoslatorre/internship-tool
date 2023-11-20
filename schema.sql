CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_number TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    mobile TEXT,
    rg TEXT,
    cpf TEXT,
    birthdate DATE,
    course TEXT,
    semester_year TEXT,
    schedule TEXT,
    address TEXT,
    zip_code TEXT,
    neighborhood TEXT,
    city TEXT,
    state TEXT,
    pcd BOOLEAN,
    responsible TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
