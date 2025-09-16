create database if not exists HotelLuz;
use HotelLuz;

-- ============================================
-- DROP TABLES (para reiniciar la BD si existe)
-- ============================================
DROP TABLE IF EXISTS Campania_Marketing;
DROP TABLE IF EXISTS Reporte;
DROP TABLE IF EXISTS Usuario_Admin;
DROP TABLE IF EXISTS Contabilidad;
DROP TABLE IF EXISTS Inventario;
DROP TABLE IF EXISTS Limpieza;
DROP TABLE IF EXISTS Empleado;
DROP TABLE IF EXISTS Reserva;
DROP TABLE IF EXISTS Habitacion;
DROP TABLE IF EXISTS Tipo_Habitacion;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Metodo_Pago;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Categoria;
DROP TABLE IF EXISTS Rol;
DROP TABLE IF EXISTS Estado;
DROP TABLE IF EXISTS Direccion;
DROP TABLE IF EXISTS Pais;
DROP TABLE IF EXISTS Provincia;
DROP TABLE IF EXISTS Canton;
DROP TABLE IF EXISTS Distrito;

-- ============================================
-- CREACIÓN DE TABLAS
-- ============================================
CREATE TABLE Pais (
  Id_Pais INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Pais VARCHAR(100)
);

CREATE TABLE Provincia (
  Id_Provincia INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Provincia VARCHAR(100)
);

CREATE TABLE Canton (
  Id_Canton INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Canton VARCHAR(100)
);

CREATE TABLE Distrito (
  Id_Distrito INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Distrito VARCHAR(100)
);

CREATE TABLE Direccion (
  Id_Direccion INT PRIMARY KEY AUTO_INCREMENT,
  Direccion_exacta VARCHAR(100),
  Id_Pais INT,
  Id_Provincia INT,
  Id_Canton INT,
  Id_Distrito INT,
  FOREIGN KEY (Id_Pais) REFERENCES Pais(Id_Pais),
  FOREIGN KEY (Id_Provincia) REFERENCES Provincia(Id_Provincia),
  FOREIGN KEY (Id_Canton) REFERENCES Canton(Id_Canton),
  FOREIGN KEY (Id_Distrito) REFERENCES Distrito(Id_Distrito)
);

CREATE TABLE Estado (
  Id_Estado INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Estado VARCHAR(100)
);

CREATE TABLE Cliente (
  Id_Cliente INT PRIMARY KEY AUTO_INCREMENT,
  Nombre VARCHAR(100),
  Apellido VARCHAR(100),
  Telefono VARCHAR(15),
  Correo VARCHAR(100),
  Identificacion VARCHAR(20),
  Fecha_Nacimiento DATE
);

CREATE TABLE Rol (
  Id_Rol INT PRIMARY KEY AUTO_INCREMENT,
  Mombre_Rol VARCHAR(100)
);

CREATE TABLE Tipo_Habitacion (
  Id_Tipo_Habitacion INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Tipo VARCHAR(100)
);

CREATE TABLE Habitacion (
  Id_Habitacion INT PRIMARY KEY AUTO_INCREMENT,
  Id_Estado INT,
  Id_Tipo_Habitacion INT,
  Numero VARCHAR(10),
  Precio DECIMAL(10,2),
  Desayuno_Incluido BOOLEAN,
  FOREIGN KEY (Id_Estado) REFERENCES Estado(Id_Estado),
  FOREIGN KEY (Id_Tipo_Habitacion) REFERENCES Tipo_Habitacion(Id_Tipo_Habitacion)
);

CREATE TABLE Metodo_Pago (
  Id_Metodo_Pago INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Metodo_Pago VARCHAR(100)
);

CREATE TABLE Reserva (
  Id_Reserva INT PRIMARY KEY AUTO_INCREMENT,
  Id_Cliente INT,
  Id_Habitacion INT,
  Id_Metodo_Pago INT,
  Id_Estado INT,
  Fecha_Inicio DATE,
  Fecha_Fin DATE,
  Canal_Reserva VARCHAR(50),
  Total DECIMAL(10,2),
  FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente),
  FOREIGN KEY (Id_Habitacion) REFERENCES Habitacion(Id_Habitacion),
  FOREIGN KEY (Id_Metodo_Pago) REFERENCES Metodo_Pago(Id_Metodo_Pago),
  FOREIGN KEY (Id_Estado) REFERENCES Estado(Id_Estado)
);

CREATE TABLE Empleado (
  Id_Empleado INT PRIMARY KEY AUTO_INCREMENT,
  Id_Rol INT,
  Id_Direccion INT,
  Nombre VARCHAR(100),
  Apellido VARCHAR(100),
  Cedula VARCHAR(20),
  Telefono VARCHAR(15),
  Correo VARCHAR(100),
  Fecha_Contratacion DATE,
  Salario DECIMAL(10,2),
  FOREIGN KEY (Id_Rol) REFERENCES Rol(Id_Rol),
  FOREIGN KEY (Id_Direccion) REFERENCES Direccion(Id_Direccion)
);

CREATE TABLE Limpieza (
  Id_Limpieza INT PRIMARY KEY AUTO_INCREMENT,
  Id_Empleado INT,
  Id_Habitacion INT,
  Id_Estado INT,
  Fecha DATE,
  Observaciones VARCHAR(255),
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id_Empleado),
  FOREIGN KEY (Id_Habitacion) REFERENCES Habitacion(Id_Habitacion),
  FOREIGN KEY (Id_Estado) REFERENCES Estado(Id_Estado)
);

CREATE TABLE Categoria (
  Id_Categoria INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Categoria VARCHAR(100)
);

CREATE TABLE Producto (
  Id_Producto INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Producto VARCHAR(100),
  Id_Categoria INT,
  FOREIGN KEY (Id_Categoria) REFERENCES Categoria(Id_Categoria)
);

CREATE TABLE Inventario (
  Id_Inventario INT PRIMARY KEY AUTO_INCREMENT,
  Id_Estado INT,
  Id_Producto INT,
  Nombre_Item VARCHAR(100),
  Categoria VARCHAR(50),
  Cantidad INT,
  Unidad VARCHAR(20),
  Fecha_Ingreso DATE,
  FOREIGN KEY (Id_Estado) REFERENCES Estado(Id_Estado),
  FOREIGN KEY (Id_Producto) REFERENCES Producto(Id_Producto)
);

CREATE TABLE Contabilidad (
  Id_Transaccion INT PRIMARY KEY AUTO_INCREMENT,
  Fecha DATE,
  Tipo VARCHAR(20),
  Monto DECIMAL(10,2),
  Categoria VARCHAR(50),
  Descripcion VARCHAR(255),
  Id_Reserva INT,
  FOREIGN KEY (Id_Reserva) REFERENCES Reserva(Id_Reserva)
);

CREATE TABLE Usuario_Admin (
  Id_Usuario INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Usuario VARCHAR(50),
  Contrasena VARCHAR(100),
  Id_Empleado INT,
  Id_Rol INT,
  FOREIGN KEY (Id_Empleado) REFERENCES Empleado(Id_Empleado),
  FOREIGN KEY (Id_Rol) REFERENCES Rol(Id_Rol)
);

CREATE TABLE Reporte (
  Id_Reporte INT PRIMARY KEY AUTO_INCREMENT,
  Tipo_Reporte VARCHAR(50),
  Fecha_Generacion DATE,
  Id_Usuario INT,
  Detalle TEXT,
  FOREIGN KEY (Id_Usuario) REFERENCES Usuario_Admin(Id_Usuario)
);

CREATE TABLE Campania_Marketing (
  Id_Campania INT PRIMARY KEY AUTO_INCREMENT,
  Nombre VARCHAR(100),
  Fecha_Inicio DATE,
  Fecha_Fin DATE,
  Canal VARCHAR(50),
  Presupuesto DECIMAL(10,2),
  Id_Estado INT,
  FOREIGN KEY (Id_Estado) REFERENCES Estado(Id_Estado)
);

-- ============================================
-- INSERTS DE EJEMPLO (Costa Rica)
-- ============================================

-- País
INSERT INTO Pais (Nombre_Pais) VALUES ('Costa Rica');

-- Provincias
INSERT INTO Provincia (Nombre_Provincia) VALUES 
('San José'), ('Alajuela'), ('Cartago'),
('Heredia'), ('Guanacaste'), ('Puntarenas'), ('Limón');

-- Cantones
INSERT INTO Canton (Nombre_Canton) VALUES
('Central San José'), ('Central Alajuela'), ('Central Cartago'),
('Central Heredia'), ('Liberia'), ('Central Puntarenas'), ('Central Limón');

-- Distritos
INSERT INTO Distrito (Nombre_Distrito) VALUES
('Carmen'), ('Alajuela'), ('Oriental'),
('Heredia'), ('Liberia'), ('Puntarenas'), ('Limón');

-- Direcciones
INSERT INTO Direccion (Direccion_exacta, Id_Pais, Id_Provincia, Id_Canton, Id_Distrito) VALUES
('Avenida Central, frente al Teatro Nacional', 1, 1, 1, 1),
('200m norte del Parque Central de Alajuela', 1, 2, 2, 2),
('Calle 5, Cartago centro', 1, 3, 3, 3),
('Costado oeste del Parque Central, Heredia', 1, 4, 4, 4);

-- Estados
INSERT INTO Estado (Nombre_Estado) VALUES
('Activo'), ('Inactivo'), ('Ocupado'),
('Disponible'), ('Pendiente'), ('Finalizado'), ('En Limpieza');

-- Clientes
INSERT INTO Cliente (Nombre, Apellido, Telefono, Correo, Identificacion, Fecha_Nacimiento) VALUES
('Carlos', 'Jiménez', '88881234', 'carlos.jimenez@gmail.com', '1-1234-0567', '1990-05-15'),
('María', 'Fernández', '85263478', 'maria.fernandez@yahoo.com', '2-0456-0789', '1985-09-23'),
('José', 'Ramírez', '89992345', 'jose.ramirez@hotmail.com', '1-2345-0678', '2000-01-12');

-- Roles
INSERT INTO Rol (Mombre_Rol) VALUES
('Administrador'), ('Recepcionista'), ('Limpieza'), ('Contador'), ('Marketing');

-- Empleados
INSERT INTO Empleado (Id_Rol, Id_Direccion, Nombre, Apellido, Cedula, Telefono, Correo, Fecha_Contratacion, Salario) VALUES
(1, 1, 'Laura', 'Soto', '1-0456-0789', '88884567', 'laura.soto@hotelcr.com', '2020-03-01', 1200000.00),
(2, 2, 'Pedro', 'Chavarría', '1-0789-1234', '88774567', 'pedro.chavarria@hotelcr.com', '2021-06-15', 600000.00),
(3, 3, 'Ana', 'López', '2-0567-0987', '89994567', 'ana.lopez@hotelcr.com', '2019-08-20', 450000.00);

-- Tipos de habitación
INSERT INTO Tipo_Habitacion (Nombre_Tipo) VALUES
('Sencilla'), ('Doble'), ('Suite');

-- Habitaciones
INSERT INTO Habitacion (Id_Estado, Id_Tipo_Habitacion, Numero, Precio, Desayuno_Incluido) VALUES
(4, 1, '101', 45000.00, TRUE),
(4, 2, '102', 65000.00, TRUE),
(3, 3, '201', 120000.00, TRUE);

-- Métodos de pago
INSERT INTO Metodo_Pago (Nombre_Metodo_Pago) VALUES
('Tarjeta de Crédito'), ('Tarjeta de Débito'), ('Efectivo'), ('Transferencia Bancaria');

-- Reservas
INSERT INTO Reserva (Id_Cliente, Id_Habitacion, Id_Metodo_Pago, Id_Estado, Fecha_Inicio, Fecha_Fin, Canal_Reserva, Total) VALUES
(1, 1, 1, 1, '2025-09-20', '2025-09-25', 'Página Web', 225000.00),
(2, 2, 2, 5, '2025-10-01', '2025-10-03', 'Booking', 130000.00);

-- Limpieza
INSERT INTO Limpieza (Id_Empleado, Id_Habitacion, Id_Estado, Fecha, Observaciones) VALUES
(3, 1, 7, '2025-09-15', 'Habitación desinfectada, todo en orden'),
(3, 2, 7, '2025-09-14', 'Cambio de sábanas y limpieza general');

-- Categorías
INSERT INTO Categoria (Nombre_Categoria) VALUES
('Aseo'), ('Alimentos'), ('Tecnología');

-- Productos
INSERT INTO Producto (Nombre_Producto, Id_Categoria) VALUES
('Jabón Líquido', 1), ('Café Britt', 2), ('Televisor LG 42"', 3);

-- Inventario
INSERT INTO Inventario (Id_Estado, Id_Producto, Nombre_Item, Categoria, Cantidad, Unidad, Fecha_Ingreso) VALUES
(1, 1, 'Jabón Líquido', 'Aseo', 50, 'botellas', '2025-09-01'),
(1, 2, 'Café Britt', 'Alimentos', 20, 'paquetes', '2025-09-05'),
(1, 3, 'Televisor LG 42"', 'Tecnología', 5, 'unidades', '2025-08-20');

-- Contabilidad
INSERT INTO Contabilidad (Fecha, Tipo, Monto, Categoria, Descripcion, Id_Reserva) VALUES
('2025-09-20', 'Ingreso', 225000.00, 'Reserva', 'Reserva de Carlos Jiménez', 1),
('2025-10-01', 'Ingreso', 130000.00, 'Reserva', 'Reserva de María Fernández', 2),
('2025-09-10', 'Gasto', 50000.00, 'Mantenimiento', 'Reparación aire acondicionado', NULL);

-- Usuarios Admin
INSERT INTO Usuario_Admin (Nombre_Usuario, Contrasena, Id_Empleado, Id_Rol) VALUES
('admin1', '1234seguro', 1, 1),
('recep1', 'recepcion2025', 2, 2);

-- Reportes
INSERT INTO Reporte (Tipo_Reporte, Fecha_Generacion, Id_Usuario, Detalle) VALUES
('Ocupación Hotel', '2025-09-16', 1, 'Actualmente 80% de ocupación en temporada alta'),
('Inventario', '2025-09-10', 1, 'Stock de café Britt bajo, quedan 20 paquetes');

-- Campañas de Marketing
INSERT INTO Campania_Marketing (Nombre, Fecha_Inicio, Fecha_Fin, Canal, Presupuesto, Id_Estado) VALUES
('Campaña Facebook Septiembre', '2025-09-01', '2025-09-30', 'Facebook', 100000.00, 1),
('Campaña Google Ads Octubre', '2025-10-01', '2025-10-31', 'Google Ads', 200000.00, 5);
