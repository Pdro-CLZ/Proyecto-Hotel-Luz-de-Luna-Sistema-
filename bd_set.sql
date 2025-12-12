-- ==============================================
-- De primero
-- ==============================================

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
-- De segundo, despues de migrate + runserver
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

-- ============================================
-- LIMPIEZA DE DATOS ANTERIORES
-- ============================================
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE reservas_fechareservada;
TRUNCATE TABLE reservas_preciohabitacion;
TRUNCATE TABLE reservas_reserva;
TRUNCATE TABLE sitio_web_cliente;
TRUNCATE TABLE reservas_habitacion_amenidades;
TRUNCATE TABLE reservas_habitacion;
TRUNCATE TABLE reservas_amenidad;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================
-- AMENIDADES
-- ============================================
INSERT INTO reservas_amenidad (nombre) VALUES
('Hamaca'),
('Piscina'),
('Refrigeradora'),
('Parqueo'),
('Wi-Fi'),
('Cocina'),
('Cama grande'),
('Cama pequeña');

-- ============================================
-- HABITACIONES
-- ============================================
INSERT INTO reservas_habitacion (id, nombre) VALUES
(1, 'Habitación 1'),
(2, 'Habitación 2'),
(3, 'Habitación 3'),
(4, 'Habitación 4'),
(5, 'Habitación 5'),
(6, 'Habitación 6'),
(7, 'Habitación 7'),
(8, 'Habitación 8');

-- ============================================
-- TODAS LAS AMENIDADES PARA TODAS LAS HABITACIONES
-- ============================================
INSERT INTO reservas_habitacion_amenidades (habitacion_id, amenidad_id)
SELECT h.id, a.id
FROM reservas_habitacion h
CROSS JOIN reservas_amenidad a;

-- ============================================
-- CLIENTE (DEBE IR EN sitio_web_cliente)
-- ============================================



INSERT INTO sitio_web_cliente 
(usuario_id, direccion_id, telefono, fecha_nacimiento, fecha_registro, activo)
VALUES (
    1,
    1,
    '88888888',
    NULL,
    NOW(),
    1
);




-- ============================================
-- RESERVAS Y FECHAS RESERVADAS
-- ============================================

-- 🔸 Crear una reserva para cada habitación excepto la 1 y la 8
INSERT INTO reservas_reserva (cliente_id, habitacion_id, fecha_inicio, fecha_fin, total, canal_reservacion, metodo_pago)
SELECT 
    (SELECT id FROM sitio_web_cliente ORDER BY id LIMIT 1) AS cliente_id,
    id,
    '2025-11-09',
    '2025-11-10',
    100,
    'sitio',
    'efectivo'
FROM reservas_habitacion
WHERE id NOT IN (1,8);

-- 🔸 Registrar las fechas reservadas
INSERT INTO reservas_fechareservada (habitacion_id, fecha, reserva_id)
SELECT r.habitacion_id, '2025-11-09', r.id FROM reservas_reserva r
UNION ALL
SELECT r.habitacion_id, '2025-11-10', r.id FROM reservas_reserva r;

-- ============================================
-- PRECIOS POR HABITACIÓN (desde 2025-11-08 hasta 2026-12-31)
-- ============================================

-- 🔸 Crear tabla temporal de fechas
DROP TEMPORARY TABLE IF EXISTS fechas_temp;
CREATE TEMPORARY TABLE fechas_temp (fecha DATE);

INSERT INTO fechas_temp (fecha)
SELECT DATE_ADD('2025-11-08', INTERVAL t.n DAY)
FROM (
    SELECT a.N + b.N * 10 + c.N * 100 AS n
    FROM 
        (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
         UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) a,
        (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
         UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) b,
        (SELECT 0 AS N UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 
         UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) c
) AS t
WHERE DATE_ADD('2025-11-08', INTERVAL t.n DAY) <= '2026-12-31';

-- 🔸 Insertar precios según temporada
INSERT INTO reservas_preciohabitacion (habitacion_id, fecha, precio)
SELECT h.id,
       f.fecha,
       CASE
           WHEN MONTH(f.fecha) IN (12,1,2,3,4,5) THEN
               CASE
                   WHEN h.id IN (1,2) THEN 80
                   WHEN h.id = 3 THEN 100
                   WHEN h.id IN (4,6) THEN 120
                   WHEN h.id IN (7,8) THEN 140
                   ELSE 60
               END
           ELSE
               CASE
                   WHEN h.id IN (1,2) THEN 60
                   WHEN h.id = 3 THEN 80
                   WHEN h.id IN (4,6) THEN 100
                   WHEN h.id IN (7,8) THEN 120
                   ELSE 60
               END
       END AS precio
FROM reservas_habitacion h
JOIN fechas_temp f;

-- 🔸 Limpieza temporal
DROP TEMPORARY TABLE fechas_temp;

