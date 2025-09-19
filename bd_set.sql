-- 1️⃣ Crear la base de datos
CREATE DATABASE IF NOT EXISTS hotelprojectbd
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2️⃣ Crear el usuario (solo si no existe)
CREATE USER IF NOT EXISTS 'hotel_admin'@'localhost' IDENTIFIED BY '12password34?!';

-- 3️⃣ Darle permisos sobre la base de datos
GRANT ALL PRIVILEGES ON HotelProjectBD.* TO 'hotel_admin'@'localhost';

-- 4️⃣ Aplicar cambios de permisos
FLUSH PRIVILEGES;
