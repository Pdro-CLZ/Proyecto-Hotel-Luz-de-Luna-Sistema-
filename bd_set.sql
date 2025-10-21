DROP DATABASE hotelprojectbd;
CREATE DATABASE IF NOT EXISTS hotelprojectbd
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2️⃣ Crear el usuario (solo si no existe)
CREATE USER IF NOT EXISTS 'hotel_admin'@'localhost' IDENTIFIED BY '12password34?!';

-- 3️⃣ Darle permisos sobre la base de datos
GRANT ALL PRIVILEGES ON HotelProjectBD.* TO 'hotel_admin'@'localhost';

-- 4️⃣ Aplicar cambios de permisos
FLUSH PRIVILEGES;

-- ==============================================
-- Poblar tablas de ubicación y empleado base
-- ==============================================
use hotelprojectbd;
-- ===============================
-- POBLAR TABLAS DE LA APP personal
-- ===============================

-- 1. Insertar país
INSERT INTO personal_pais (id, nombre)
VALUES (1, 'Costa Rica');

-- 2. Insertar provincia
INSERT INTO personal_provincia (id, nombre)
VALUES (1, 'San José');

-- 3. Insertar cantón
INSERT INTO personal_canton (id, nombre)
VALUES (1, 'Escazú');

-- 4. Insertar distrito
INSERT INTO personal_distrito (id, nombre)
VALUES (1, 'San Rafael');

-- 5. Insertar dirección
INSERT INTO personal_direccion (id, direccion_exacta, pais_id, provincia_id, canton_id, distrito_id)
VALUES (1, 'Avenida Central, 200m norte del parque', 1, 1, 1, 1);

-- 6. Insertar empleado (ligado al usuario con id=1)
INSERT INTO personal_empleado (
    id, usuario_id, direccion_id, nombre, apellido, telefono, correo, fecha_contratacion, salario, activo
)
VALUES (
    1, 1, 1, 'Carlos', 'Jiménez', '88885555', 'carlos.jimenez@example.com', '2023-01-15', 550000.00, TRUE
);

-- 7. Insertar asistencia del empleado
INSERT INTO personal_asistencia (
    id, empleado_id, fecha, hora_llegada, hora_salida, horas_trabajadas, observaciones
)
VALUES
(1, 1, '2025-10-21', '08:00:00', '16:00:00', 8.00, 'Asistencia normal'),
(2, 1, '2025-10-20', '08:10:00', '16:05:00', 7.90, 'Llegó un poco tarde');
