"""
Simple translations mapping for the `sitio_web` module.

This is intentionally small and only covers the strings used in the sitio_web
templates per the user story. We keep a simple dict here to avoid requiring
gettext/po files for the quick HU implementation.
"""

TRANSLATIONS = {
    # Nav / common
    'Inicio': {'es': 'Inicio', 'en': 'Home'},
    'Habitaciones': {'es': 'Habitaciones', 'en': 'Rooms'},
    'Servicios': {'es': 'Servicios', 'en': 'Services'},
    'Reservaciones': {'es': 'Reservaciones', 'en': 'Bookings'},
    'Actividades': {'es': 'Actividades', 'en': 'Activities'},
    'Contacto': {'es': 'Contacto', 'en': 'Contact'},
    'Iniciar sesión': {'es': 'Iniciar sesión', 'en': 'Log in'},
    'Registrarse': {'es': 'Registrarse', 'en': 'Sign up'},
    'Perfil': {'es': 'Perfil', 'en': 'Profile'},
    'Cerrar sesión': {'es': 'Cerrar sesión', 'en': 'Log out'},
    'Hola,': {'es': 'Hola,', 'en': 'Hello,'},

    # Index / hero
    'Bienvenido al Hotel Luz de Luna': {
        'es': 'Bienvenido al Hotel Luz de Luna',
        'en': 'Welcome to Hotel Luz de Luna'
    },
    'Disfruta de una experiencia única de descanso y confort en un entorno natural y tranquilo.': {
        'es': 'Disfruta de una experiencia única de descanso y confort en un entorno natural y tranquilo.',
        'en': 'Enjoy a unique experience of rest and comfort in a peaceful natural setting.'
    },

    # Habitaciones
    'Nuestras Habitaciones': {'es': 'Nuestras Habitaciones', 'en': 'Our Rooms'},
    'Confort, elegancia y vista panorámica en cada una de nuestras habitaciones.': {
        'es': 'Confort, elegancia y vista panorámica en cada una de nuestras habitaciones.',
        'en': 'Comfort, elegance and panoramic views in each of our rooms.'
    },
    'Ver todas las habitaciones': {'es': 'Ver todas las habitaciones', 'en': 'View all rooms'},
    'No hay habitaciones disponibles en este momento.': {
        'es': 'No hay habitaciones disponibles en este momento.',
        'en': 'There are no rooms available at this time.'
    },

    # -------------------------------
    # PÁRRAFOS DINÁMICOS (DESCRIPCIÓN)
    # -------------------------------
    "Suite amplia con balcón y vista al mar, decoración elegante y cama king-size. Ideal para parejas.": {
        "es": "Suite amplia con balcón y vista al mar, decoración elegante y cama king-size. Ideal para parejas.",
        "en": "Spacious suite with balcony and sea view, elegant decor and king-size bed. Ideal for couples."
    },
    "Espacio acogedor con acceso directo al jardín del hotel, ideal para quienes buscan tranquilidad.": {
        "es": "Espacio acogedor con acceso directo al jardín del hotel, ideal para quienes buscan tranquilidad.",
        "en": "Cozy space with direct access to the hotel garden, ideal for those seeking tranquility."
    },
    "Habitación amplia con dos camas y sofá cama, perfecta para familias pequeñas.": {
        "es": "Habitación amplia con dos camas y sofá cama, perfecta para familias pequeñas.",
        "en": "Spacious room with two beds and a sofa bed, perfect for small families."
    },
    "Habitación premium con grandes ventanales y excelente iluminación natural.": {
        "es": "Habitación premium con grandes ventanales y excelente iluminación natural.",
        "en": "Premium room with large windows and excellent natural lighting."
    },
    "Habitación funcional y acogedora con lo esencial para una estadía placentera.": {
        "es": "Habitación funcional y acogedora con lo esencial para una estadía placentera.",
        "en": "Functional and cozy room with the essentials for a pleasant stay."
    },
    "Suite pequeña con área de estar y una cama queen, perfecta para ejecutivos.": {
        "es": "Suite pequeña con área de estar y una cama queen, perfecta para ejecutivos.",
        "en": "Small suite with sitting area and a queen bed, perfect for executives."
    },
    "Opción económica con lo esencial para una estancia corta y funcional.": {
        "es": "Opción económica con lo esencial para una estancia corta y funcional.",
        "en": "Economical option with the essentials for a short and functional stay."
    },

    # Actividades
    'Disfruta de las mejores experiencias cerca del hotel.': {
        'es': 'Disfruta de las mejores experiencias cerca del hotel.',
        'en': 'Enjoy the best experiences near the hotel.'
    },
    'Tour a las Cataratas': {'es': 'Tour a las Cataratas', 'en': 'Waterfall Tour'},
    'Explora hermosas cascadas y senderos naturales cerca del hotel.': {
        'es': 'Explora hermosas cascadas y senderos naturales cerca del hotel.',
        'en': 'Explore beautiful waterfalls and nature trails near the hotel.'
    },
    'Tour de Café': {'es': 'Tour de Café', 'en': 'Coffee Tour'},
    'Aprende sobre el proceso del café costarricense con degustación incluida.': {
        'es': 'Aprende sobre el proceso del café costarricense con degustación incluida.',
        'en': 'Learn about Costa Rican coffee processing with a tasting included.'
    },
    'Cabalgata Ecológica': {'es': 'Cabalgata Ecológica', 'en': 'Eco Horseback Ride'},
    'Vive una experiencia natural a caballo por los alrededores del valle.': {
        'es': 'Vive una experiencia natural a caballo por los alrededores del valle.',
        'en': 'Enjoy a nature experience on horseback around the valley.'
    },

    # Reservar
    'Reservar ahora': {'es': 'Reservar ahora', 'en': 'Book now'},

    # Amenidades
    "Cama grande": {
        "es": "Cama grande",
        "en": "Large bed",
    },
    "Cama pequeña": {
        "es": "Cama pequeña",
        "en": "Small bed",
    },
    "Wi-Fi": {
        "es": "Wi-Fi",
        "en": "Wi-Fi",
    },
    "Hamaca": {
        "es": "Hamaca",
        "en": "Hammock",
    },
    "Refrigeradora": {
        "es": "Refrigeradora",
        "en": "Fridge",
    },
    "Parqueo": {
        "es": "Parqueo",
        "en": "Parking",
    },
    "Cocina": {
        "es": "Cocina",
        "en": "Kitchen",
    },
    "Piscina": {
        "es": "Piscina",
        "en": "Pool",
    },

    # habitaciones
    "Habitación 1": {
        "es": "Habitación 1",  
        "en": "Room 1",
    },
    "Habitación 2": {
        "es": "Habitación 2",  
        "en": "Room 2",
    },
    "Habitación 3": {
        "es": "Habitación 3",  
        "en": "Room 3",
    },
    "Habitación 4": {
        "es": "Habitación 4",  
        "en": "Room 4",
    },
    "Habitación 5": {
        "es": "Habitación 5",  
        "en": "Room 5",
    },
    "Habitación 6": {
        "es": "Habitación 6",  
        "en": "Room 6",
    },
    "Habitación 7": {
        "es": "Habitación 7",  
        "en": "Room 7",
    },
    "Habitación 8": {
        "es": "Habitación 8",  
        "en": "Room 8",
    },
    "Buscar": {
        "es": "Buscar",
        "en": "Search",
    },
    "Buscar por nombre o amenidad": {
        "es": "Buscar por nombre o amenidad",
        "en": "Search by name or amenity",
    }
}


# Additional keys added to cover more templates
TRANSLATIONS.update({
    'Servicios del Hotel': {'es': 'Servicios del Hotel', 'en': 'Hotel Services'},
    'Restaurante gourmet': {'es': 'Restaurante gourmet', 'en': 'Gourmet restaurant'},
    'Piscina al aire libre': {'es': 'Piscina al aire libre', 'en': 'Outdoor pool'},
    'Spa y masajes relajantes': {'es': 'Spa y masajes relajantes', 'en': 'Spa and relaxing massages'},
    'Wi-Fi gratuito': {'es': 'Wi-Fi gratuito', 'en': 'Free Wi-Fi'},
    'Ver más actividades': {'es': 'Ver más actividades', 'en': 'See more activities'},
    'Contáctanos': {'es': 'Contáctanos', 'en': 'Contact us'},
    'Teléfono': {'es': 'Teléfono', 'en': 'Phone'},
    'Correo electrónico': {'es': 'Correo electrónico', 'en': 'Email'},
    'Correo electrónico:': {'es': 'Correo electrónico:', 'en': 'Email:'},
    'WhatsApp': {'es': 'WhatsApp', 'en': 'WhatsApp'},
    'Dirección': {'es': 'Dirección', 'en': 'Address'},
    'Dirección:': {'es': 'Dirección:', 'en': 'Address:'},
    'Consultar Disponibilidad': {'es': 'Consultar Disponibilidad', 'en': 'Check availability'},
    'Fecha de Inicio': {'es': 'Fecha de Inicio', 'en': 'Start date'},
    'Fecha de Fin': {'es': 'Fecha de Fin', 'en': 'End date'},
    'Tipo de Habitación': {'es': 'Tipo de Habitación', 'en': 'Room type'},
    'Habitación': {'es': 'Habitación', 'en': 'Room'},
    'Amenidades': {'es': 'Amenidades', 'en': 'Amenities'},
    'Precio Total': {'es': 'Precio Total', 'en': 'Total Price'},
    'Acción': {'es': 'Acción', 'en': 'Action'},
    'Ver Detalles': {'es': 'Ver Detalles', 'en': 'View Details'},
    'Reservar': {'es': 'Reservar', 'en': 'Book'},
    'Sin amenidades': {'es': 'Sin amenidades', 'en': 'No amenities'},
    'No hay habitaciones disponibles en el rango seleccionado.': {
        'es': 'No hay habitaciones disponibles en el rango seleccionado.',
        'en': 'There are no rooms available in the selected range.'
    },
    'Volver': {'es': 'Volver', 'en': 'Back'},
    'Amenidades': {'es': 'Amenidades', 'en': 'Amenities'},
    'Máx.': {'es': 'Máx.', 'en': 'Max.'},
    'personas': {'es': 'personas', 'en': 'people'},
    'Ubicación': {'es': 'Ubicación', 'en': 'Location'},
    'Ubicación:': {'es': 'Ubicación:', 'en': 'Location:'},
    'Precio aproximado:': {'es': 'Precio aproximado', 'en': 'Approx. price'},
    'Cama grande': {'es': 'Cama grande', 'en': 'King bed'},
    'Cama pequeña': {'es': 'Cama pequeña', 'en': 'Small bed'},
    'nombre:': {'es': 'Nombre', 'en': 'Name'},
    'mensaje': {'es': 'Mensaje', 'en': 'Message'},
    'Mensaje:': {'es': 'Mensaje:', 'en': 'Message:'},
    'Enviar': {'es': 'Enviar', 'en': 'Send'},
    'Enviar:': {'es': 'Enviar:', 'en': 'Send:'},
    'Encuéntranos fácilmente en el mapa:': {'es': 'Encuéntranos fácilmente en el mapa:', 'en': 'Find us easily on the map: '},
    'Estamos aquí para ayudarte. Puedes comunicarte con nosotros mediante cualquiera de los siguientes medios:': 
    {'es': 'Estamos aquí para ayudarte. Puedes comunicarte con nosotros mediante cualquiera de los siguientes medios:', 
     'en': 'We are here to help you. You can contact us through any of the following means:'},
     'Información de contacto': 
    {'es': 'Información de contacto', 
     'en': 'Contact Information'},
     'Iniciar Sesión': {'es': 'Iniciar Sesión', 'en': 'Log In'},
     'Volver al inicio': {'es': 'Volver al inicio', 'en': 'Back to Home'},
     '¿No tienes cuenta?': {'es': '¿No tienes cuenta?', 'en': 'Don\'t have an account?'},
     'Regístrate aquí': {'es': 'Regístrate aquí', 'en': 'Register here'},
     'Correo': {'es': 'Correo', 'en': 'Email'},
     'Contraseña': {'es': 'Contraseña', 'en': 'Password'},  
     'Haz tu reserva fácilmente en línea o contáctanos para más información.': {
        'es': 'Haz tu reserva fácilmente en línea o contáctanos para más información.',
        'en': 'Make your reservation easily online or contact us for more information.'},

     #Registro de cliente
     'Registro de Cliente': {'es': 'Registro de Cliente', 'en': 'Client Registration'},     
     'Datos de Usuario': {'es': 'Datos de Usuario', 'en': 'User Data'},
     'Información de Contacto': 
    {'es': 'Información de Contacto', 
     'en': 'Contact Information'},
     'Registrar': {'es': 'Registrarse', 'en': 'Sign Up'},

     #Perfil de cliente
     'Nombre completo': {'es': 'Nombre completo', 'en': 'Full Name'},
     'Editar perfil': {'es': 'Editar perfil', 'en': 'Edit profile'},
     'Confirmar Reserva': {'es': 'Confirmar Reserva',
                            'en': 'Confirm Booking'},
    'Cancelar': {'es': 'Cancelar', 'en': 'Cancel'},
    'Cédula': {'es': 'Cédula', 'en': 'ID Card' },
    'Nombre:': {'es': 'Nombre', 'en': 'Name'},
    'Amenidades:': {'es': 'Amenidades', 'en': 'Amenities'},
    'Detalles de la habitación': {'es': 'Detalles de la habitación', 'en': 'Room Details'},
    'Contacto:': {'es': 'Contacto:', 'en': 'Contact:'},
    '8 minutos del hotel': {'es': '8 minutos del hotel', 'en': '8 minutes from the hotel'},
    '10 minutos del hotel': {'es': '10 minutos del hotel', 'en': '10 minutes from the hotel'},
    '15 minutos del hotel': {'es': '15 minutos del hotel', 'en': '15 minutes from the hotel'},
    '$25 por persona': {'es': 'por persona', 'en': 'per person'},
    '$20 por persona': {'es': '$20 por persona', 'en': '$20 per person'},
    '$30 por persona': {'es': '$30 por persona', 'en': '$30 per person'},
    'Teléfono:': {'es': 'Teléfono:', 'en': 'Telephone:'},
    'Formulario de contacto': {'es': 'Formulario de contacto', 'en': 'Contact form'},
    'Consultar Disponibilidad': {'es': 'Consultar Disponibilidad', 'en': 'Check Availability'},
                            
        'Número:': {'es': 'Número:', 'en': 'Number:'},
        'Descripción:': {'es': 'Descripción:', 'en': 'Description:'},
        'Sin amenidades registradas': {'es': 'Sin amenidades registradas', 'en': 'No amenities registered'},
        'Precios por fecha': {'es': 'Precios por fecha', 'en': 'Prices by date'},
                    
})
