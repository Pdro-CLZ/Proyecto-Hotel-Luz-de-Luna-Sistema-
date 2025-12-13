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

use hotelprojectbd;
INSERT INTO administracion_rol (nombre, descripcion, activo) VALUES
('Administrador', 'Rol con todos los permisos', 1),
('Empleado_Nivel1', 'Empleado nivel 1', 1),
('Empleado_Nivel2', 'Empleado nivel 2', 1),
('Cliente', 'Cliente del hotel', 1);
-- ==============================================
-- ==============================================
-- ==============================================






-- ==============================================
-- De segundo, despues de migrate + runserver
-- ==============================================
-- ====================================
-- APP PERSONAL
-- ====================================

-- Paises
INSERT INTO personal_pais (nombre) VALUES
('Costa Rica');  

-- Provincias
INSERT INTO personal_provincia (nombre) VALUES
('Puntarenas');  

-- Cantones
INSERT INTO personal_canton (nombre) VALUES
('Cóbano'); 

-- Distritos de Cóbano
INSERT INTO personal_distrito (nombre) VALUES
('San Isidro'),
('Santa Teresa'),
('Montezuma'),
('Paquera'),
('Lepanto');

-- Direcciones
INSERT INTO personal_direccion (direccion_exacta, pais_id, provincia_id, canton_id, distrito_id) VALUES
('Calle Principal, San Isidro', 1, 1, 1, 1),
('Avenida Central, Santa Teresa', 1, 1, 1, 2),
('Residencial Montezuma 23', 1, 1, 1, 3),
('Barrio Paquera, Casa 5', 1, 1, 1, 4),
('Urbanización Lepanto, Casa 12', 1, 1, 1, 5);

-- Empleados
INSERT INTO personal_empleado (usuario_id, direccion_id, nombre, apellido, telefono, correo, fecha_contratacion, salario, activo) VALUES
(2, 1, 'Carlos', 'Pérez', '88881234', 'carlos.perez@email.com', '2023-01-10', 500000, 1),
(3, 2, 'Ana', 'Gómez', '88882345', 'ana.gomez@email.com', '2023-03-05', 450000, 1),
(4, 3, 'Luis', 'Ramírez', '88883456', 'luis.ramirez@email.com', '2022-07-12', 480000, 1),
(1, 5, 'Jorge', 'Molina', '88885678', 'jorge.molina@email.com', '2022-11-25', 460000, 1);

-- Asistencias
INSERT INTO personal_asistencia (empleado_id, fecha, hora_llegada, hora_salida, horas_trabajadas, observaciones) VALUES
(1, '2025-12-10', '08:00:00', '16:00:00', 8, 'Todo normal'),
(2, '2025-12-10', '08:15:00', '16:15:00', 8, NULL),
(3, '2025-12-10', '07:50:00', '15:50:00', 8, 'Llegó temprano'),
(4, '2025-12-10', '08:10:00', '16:10:00', 8, NULL);


-- ====================================
-- APP CONTABILIDAD
-- ====================================

-- Contabilidad
INSERT INTO contabilidad_contabilidad (fecha, tipo, metodo_pago, monto, categoria, descripcion) VALUES
('2025-12-01', 'Ingreso', 'Efectivo', 100000, 'Ventas', 'Venta de producto A'),
('2025-12-02', 'Gasto', 'Tarjeta', 50000, 'Compra', 'Compra de insumos'),
('2025-12-03', 'Ingreso', 'Transferencia', 75000, 'Servicios', 'Servicio de consultoría'),
('2025-12-04', 'Gasto', 'Efectivo', 30000, 'Mantenimiento', 'Reparación equipo'),
('2025-12-05', 'Ingreso', 'Efectivo', 120000, 'Ventas', 'Venta de producto B');

-- CierreMensual
INSERT INTO contabilidad_cierremensual (mes, anio, total_ingresos, total_gastos, utilidad, fecha_cierre) VALUES
(1, 2025, 500000, 200000, 300000, NOW()),
(2, 2025, 600000, 250000, 350000, NOW()),
(3, 2025, 550000, 220000, 330000, NOW()),
(4, 2025, 580000, 240000, 340000, NOW()),
(5, 2025, 620000, 260000, 360000, NOW());

-- CierreAnual
INSERT INTO contabilidad_cierreanual (anio, total_ingresos, total_gastos, utilidad, fecha_cierre) VALUES
(2024, 7000000, 3000000, 4000000, NOW()),
(2025, 7500000, 3200000, 4300000, NOW()),
(2023, 6800000, 2900000, 3900000, NOW()),
(2022, 6500000, 2800000, 3700000, NOW()),
(2021, 6200000, 2700000, 3500000, NOW());


-- ====================================
-- APP INVENTARIO
-- ====================================

INSERT INTO inventario_inventario (nombre, descripcion, tipo, cantidad, activo, fecha_creacion) VALUES
('Laptop Dell', 'Laptop para oficina', 'Activo', 10, 1, NOW()),
('Silla oficina', 'Silla ergonómica', 'Activo', 15, 1, NOW()),
('Papel A4', 'Paquete de 500 hojas', 'Insumo', 50, 1, NOW()),
('Tinta impresora', 'Cartucho negro HP', 'Insumo', 30, 1, NOW()),
('Proyector', 'Proyector multimedia', 'Activo', 5, 1, NOW());


-- ====================================
-- APP LIMPIEZA
-- ====================================

-- ZonaLimpieza

INSERT INTO limpieza_zonalimpieza (nombre, detalles, usuario_registro_id, estado, fecha_registro, is_habitacion) VALUES
('Lobby', 'Zona de recepción', 2, 'Disponible', NOW(), 0),
('Habitación 101', 'Habitación estándar', 3, 'No disponible', NOW(), 1),
('Pasillo Principal', 'Pasillo del primer piso', 2, 'Disponible', NOW(), 0),
('Cocina', 'Cocina del personal', 3, 'Disponible', NOW(), 0),
('Habitación 102', 'Habitación suite', 1, 'No disponible', NOW(), 1);


-- TareaLimpieza
INSERT INTO limpieza_zonalimpieza 
(nombre, detalles, usuario_registro_id, estado, fecha_registro, is_habitacion) VALUES
('Lobby', 'Zona de recepción', 2, 'Disponible', NOW(), 0),
('Habitación 101', 'Habitación estándar', 3, 'No disponible', NOW(), 1),
('Pasillo Principal', 'Pasillo del primer piso', 2, 'Disponible', NOW(), 0),
('Cocina', 'Cocina del personal', 3, 'Disponible', NOW(), 0),
('Habitación 102', 'Habitación suite', 2, 'No disponible', NOW(), 1);



-- ====================================
-- APP MARKETING
-- ====================================

-- ContactoMarketing
INSERT INTO marketing_contactomarketing (nombre, apellido, correo) VALUES
('Luis', 'Martínez', 'luis.martinez@email.com'),
('Ana', 'Rojas', 'ana.rojas@email.com'),
('Carlos', 'Vega', 'carlos.vega@email.com'),
('María', 'López', 'maria.lopez@email.com'),
('Jorge', 'Soto', 'jorge.soto@email.com');

-- PlantillaMarketing
INSERT INTO marketing_plantillamarketing (nombre, asunto, contenido_html, fecha_creacion) VALUES
('Promo Navidad', 'Descuentos navideños', '<p>¡Aprovecha nuestras ofertas!</p>', NOW()),
('Lanzamiento Producto', 'Nuevo producto disponible', '<p>Descubre nuestro producto estrella.</p>', NOW()),
('Recordatorio Pago', 'No olvides tu pago', '<p>Tu factura está pendiente.</p>', NOW()),
('Encuesta Cliente', 'Queremos tu opinión', '<p>Participa en nuestra encuesta.</p>', NOW()),
('Feliz Año', 'Saludos de año nuevo', '<p>Te deseamos un próspero año.</p>', NOW());

-- CampaniaMarketing
INSERT INTO marketing_campaniamarketing (nombre, plantilla_id, fecha_envio, estado) VALUES
('Navidad 2025', 1, NOW(), 'Pendiente'),
('Lanzamiento Enero', 2, NOW(), 'Pendiente'),
('Recordatorio Pagos', 3, NOW(), 'Pendiente'),
('Encuesta Clientes', 4, NOW(), 'Pendiente'),
('Feliz Año 2026', 5, NOW(), 'Pendiente');

-- ====================================
-- APP REPORTERIA
-- ====================================

INSERT INTO reporteria_reporte (tipo_reporte, fecha_generacion, usuario_id, detalle) VALUES
('Asistencia Empleados', '2025-12-10', 2, 'Reporte mensual de asistencia'),
('Ingresos/Gastos', '2025-12-10', 3, 'Reporte financiero de diciembre'),
('Inventario', '2025-12-10', 4, 'Reporte de inventario actual'),
('Limpieza', '2025-12-10', 1, 'Reporte de tareas completadas'),
('Marketing', '2025-12-10', 1, 'Reporte de campañas enviadas');


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

