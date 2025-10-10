
\c auth_service_db;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- CREATE TABLE IF NOT EXISTS usuarios (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     nombre VARCHAR(100) NOT NULL,
--     apellido VARCHAR(100) NOT NULL,
--     fecha_nacimiento DATE,
--     telefono VARCHAR(20),
--     rol VARCHAR(20) CHECK (rol IN ('admin', 'estudiante', 'orientador')),
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     ultimo_login TIMESTAMP,
--     activo BOOLEAN DEFAULT TRUE
-- );

-- CREATE TABLE IF NOT EXISTS perfiles_estudiantes (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
--     intereses TEXT,
--     habilidades TEXT,
--     carrera_interes VARCHAR(100),
--     grado_academico VARCHAR(50),
--     institucion_id UUID,
--     actualmente_estudiando BOOLEAN DEFAULT FALSE,
--     UNIQUE(usuario_id)
-- );

-- CREATE TABLE IF NOT EXISTS perfiles_orientadores (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
--     especialidad VARCHAR(100),
--     experiencia TEXT,
--     certificaciones TEXT,
--     institucion_id UUID,
--     UNIQUE(usuario_id)
-- );

-- CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
-- CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(rol);
-- CREATE INDEX IF NOT EXISTS idx_perfiles_estudiantes_institucion ON perfiles_estudiantes(institucion_id);
-- CREATE INDEX IF NOT EXISTS idx_perfiles_orientadores_institucion ON perfiles_orientadores(institucion_id);
