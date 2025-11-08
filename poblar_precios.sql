-- ============================================
-- LIMPIEZA DE DATOS ANTERIORES
-- ============================================
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE reservas_fechareservada;
TRUNCATE TABLE reservas_preciohabitacion;
TRUNCATE TABLE reservas_reserva;
TRUNCATE TABLE reservas_cliente;
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
-- CLIENTE
-- ============================================
INSERT INTO reservas_cliente (nombre, apellido, telefono, correo, identificacion)
VALUES ('Carlos', 'Jiménez', '88888888', 'carlos@example.com', '111111111');

-- ============================================
-- RESERVAS Y FECHAS RESERVADAS
-- ============================================

-- 🔸 Crear una reserva para cada habitación excepto la 1 y la 8
INSERT INTO reservas_reserva (cliente_id, habitacion_id, fecha_inicio, fecha_fin, total)
SELECT 1, id, '2025-11-09', '2025-11-10', 100
FROM reservas_habitacion
WHERE id NOT IN (1,8);

-- 🔸 Registrar las fechas reservadas para esas habitaciones
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
