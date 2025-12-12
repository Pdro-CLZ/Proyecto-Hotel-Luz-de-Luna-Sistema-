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

        'Cerrar': {'es': 'Cerrar', 'en': 'Close'},
        'Anterior': {'es': 'Anterior', 'en': 'Previous'},
        'Siguiente': {'es': 'Siguiente', 'en': 'Next'},

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
                    

        'Surf': {'es': 'Surf', 'en': 'Surf'},
        'Surf description': {
            'es': 'Una de las mayores atracciones de Santa Teresa es el surf. Cuenta con kilómetros de playas vírgenes con varios puntos de surf para principiantes como para surfistas profesionales. Nuestro hotel puede organizar lecciones de surf o un fotógrafo de surf para usted.',
            'en': 'One of the main attractions of Santa Teresa is surfing. It offers kilometers of pristine beaches with surf spots for beginners and professional surfers. Our hotel can arrange surf lessons or a surf photographer for you.'
        },
        'Varios puntos de la costa': {'es': 'Varios puntos de la costa', 'en': 'Various coastal spots'},

        'Yoga': {'es': 'Yoga', 'en': 'Yoga'},
        'Yoga description': {
            'es': 'Para relajarse durante sus vacaciones, usted puede practicar yoga. Varios lugares en Santa Teresa ofrecen clases de yoga de diferentes estilos y niveles. También es perfecto para estirar los músculos para prepararse para el surf.',
            'en': 'To relax during your vacation, you can practice yoga. Several venues in Santa Teresa offer yoga classes of different styles and levels. It is also perfect to stretch the muscles to prepare for surfing.'
        },
        'Varios estudios en la zona': {'es': 'Varios estudios en la zona', 'en': 'Various studios in the area'},

        'Canopy Tour': {'es': 'Canopy Tour', 'en': 'Canopy Tour'},
        'Canopy description': {
            'es': 'Se deslizan a través de las copas de los árboles de la selva en Mal País, junto al Parque Nacional Cabo Blanco. Esta es una aventura alrededor de un kilómetro con 9 cables y 11 plataformas elevadas en los árboles gigantescos.',
            'en': 'Zip through the rainforest treetops in Mal País, next to Cabo Blanco National Park. This is about a one-kilometer adventure with 9 cables and 11 elevated platforms in the giant trees.'
        },

        'SUP': {'es': 'SUP', 'en': 'SUP (Stand-up paddle)'},
        'SUP description': {
            'es': 'Stand-up paddle (SUP) es un gran entrenamiento para todo el cuerpo y es muy fácil de aprender. En el agua, a menudo se ven tortugas, mantarrayas y otras formas de vida marina.',
            'en': 'Stand-up paddle (SUP) is a great full-body workout and very easy to learn. On the water you can often see turtles, manta rays and other marine life.'
        },
        'Costa local': {'es': 'Costa local', 'en': 'Local coast'},

        'ATV Tours': {'es': 'ATV Tours', 'en': 'ATV Tours'},
        'ATV description': {
            'es': 'Alquile una quadra para uno o más días para explorar de forma independiente todas las playas y lugares de interés en la zona de Santa Teresa y Mal País.',
            'en': 'Rent an ATV for one or more days to independently explore all the beaches and points of interest in the Santa Teresa and Mal País area.'
        },

        'Tour a Montezuma': {'es': 'Tour a Montezuma', 'en': 'Montezuma Tour'},
        'Montezuma description': {
            'es': 'La localidad de Playa Montezuma es famosa por sus playas pintorescas, ríos y cascadas. Se puede nadar en las piscinas de la cascada o de un río en la selva, y después ir de compras en el pueblo y tomar el almuerzo o la cena.',
            'en': 'The town of Playa Montezuma is famous for its picturesque beaches, rivers and waterfalls. You can swim in waterfall pools or a jungle river, then shop in town and have lunch or dinner.'
        },

        'Buceo en Isla Tortuga': {'es': 'Buceo en Isla Tortuga', 'en': 'Diving at Tortuga Island'},
        'Tortuga description': {
            'es': 'Un tour de un día completo, con todo incluido, a uno de los mejores puntos de buceo y snorkeling en la costa del Pacífico de Costa Rica. Después de un viaje de 50 minutos a bordo, se llega al paraíso tropical de la Isla Tortuga, donde se puede bucear en las aguas cristalinas.',
            'en': 'A full-day, all-inclusive tour to one of the best diving and snorkeling spots on Costa Rica\'s Pacific coast. After a 50-minute boat trip you arrive at the tropical paradise of Isla Tortuga, where you can dive in crystal-clear waters.'
        },
        'Isla Tortuga': {'es': 'Isla Tortuga', 'en': 'Tortuga Island'},

        'Pesca o Tour en Bote': {'es': 'Pesca o Tour en Bote', 'en': 'Fishing or Boat Tour'},
        'Pesca description': {
            'es': 'Durante una excursión en Mal País, de 3 horas con guía local, se puede ver manta rayas, tortugas marinas, delfines, ballenas, y tal vez usted coge un atún, pargo de aleta amarilla o una caballa.',
            'en': 'During an excursion from Mal País, a 3-hour trip with a local guide, you may see manta rays, sea turtles, dolphins, whales, and maybe catch a tuna, yellowfin snapper or a mackerel.'
        },

        'Consultar precio': {'es': 'Consultar precio', 'en': 'Price on request'},

        'Let us help organize': {
            'es': 'Háganos saber si le podemos ayudar para organizar una de estas excursiones para usted!',
            'en': 'Let us know if we can help organize one of these excursions for you!'
        },
        
        'Nuestro hotel puede organizar lecciones de surf o un fotógrafo de surf para usted.': {
            'es': 'Nuestro hotel puede organizar lecciones de surf o un fotógrafo de surf para usted.',
            'en': 'Our hotel can arrange surf lessons or a surf photographer for you.'
        },
    })
