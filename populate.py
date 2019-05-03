import os
import django
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Server.settings')
django.setup()

from Grooving.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

users_artists_email = "utri1990@gmail.com"  # 'tucorreo@elquesea.com'     # Preferiblemente gmail
users_customers_email = "utri1990@gmail.com"  # 'tucorreo@elquesea.com'   # Preferiblemente gmail


def _service_generate_unique_payment_code():
    random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    payment_code = random_alphanumeric
    return payment_code


def save_data():
    # System configuration
    system_configuration1 = SystemConfiguration.objects.create(minimumPrice='20', currency='EUR', paypalTax='3.4',
                                                               creditCardTax='1.9',
                                                               vat='21', profit='10',
                                                               corporateEmail='grupogrooving@gmail.com',
                                                               reportEmail='grupogrooving@gmail.com',
                                                               appName='Grooving',
                                                               slogan='Connecting artist with you',
                                                               logo='',
                                                               privacyText_en="<h2>Introduction</h2>" +
                                                                              "<p>For Grooving, accessible from https://grooving-frontend-d4.herokuapp.com, one of our main " +
                                                                              "priorities is the privacy of our visitors. This Privacy Policy document contains the " +
                                                                              "information that is collected and recorded by Grooving and how we use it.</p>" +
                                                                              "<p>If you have additional questions or require more information about our Privacy Policy, " +
                                                                              "do not hesitate to contact us through email at grupogrooving@gmail.com</p>" +

                                                                              "<h2>Log Files</h2>" +
                                                                              "<p>Grooving follows a standard procedure of using log files. These files log visitors when  " +
                                                                              "they visit websites. All hosting companies use them since they are part of hosting services analytics. " +
                                                                              "The information collected by log files include internet protocol (IP) addresses, browser type, " +
                                                                              "Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the " +
                                                                              "number of clicks. These are not linked to any information that is personally identifiable. " +
                                                                              "The purpose of the information is for analyzing trends, administering the site, tracking users' " +
                                                                              "movement on the website, and gathering demographic information.</p>" +

                                                                              "<h2>Cookies policy</h2>" +

                                                                              "<p>For the operation of our application we use cookies to optimize user experience. Once you " +
                                                                              "access and browse the application for the first time, a window will appear in which you agree " +
                                                                              "to use cookies in accordance with our Privacy Policy. If you continue to browse the application " +
                                                                              "without accepting them, Grooving will consider that you have accepted our Privacy Policy " +
                                                                              "automatically.</p>" +

                                                                              "<h3>Third Party Privacy Policies</h3>" +

                                                                              "<p>In addition, third-party cookies are used for the development of your activity. Paypal and " +
                                                                              "Braintree cookies are used for payment security, to keep the users active session we use Django " +
                                                                              "cookies and for the management of images we use GitHub.</p>" +

                                                                              "<p>Note that Grooving has no access to or control over these cookies.</p>" +
                                                                              "<p>This Privacy Policy applies only to our online activities and is valid for visitors to our " +
                                                                              "website regarding the information that they shared and/or collect in Grooving. This " +
                                                                              "policy is not applicable to any information collected offline or via channels other than this " +
                                                                              "website.</p>" +

                                                                              "<p>Grooving's Privacy Policy does not apply to other websites. Thus, we are advising you to " +
                                                                              "consult the respective Privacy Policies of these third-party servers for more detailed " +
                                                                              "information. You may find a complete list of these Privacy Policies bellow:</p>" +

                                                                              "<h4>Braintree</h4>" +
                                                                              "<p>For more information visit the following link:" +
                                                                              "<a href=\"https://www.braintreepayments.com/legal/acceptable-use-policy\">" +
                                                                              "Braintree cookies policy</a></p>" +

                                                                              "<h4>Heroku</h4>" +
                                                                              "<p>For more information visit the following link: " +
                                                                              "<a href=\"https://www.salesforce.com/company/privacy/full_privacy.jsp#nav_info\">" +
                                                                              "Heroku cookies policy</a>" +

                                                                              "<h4>GitHub</h4>" +
                                                                              "<p>For more information visit the following link: " +
                                                                              "<a href=\"https://github.com/github/site-policy\">Github cookies policy</a></p>" +

                                                                              "<h4>Paypal</h4>" +
                                                                              "<p> For more information visit the following link: " +
                                                                              "<a href=\"https://www.paypal.com/uk/webapps/mpp/ua/cookie-full\">Paypal cookies policy</a></p>" +

                                                                              "<h2>Consent</h2>" +
                                                                              "<p>By using our website, you hereby accept our Privacy Policy and agree to its Terms and " +
                                                                              "Conditions.</p>",
                                                               privacyText_es=
                                                               "<h2>Introducción</h2>" +
                                                               "<p>En Grooving, accesible desde https://grooving-frontend-d4.herokuapp.com, una de nuestras " +
                                                               "principales prioridades es la privacidad de nuestros visitantes. Este documento de Política de " +
                                                               "privacidad contiene tipos de información que Grooving recopila y registra, y cómo la usamos.</p>" +
                                                               "<p>Si tiene preguntas adicionales o necesita más información sobre nuestra Política de " +
                                                               "privacidad, no dude en ponerse en contacto con nosotros a través del correo electrónico " +
                                                               "grupogrooving@gmail.com </p>" +

                                                               "<h2>Archivos de registro</h2>" +
                                                               "<p>Grooving sigue un procedimiento estándar de uso de archivos de registro. Estos archivos " +
                                                               "registran a los visitantes cuando visitan sitios web. Todas las empresas de hosting hacen esto " +
                                                               "y forman parte de la analítica de servicios de hosting. La información recopilada por los " +
                                                               "archivos de registro incluye direcciones de protocolo de Internet (IP), tipo de navegador, " +
                                                               "proveedor de servicios de Internet (ISP), marca de fecha y hora, páginas de referencia/salida " +
                                                               "y posiblemente el número de clics. Estos no están vinculados a ninguna información que sea " +
                                                               "personalmente identificable. El propósito de la información es analizar tendencias, administrar " +
                                                               "el sitio, rastrear el movimiento de los usuarios en el sitio web y recopilar información "
                                                               "demográfica.</p>" +

                                                               "<h2>Política de cookies</h2>" +
                                                               "<p>Para el correcto funcionamiento de nuestra aplicación utilizamos cookies para optimizar la " +
                                                               "experiencia de usuario. Una vez que acceda y navegue por primera vez en la aplicación se " +
                                                               "mostrará una ventana en la que usted acepta utilizar las cookies de acuerdo a nuestra Política " +
                                                               "de privacidad. Si usted continua navegando por la aplicación sin aceptarlas, Grooving " +
                                                               "considerará que usted ha aceptado nuestra Política de privacidad de forma automática.</p>" +

                                                               "<h3>Política de privacidad de terceros</h3>" +

                                                               "<p>Además se utilizan cookies de terceros para el desarrollo de su actividad. Para la seguridad " +
                                                               "de los pagos se utilizan las cookies de Paypal y Braintree, para mantener la sesión activa de " +
                                                               "los usuarios utilizamos cookies de Django y para la gestión de imágenes utilizamos las cookies " +
                                                               "de GitHub.</p>" +

                                                               "<p>Tenga en cuenta que Grooving no tiene acceso ni control sobre estas cookies.</p>" +

                                                               "<p>Esta Política de privacidad se aplica sólo a nuestras actividades en línea y es válida para " +
                                                               "los visitantes de nuestro sitio web en relación con la información que compartieron y/o " +
                                                               "recopilaron en Grooving. Esta política no se aplica a ninguna información recopilada fuera de " +
                                                               "línea o a través de canales que no sean este sitio web.</p>" +

                                                               "<p>La política de privacidad de Grooving no se aplica a otros sitios web. Por lo tanto, le " +
                                                               "recomendamos que consulte las políticas de privacidad. Puede encontrar una lista completa de " +
                                                               "estas Políticas de privacidad y sus enlaces a continuación:</p>" +

                                                               "<h4>Braintree</h4>" +
                                                               "<p>Para más información visita el siguiente link: " +
                                                               "<a href=\"https://www.braintreepayments.com/legal/acceptable-use-policy\">" +
                                                               "Braintree cookies policy</a></p>" +

                                                               "<h4>Heroku</h4>" +
                                                               "<p>Para más información visita el siguiente link: " +
                                                               "<a href=\"https://www.salesforce.com/company/privacy/full_privacy.jsp#nav_info\">Heroku cookies policy</a>" +

                                                               "<h4>GitHub</h4>" +
                                                               "<p>Para más información visita el siguiente link: " +
                                                               "<a href=\"https://github.com/github/site-policy\">Github cookies policy</a></p>" +

                                                               "<h4>Paypal</h4>" +
                                                               "<p>Para más información visita el siguiente link: " +
                                                               "<a href=\"https://www.paypal.com/uk/webapps/mpp/ua/cookie-full\">Paypal cookies policy</a></p>" +

                                                               "<h2>Consentimiento</h2>" +
                                                               "<p>Al utilizar nuestro sitio web, usted acepta nuestra Política de privacidad y acepta sus " +
                                                               "Términos y condiciones.</p>",
                                                               aboutUs_en="<p>At Grooving, we work hard to solve the daily problems of the artists by making them known " +
                                                                          "and increasing their daily activity in an easy, simple and reliable way. </p>" +

                                                                          "<h2>Do you think it's impossible? </h2>" +

                                                                          "<p>With <b>Grooving</b>, we manage to make it real by simplifying the search and hiring of " +
                                                                          "artists. </p>",
                                                               aboutUs_es="<h2>Sobre nosotros</h2>" +
                                                                          "<p>En Grooving, trabajamos duro para resolver los problemas diarios de los artistas dándoles a " +
                                                                          "conocer e incrementando su actividad diaria de una forma fácil, sencilla y fiable.</p>" +

                                                                          "<h2>¿Piensas que es imposible?</h2>" +

                                                                          "<p>Con <b>Grooving</b> conseguimos hacerlo realidad simplificando la búsqueda y contratación de " +
                                                                          "artistas.</p>",

                                                               termsText_es="<p>Las condiciones de uso de la página web, las reglas de uso y el uso de grooving-frontend-d4.herokuapp.com, la " +
                                                                            "propiedad de Grooving SL y el correo electrónico grupogrooving@gmail.com, en adelante, " +
                                                                            "Grooving, que el usuario del portal debe aceptar para utilizar todos los servicios e " +
                                                                            "información que se proporcionan desde el portal.</p>" +

                                                                            "<p>Tanto el usuario como Grooving, propietario del portal, se han convertido en las partes. " +
                                                                            "El acceso al uso del portal, la parte de sus contenidos y servicios significa la aceptación " +
                                                                            "total de estas condiciones de uso. La implementación del uso del portal se refiere a la " +
                                                                            "aplicación estricta de los términos reconocidos en los términos de uso del portal.</p>" +

                                                                            "<h2>Regulación de las condiciones de uso</h2>" +
                                                                            "<p>Las condiciones generales de uso del portal regulan el acceso y uso del portal, los " +
                                                                            "contenidos y servicios, la disposición de los usuarios y/o a través del portal, ya sea a " +
                                                                            "través del portal, por los usuarios o por un tercero. Sin embargo, el acceso y el uso del " +
                                                                            "contenido y/o los servicios pueden utilizarse en ciertas condiciones específicas.</p>" +

                                                                            "<h2>Modificaciones</h2>" +

                                                                            "<p>La empresa se reserva el derecho de modificar en cualquier momento las condiciones " +
                                                                            "generales de uso del portal. En cualquier caso, le recomendamos que consulte periódicamente " +
                                                                            "las condiciones generales de uso del portal y que éstas se puedan modificar.</p>" +

                                                                            "<h2>Información y servicios</h2>" +

                                                                            "<p>Los usuarios pueden acceder a un tipo diferente de información y servicios a través " +
                                                                            "del portal. El portal se reserva el derecho de modificar, en cualquier momento y sin previo " +
                                                                            "aviso, la presentación y configuración de la información y los servicios del portal. El " +
                                                                            "usuario reconoce y acepta expresamente que en cualquier momento el portal puede interrumpir, " +
                                                                            "desactivar y/o cancelar cualquier información o servicio. Sin embargo, a veces, por razones " +
                                                                            "de mantenimiento, actualización, cambio de ubicación, etc., puede significar la interrupción " +
                                                                            "del acceso al portal.</p>" +

                                                                            "<p>El pago será efectuado por la parte contratante a Grooving. Antes del comienzo de la " +
                                                                            "actuación, el cliente completará el proceso de pago enviando un pago al artista con el que " +
                                                                            "recibirá un ingreso por los servicios prestados. En este proceso, Grooving se llevará el 10% " +
                                                                            "del pago realizado.</p>" +

                                                                            "<p>Si no se acepta una petición en 29 días, se da por supuesto que la oferta no interesa.</p>" +

                                                                            "<h2>Información del portal y disponibilidad de servicios</h2>" +
                                                                            "<p>El portal no garantiza la disponibilidad continua y permanente de los servicios, " +
                                                                            "quedando así eximido de cualquier responsabilidad por posibles daños, como la falta de " +
                                                                            "disponibilidad del servicio debido a fuerza mayor o errores en las redes de transferencia " +
                                                                            "de datos telemáticos, o desconexiones hechas para la mejora o mantenimiento de equipos y " +
                                                                            "sistemas informáticos. En estos casos, el portal será anunciado 24 horas antes de la " +
                                                                            "interrupción. El portal no será responsable de la interrupción, suspensión o terminación " +
                                                                            "de la información o servicios.<p>" +

                                                                            "<h2>Responsabilidades del contenido del portal</h2>" +

                                                                            "<p>El portal controlará la licencia de los servicios prestados a través de la plataforma por " +
                                                                            "terceros. En el caso de que el usuario como resultado del uso del portal sufra o dañe la " +
                                                                            "comunicación y se tomen las medidas adecuadas para resolverlo.</p>" +

                                                                            "<p>Haremos todo lo posible para evitar la subida de contenido ilegal pero no podemos asegurarlo " +
                                                                            "al 100%. El usuario reconoce que el portal no es responsable de los contenidos y/o servicios " +
                                                                            "proporcionados o proporcionados por terceros en y/o a través del portal.</p>" +

                                                                            "<p>En cualquier caso, el portal excluye cualquier responsabilidad por daños y pérdidas que " +
                                                                            "puedan deberse a información y/o servicios prestados o proporcionados por terceros que no " +
                                                                            "sean la propios de Grooving. Toda la responsabilidad será asumida por un tercero, ya sea " +
                                                                            "proveedor, colaborador u otro.</p>" +

                                                                            "<h2>Obligaciones de los usuarios</h2>" +
                                                                            "<p>El usuario debe respetar en todo momento los términos y condiciones establecidos. " +
                                                                            "El usuario acepta que utilizará el portal asumiendo cualquier responsabilidad que pueda " +
                                                                            "surgir de la infracción de las reglas.</p>" +

                                                                            "<p>Asimismo, el usuario no puede usar el portal para transmitir, almacenar, divulgar, " +
                                                                            "promocionar o distribuir datos o contenidos que sean portadores de virus o cualquier otro " +
                                                                            "código de computadora, archivos o programas diseñados para interrumpir, destruir o impedir " +
                                                                            "el funcionamiento de cualquier program o equipo.</p>" +

                                                                            "<p>El usuario se compromete a indemnizar y eximir de responsabilidad al portal por " +
                                                                            "cualquier daño, perjuicio, penalización, multa, penalización o compensación que el portal " +
                                                                            "deba afrontar.</p>" +

                                                                            "<h2>Cookies</h2>" +
                                                                            "<p>Empleamos el uso de cookies. Al acceder a Grupo Grooving, usted ha aceptado usar cookies " +
                                                                            "de acuerdo con la Política de privacidad de Grooving.</p>" +

                                                                            "<p>La mayoría de los sitios web interactivos utilizan cookies para permitirnos recuperar " +
                                                                            "los detalles del usuario para cada visita. Las cookies son utilizadas por nuestro sitio web " +
                                                                            "para permitir la funcionalidad de ciertas áreas para que sea más fácil para las personas que " +
                                                                            "visitan nuestro sitio web.</p>" +

                                                                            "<h2>iFrames</h2>" +
                                                                            "<p>Sin la aprobación previa y el permiso por escrito, no puede crear iFrames alrededor de " +
                                                                            "nuestras páginas web que alteren de alguna manera la presentación visual o la apariencia de " +
                                                                            "nuestro sitio web.</p>" +

                                                                            "<h2>Licencias</h2>" +
                                                                            "<p>A menos que se indique lo contrario, Grooving y/o sus licenciantes son propietarios de " +
                                                                            "los derechos de propiedad intelectual de todo el material de Grooving. Todos los derechos " +
                                                                            "de propiedad intelectual están reservados.</p>" +

                                                                            "<h2>Eliminación de enlaces</h2>" +

                                                                            "<p> Si encuentra algún enlace en Grooving que sea ofensivo por cualquier motivo, puede " +
                                                                            "contactarnos e informarnos en cualquier momento. Estudiaremos sus peticiones para retirar " +
                                                                            "los enlaces.</p>" +

                                                                            "<p>No aseguramos que la información sea correcta, su integridad o exactitud; ni prometemos " +
                                                                            "garantizar que el sitio web permanezca disponible o que el material en el sitio web se " +
                                                                            "mantenga actualizado.</p>" +

                                                                            "<h2>Comportamiento inapropiado de otros usuarios</h2>" +
                                                                            "<p>Si detecta un comportamiento inadecuado de otro usuario de Grooving, puede reportarlo a " +
                                                                            "Grooving enviando un correo electrónico a grupogrooving@gmail.com adjuntando el nombre de " +
                                                                            "usuario que desea informar, el motivo y alguna prueba (vídeo, imágenes, enlaces, ...) .</p>" +

                                                                            "<h2>GPDR - Regulación de Protección General de Datos</h2>" +
                                                                            "<p>Este documento está adaptado al Reglamento Europeo de Protección de Datos (RGPD) y a la " +
                                                                            "reciente Ley Orgánica 3/2018, del 5 de diciembre, de Protección de Datos Personales y " +
                                                                            "garantía de los derechos digitales cumpliendo con cada uno de sus artículos y sometiéndose " +
                                                                            "a auditorías regularmente.</p>" +

                                                                            "<p>Si tiene dudas o en el caso de que no pueda ejercer alguno de sus derechos, puede enviar " +
                                                                            "un correo a grupogrooving@gmail.com.</p>" +

                                                                            "<p>Todos los datos generados en Grooving son almacenados en nuestros servidores y utilizando " +
                                                                            "protocolos seguros de comunicación.</p>" +

                                                                            "<h3>Derecho a ser informado sobre brechas de seguridad</h3>" +
                                                                            "<p>En caso de que el equipo de Grooving detecte una brecha de seguridad, a todas aquellas " +
                                                                            "personas afectadas se les notificará en un máximo de 72 horas posteriores a su detección.</p>" +

                                                                            "<h3>Derecho a exportar tus datos personales</h3>" +
                                                                            "<p>Todos los usuarios que utilizan Grooving pueden solicitar los datos que nuestra empresa " +
                                                                            "tiene sobre ellos desde su perfil de usuario y serán enviadas en formato PDF adjunto al " +
                                                                            "correo vinculado con el usuario en Grooving.</p>" +

                                                                            "<p>Los datos que se enviarán a los artistas que lo hayan solicitado serán los siguientes:</p>" +

                                                                            "<ul>" +
                                                                            "<li type=”circle”><b>Información artística</b>: nombre artístico, género artístico, zonas de " +
                                                                            "actuación, puntuación del grupo, días no disponibles, biografía, paquetes de pago " +
                                                                            "disponibles y contenido adicional.</li>" +

                                                                            "<li type=”circle”><b>Ofertas</b>: nombre del evento, contratante, día del evento, dirección, " +
                                                                            "zona de actuación, descripción de la oferta, estado de la oferta, precio, cuenta de paypal " +
                                                                            "en la que se vaya a realizar el pago y valoración por parte del cliente.</li>" +
                                                                            "</ul>" +

                                                                            "<p>Los datos que se enviarán a los clientes que lo hayan solicitado serán los siguientes:</p>" +
                                                                            "<ul>" +
                                                                            "<li type=”circle”><b>Eventos</b>: nombre, dirección y zona.</li>" +
                                                                            "<li type=”circle”><b>Ofertas realizadas</b>: artista, día del evento, paquete de pago " +
                                                                            "seleccionado, precio y estado de la oferta.</li>" +
                                                                            "</ul>" +

                                                                            "<h3>Derecho al olvido</h3>" +
                                                                            "<ul>" +
                                                                            "<li type=”circle”><b>Artistas</b>: se anonimiza el portfolio (banner, biografía y nombre " +
                                                                            "artistico).</li>" +
                                                                            "<li type=”circle”><b>Paquetes de pago</b>: descripción, información sobre la actuación.</li>" +
                                                                            "<li type=”circle”><b>Ofertas</b>: las credenciales de paypal del artista.</li>" +
                                                                            "</ul>" +

                                                                            "<p>Todas aquellas interacciones que el cliente haya realizado en la aplicación serán " +
                                                                            "eliminadas a excepción de:</p>" +

                                                                            "<ul>" +
                                                                            "<li><b>Localizaciones de los eventos</b>: descripción, dirección y nombre</li>" +
                                                                            "</ul>" +

                                                                            "<p>Para mantener la privacidad de los usuarios se eliminarán todas aquellas conversaciones " +
                                                                            "en las que haya participado.</p>" +

                                                                            "<p>Al aplicar este derecho, los datos de la aplicación se anonimizarán en nuestros " +
                                                                            "servidores con motivo de mantener un histórico de datos para realizar opearaciones " +
                                                                            "estadísticas.</p>" +
                                                               
                                                                            "<h1>Privacidad</h1>" +
                                                                            "<h2>Introducción</h2>" +
                                                                            "<p>En Grooving, accesible desde https://grooving-frontend-d4.herokuapp.com, una de nuestras " +
                                                                            "principales prioridades es la privacidad de nuestros visitantes. Este documento de Política de " +
                                                                            "privacidad contiene tipos de información que Grooving recopila y registra, y cómo la usamos.</p>" +
                                                                            "<p>Si tiene preguntas adicionales o necesita más información sobre nuestra Política de " +
                                                                            "privacidad, no dude en ponerse en contacto con nosotros a través del correo electrónico " +
                                                                            "grupogrooving@gmail.com </p>" +

                                                                            "<h2>Archivos de registro</h2>" +
                                                                            "<p>Grooving sigue un procedimiento estándar de uso de archivos de registro. Estos archivos " +
                                                                            "registran a los visitantes cuando visitan sitios web. Todas las empresas de hosting hacen esto " +
                                                                            "y forman parte de la analítica de servicios de hosting. La información recopilada por los " +
                                                                            "archivos de registro incluye direcciones de protocolo de Internet (IP), tipo de navegador, " +
                                                                            "proveedor de servicios de Internet (ISP), marca de fecha y hora, páginas de referencia/salida " +
                                                                            "y posiblemente el número de clics. Estos no están vinculados a ninguna información que sea " +
                                                                            "personalmente identificable. El propósito de la información es analizar tendencias, administrar " +
                                                                            "el sitio, rastrear el movimiento de los usuarios en el sitio web y recopilar información "
                                                                            "demográfica.</p>" +

                                                                            "<h2>Política de cookies</h2>" +
                                                                            "<p>Para el correcto funcionamiento de nuestra aplicación utilizamos cookies para optimizar la " +
                                                                            "experiencia de usuario. Una vez que acceda y navegue por primera vez en la aplicación se " +
                                                                            "mostrará una ventana en la que usted acepta utilizar las cookies de acuerdo a nuestra Política " +
                                                                            "de privacidad. Si usted continua navegando por la aplicación sin aceptarlas, Grooving " +
                                                                            "considerará que usted ha aceptado nuestra Política de privacidad de forma automática.</p>" +

                                                                            "<h3>Política de privacidad de terceros</h3>" +

                                                                            "<p>Además se utilizan cookies de terceros para el desarrollo de su actividad. Para la seguridad " +
                                                                            "de los pagos se utilizan las cookies de Paypal y Braintree, para mantener la sesión activa de " +
                                                                            "los usuarios utilizamos cookies de Django y para la gestión de imágenes utilizamos las cookies " +
                                                                            "de GitHub.</p>" +

                                                                            "<p>Tenga en cuenta que Grooving no tiene acceso ni control sobre estas cookies.</p>" +

                                                                            "<p>Esta Política de privacidad se aplica sólo a nuestras actividades en línea y es válida para " +
                                                                            "los visitantes de nuestro sitio web en relación con la información que compartieron y/o " +
                                                                            "recopilaron en Grooving. Esta política no se aplica a ninguna información recopilada fuera de " +
                                                                            "línea o a través de canales que no sean este sitio web.</p>" +

                                                                            "<p>La política de privacidad de Grooving no se aplica a otros sitios web. Por lo tanto, le " +
                                                                            "recomendamos que consulte las políticas de privacidad. Puede encontrar una lista completa de " +
                                                                            "estas Políticas de privacidad y sus enlaces a continuación:</p>" +

                                                                            "<h4>Braintree</h4>" +
                                                                            "<p>Para más información visita el siguiente link: " +
                                                                            "<a href=\"https://www.braintreepayments.com/legal/acceptable-use-policy\">" +
                                                                            "Braintree cookies policy</a></p>" +

                                                                            "<h4>Heroku</h4>" +
                                                                            "<p>Para más información visita el siguiente link: " +
                                                                            "<a href=\"https://www.salesforce.com/company/privacy/full_privacy.jsp#nav_info\">Heroku cookies policy</a>" +

                                                                            "<h4>GitHub</h4>" +
                                                                            "<p>Para más información visita el siguiente link: " +
                                                                            "<a href=\"https://github.com/github/site-policy\">Github cookies policy</a></p>" +


                                                                            "<h4>Paypal</h4>" +
                                                                            "<p>Para más información visita el siguiente link: " +
                                                                            "<a href=\"https://www.paypal.com/uk/webapps/mpp/ua/cookie-full\">Paypal cookies policy</a></p>" +

                                                                            "<h2>Consentimiento</h2>" +
                                                                            "<p>Al utilizar nuestro sitio web, usted acepta nuestra Política de privacidad y acepta sus " +
                                                                            "Términos y condiciones.</p>",

                                                               termsText_en="<p>The conditions of use of the web page, the rules of use and the use of " +
                                                                            "grooving-frontend-d4.herokuapp.com, the property of Grooving SL and the email grupogrooving@gmail.com, " +
                                                                            " hereinafter, Grooving, that the user of the portal must accept to use all the " +
                                                                            "services and information that are provided from the portal.</p>" +
                                                                            "<p>The user as well as Grooving, owner of the portal, have become the parties. " +
                                                                            "Access to the use of the portal, the part of its contents and services means full " +
                                                                            "acceptance of these conditions of use. The implementation of the provision and use " +
                                                                            "of the portal refers to the strict application of the terms recognized in these " +
                                                                            "terms of use of the portal.</p>" +

                                                                            "<h2>Use conditions regulation</h2>" +
                                                                            "<p>The general conditions of use of the portal regulate the access and use of the " +
                                                                            "portal, the contents and services, the disposition of the users and / or through " +
                                                                            "the portal, either through the portal, either by the users or by any third party. " +
                                                                            "However, access and use of the content and / or services may be used in certain " +
                                                                            "specific conditions.</p>" +

                                                                            "<h2>Modifications</h2>" +
                                                                            "<p>The company reserves the right to modify at any time the general conditions of " +
                                                                            "use of the portal. In any case, we recommend that you periodically consult the " +
                                                                            "general conditions of use of the portal, and that they can be modified.</p>" +

                                                                            "<h2>Information and services</h2>" +
                                                                            "<p>Users can access a different type of information and services through the portal. " +
                                                                            "The portal reserves the right to modify, at any time, and without prior notice, the " +
                                                                            "presentation and configuration of information and services from the portal. The user " +
                                                                            "expressly acknowledges and accepts that at any time the portal may interrupt, " +
                                                                            "deactivate and / or cancel any information or service. " +
                                                                            "However, sometimes, for reasons of maintenance, updating, change of location, etc., " +
                                                                            "may mean the interruption of access to the portal.</p>" +

                                                                            "<p>The payment will be made by the contracting party to Grooving. Before the beginning of " +
                                                                            "the performance, the client will complete the payment process by sending a payment to the " +
                                                                            "artist with whom he will receive an income for the services rendered. In this process, " +
                                                                            "Grooving will take 10% of the payment made.</p>" +

                                                                            "<p>If a request is not accepted in 29 days, it is assumed that the offer does not interest.</p>"

                                                                            "<h2>Portal information and services availability</h2>" +
                                                                            "<p>The portal does not guarantee the continuous and permanent availability of the " +
                                                                            "services being in this way exempt from any responsibility for possible damages such " +
                                                                            "as the lack of availability of the service due to force majeure or errors in the " +
                                                                            "telematic data transfer networks, works at will, or disconnections made for " +
                                                                            "improvement or maintenance of computer equipment and systems. In these cases, the " +
                                                                            "portal will be announced 24 hours before the interruption.  The portal will not be " +
                                                                            "responsible for the interruption, suspension or termination of the information " +
                                                                            "or services</p>" +

                                                                            "<h2>Portal contents responsibility</h2>" +
                                                                            "<p>The portal will control the license of those services provided through the " +
                                                                            "platform by third parties. In the event that the user as a result of the use of the " +
                                                                            "portal suffers or will harm the communication and the appropriate measures will be " +
                                                                            "taken to solve it.</p>" +

                                                                            "<p>We will do everything possible to prevent the upload of illegal content but we can not "
                                                                            "guarantee it to 100%. In any case, the user acknowledges that the portal is not " +
                                                                            "and is not responsible for the contents and / or services provided or provided by third " +
                                                                            "parties in and / or through the portal.</p>" +

                                                                            "<p>In any case, the portal excludes any liability for damages and losses that may be " +
                                                                            "due to information and / or services provided or provided by third parties other " +
                                                                            "than the Company. All responsibility will be the third party, whether provider, " +
                                                                            "collaborator or other.</p>" +

                                                                            "<h2>User’s obligations</h2>" +
                                                                            "<p>The user must respect at all times the terms and conditions established in this " +
                                                                            "legal notice. The user expresses expressly that he will use the portal diligently " +
                                                                            "and assuming any responsibility that may arise from the breach of the rules.</p>" +
                                                                            "<p>Likewise, the user may not use the portal to transmit, store, disclose, promote " +
                                                                            "or distribute data or contents that are carriers of viruses or any other computer " +
                                                                            "code, files or programs designed to interrupt, destroy or impair the operation of " +
                                                                            "any program or equipment.</p>"
                                                                            "<p>The user undertakes to indemnify and hold harmless the portal for any damage, " +
                                                                            "prejudice, penalty, fine, penalty or compensation that the portal has to face.</p>" +

                                                                            "<h2>Cookies</h2>" +
                                                                            "<p>We employ the use of cookies. By accessing Grooving group, you agreed to use " +
                                                                            "cookies in agreement with the Grooving's Privacy Policy.</p>" +

                                                                            "<p>Most interactive websites use cookies to let us retrieve the user's details for " +
                                                                            "each visit. Cookies are used by our website to enable the functionality of certain " +
                                                                            "areas to make it easier for people visiting our website.</p>" +

                                                                            "<h2>iFrames</h2>" +
                                                                            "<p>Without prior approval and written permission, you may not create frames around " +
                                                                            "our Webpages that alter in any way the visual presentation or appearance of our Website.</p>" +

                                                                            "<h2>License</h2>" +
                                                                            "<p>Unless otherwise stated, Grooving and/or its licensors own the intellectual " +
                                                                            "property rights for all material on Grooving. All intellectual property rights are " +
                                                                            "reserved.</p>" +

                                                                            "<h2>Removal of links from our website</h2>" +
                                                                            "<p>If you find any link on Grooving that is offensive for any reason, you are " +
                                                                            "free to contact and inform us any moment. We will consider requests to remove links.</p>" +
                                                                            "<p>We do not ensure that the information on this website is correct, we do not " +
                                                                            "warrant its completeness or accuracy; nor do we promise to ensure that the " +
                                                                            "website remains available or that the material on the website is kept up to date.</p>" +

                                                                            "<h2>Bad users behavior</h2>" +
                                                                            "<p>If you detect inappropriate behavior of another Grooving user, you can report it to " +
                                                                            "Grooving by sending an email to grupogrooving@gmail.com attached the username you want to " +
                                                                            "report, the reason, and some proof (video, images, links, ...).</p>"

                                                                            "<h2>GPDR - General Data Protection Regulation</h2>" +
                                                                            "<p>This document is adapted to the European Data Protection Regulation (RGPD) and to the " +
                                                                            "recent Organic Law 3/2018, of December 5, on the Protection of Personal Data and guarantee of " +
                                                                            "digital rights complying with each of its articles and undergoing regular audits. </p>" +

                                                                            "<p>If you have any doubts or if you can not exercise any of your rights, you can send an " +
                                                                            "email to grupogrooving@gmail.com.</p>" +

                                                                            "<p>All the data generated in Grooving is stored on our servers and using secure communication " +
                                                                            "protocols.</p>" +

                                                                            "<h3>Right to be informed with breaches</h3>" +
                                                                            "<p>In the event that the Grooving team detects a security breach, all those affected will be " +
                                                                            "notified within a maximum of 72 hours after detection.</p>" +

                                                                            "<h3>Right to export personal information</h3>" +
                                                                            "<p>All users who use Grooving can request the data that our company has about them from their " +
                                                                            "user profile and they will be sent in PDF format attached to the mail linked with the user in " +
                                                                            "Grooving.</p>" +

                                                                            "<p>The data that will be sent to the artists that have requested it will be: </p>" +
                                                                            "<ul>" +
                                                                            "<li><b>Artistic information</b>: artistic name, artistic genre, performance areas, group score, " +
                                                                            "days not available, biography, available payment packages and additional content.</li> " +

                                                                            "<li><b>Offers</b>: name of the event, contractor, day of the event, address, area of " +
                                                                            "​​action, description of the offer, status of the offer, price, paypal account in the that the " +
                                                                            "payment and valuation by the client will be made.</li>" +
                                                                            "</ul>" +

                                                                            "<p>The data that will be sent to the clients that have requested it will be:</p>" +
                                                                            "<ul>" +
                                                                            "<li><b>Events</b>: name, address and area.</li>" +
                                                                            "<li><b>Offers made</b>: artist, day of the event, selected payment package, price and " +
                                                                            "status of the offer.</li>" +
                                                                            "</ul>" +

                                                                            "<h3>Right to be forgotten</h3>" +
                                                                            "<p>Any user of the application can benefit from the right to be forgotten. This right will be " +
                                                                            "made by removing all personal data of said user.</p>" +

                                                                            "<p>All interactions that the artist has made in the application will be eliminated with the " +
                                                                            "following exceptions:</p>" +

                                                                            "<ul>" +
                                                                            "<li><b>Artists</b>: the portfolio is anonymized (banner, biography and artistic name).</li>" +
                                                                            "<li><b>Payment packages</b>: description, information about the performance.</li>" +
                                                                            "<li><b>Offers</b>: the artist's paypal credentials.</li>" +
                                                                            "</ul>" +

                                                                            "<p>All those interactions that the client has made in the application will be eliminated with " +
                                                                            "the exception of:</p>" +

                                                                            "<ul>" +
                                                                            "<li><b>Event location</b>: description, address and name.</li>" +
                                                                            "<li><b>Ratings</b>: Comments made anonymized.</li>" +
                                                                            "</ul>" +

                                                                            "<p>To maintain the privacy of users, all conversations in which you have participated will be " +
                                                                            "deleted.</p>" +

                                                                            "<p>By applying this right, the application data will be anonymized on our servers in order to " +
                                                                            "maintain a data history to perform statistical operations.</p>" +
                                                               
                                                                            "<h1>Privacy</h1>" +
                                                                            "<h2>Introduction</h2>" +
                                                                            "<p>For Grooving, accessible from https://grooving-frontend-d4.herokuapp.com, one of our main " +
                                                                            "priorities is the privacy of our visitors. This Privacy Policy document contains the " +
                                                                            "information that is collected and recorded by Grooving and how we use it.</p>" +
                                                                            "<p>If you have additional questions or require more information about our Privacy Policy, " +
                                                                            "do not hesitate to contact us through email at grupogrooving@gmail.com</p>" +

                                                                            "<h2>Log Files</h2>" +
                                                                            "<p>Grooving follows a standard procedure of using log files. These files log visitors when  " +
                                                                            "they visit websites. All hosting companies use them since they are part of hosting services analytics. " +
                                                                            "The information collected by log files include internet protocol (IP) addresses, browser type, " +
                                                                            "Internet Service Provider (ISP), date and time stamp, referring/exit pages, and possibly the " +
                                                                            "number of clicks. These are not linked to any information that is personally identifiable. " +
                                                                            "The purpose of the information is for analyzing trends, administering the site, tracking users' " +
                                                                            "movement on the website, and gathering demographic information.</p>" +

                                                                            "<h2>Cookies policy</h2>" +

                                                                            "<p>For the operation of our application we use cookies to optimize user experience. Once you " +
                                                                            "access and browse the application for the first time, a window will appear in which you agree " +
                                                                            "to use cookies in accordance with our Privacy Policy. If you continue to browse the application " +
                                                                            "without accepting them, Grooving will consider that you have accepted our Privacy Policy " +
                                                                            "automatically.</p>" +

                                                                            "<h3>Third Party Privacy Policies</h3>" +

                                                                            "<p>In addition, third-party cookies are used for the development of your activity. Paypal and " +
                                                                            "Braintree cookies are used for payment security, to keep the users active session we use Django " +
                                                                            "cookies and for the management of images we use GitHub.</p>" +

                                                                            "<p>Note that Grooving has no access to or control over these cookies.</p>" +
                                                                            "<p>This Privacy Policy applies only to our online activities and is valid for visitors to our " +
                                                                            "website regarding the information that they shared and/or collect in Grooving. This " +
                                                                            "policy is not applicable to any information collected offline or via channels other than this " +
                                                                            "website.</p>" +

                                                                            "<p>Grooving's Privacy Policy does not apply to other websites. Thus, we are advising you to " +
                                                                            "consult the respective Privacy Policies of these third-party servers for more detailed " +
                                                                            "information. You may find a complete list of these Privacy Policies bellow:</p>" +

                                                                            "<h4>Braintree</h4>" +
                                                                            "<p>For more information visit the following link:" +
                                                                            "<a href=\"https://www.braintreepayments.com/legal/acceptable-use-policy\">" +
                                                                            "Braintree cookies policy</a></p>" +

                                                                            "<h4>Heroku</h4>" +
                                                                            "<p>For more information visit the following link: " +
                                                                            "<a href=\"https://www.salesforce.com/company/privacy/full_privacy.jsp#nav_info\">" +
                                                                            "Heroku cookies policy</a>" +

                                                                            "<h4>GitHub</h4>" +
                                                                            "<p>For more information visit the following link: " +
                                                                            "<a href=\"https://github.com/github/site-policy\">Github cookies policy</a></p>" +

                                                                            "<h4>Paypal</h4>" +
                                                                            "<p> For more information visit the following link: " +
                                                                            "<a href=\"https://www.paypal.com/uk/webapps/mpp/ua/cookie-full\">Paypal cookies policy</a></p>" +

                                                                            "<h2>Consent</h2>" +
                                                                            "<p>By using our website, you hereby accept our Privacy Policy and agree to its Terms and " +
                                                                            "Conditions.</p>"
                                                               
                                                                            )

    system_configuration1.save()

    # ArtisticGenders
    artistic_gender0 = ArtisticGender.objects.create(name_en='All genres', name_es="Todos los géneros")
    artistic_gender0.save()

    artistic_gender1 = ArtisticGender.objects.create(name_en='Music', parentGender=artistic_gender0, name_es="Música")
    artistic_gender1.save()

    artistic_gender2 = ArtisticGender.objects.create(name_en='DJ', parentGender=artistic_gender1,
                                                     name_es="DJ")
    artistic_gender2.save()

    artistic_gender3 = ArtisticGender.objects.create(name_en='Pop', parentGender=artistic_gender1, name_es="Pop")
    artistic_gender3.save()

    artistic_gender4 = ArtisticGender.objects.create(name_en='Rock', parentGender=artistic_gender1, name_es="Rock")
    artistic_gender4.save()

    artistic_gender5 = ArtisticGender.objects.create(name_en='Flamenco', parentGender=artistic_gender1,
                                                     name_es="Flamenco")
    artistic_gender5.save()

    artistic_gender6 = ArtisticGender.objects.create(name_en='Magician', parentGender=artistic_gender0, name_es="Mago")
    artistic_gender6.save()

    artistic_gender7 = ArtisticGender.objects.create(name_en='Comedian', parentGender=artistic_gender0,
                                                     name_es="Comedia")
    artistic_gender7.save()

    artistic_gender8 = ArtisticGender.objects.create(name_en='Carnival', parentGender=artistic_gender0,
                                                     name_es="Carnaval")
    artistic_gender8.save()

    artistic_gender9 = ArtisticGender.objects.create(name_en='Clowns', parentGender=artistic_gender7, name_es="Payasos")
    artistic_gender9.save()

    artistic_gender11 = ArtisticGender.objects.create(name_en='Mariachis', parentGender=artistic_gender1,
                                                      name_es="Mariachis")
    artistic_gender11.save()

    artistic_gender12 = ArtisticGender.objects.create(name_en='Animation', parentGender=artistic_gender0,
                                                      name_es="Animación")
    artistic_gender12.save()

    artistic_gender13 = ArtisticGender.objects.create(name_en='Theater', parentGender=artistic_gender0,
                                                      name_es="Teatro")
    artistic_gender13.save()

    artistic_gender10 = ArtisticGender.objects.create(name_en='Drag Queen', parentGender=artistic_gender12,
                                                      name_es="Drag queen")
    artistic_gender10.save()
    # Zones

    zone0 = Zone.objects.create(name='España')
    zone0.save()

    # comunidades
    zone1_0 = Zone.objects.create(name='Andalucía', parentZone=zone0)
    zone1_0.save()

    zone1_1 = Zone.objects.create(name='Castilla-La Mancha', parentZone=zone0)
    zone1_1.save()

    zone1_2 = Zone.objects.create(name='Región de Murcia', parentZone=zone0)
    zone1_2.save()

    zone1_3 = Zone.objects.create(name='Comunidad Valenciana', parentZone=zone0)
    zone1_3.save()

    zone1_4 = Zone.objects.create(name='Islas Baleares', parentZone=zone0)
    zone1_4.save()

    zone1_4 = Zone.objects.create(name='Cataluña', parentZone=zone0)
    zone1_4.save()

    zone1_5 = Zone.objects.create(name='Aragón', parentZone=zone0)
    zone1_5.save()

    zone1_6 = Zone.objects.create(name='Navarra', parentZone=zone0)
    zone1_6.save()

    zone1_7 = Zone.objects.create(name='La Rioja', parentZone=zone0)
    zone1_7.save()

    zone1_8 = Zone.objects.create(name='País Vasco', parentZone=zone0)
    zone1_8.save()

    zone1_9 = Zone.objects.create(name='Cantabria', parentZone=zone0)
    zone1_9.save()

    zone1_10 = Zone.objects.create(name='Asturias', parentZone=zone0)
    zone1_10.save()

    zone1_11 = Zone.objects.create(name='Galicia', parentZone=zone0)
    zone1_11.save()

    zone1_12 = Zone.objects.create(name='Castilla y León', parentZone=zone0)
    zone1_12.save()

    zone1_13 = Zone.objects.create(name='Comunidad de Madrid', parentZone=zone0)
    zone1_13.save()

    zone1_14 = Zone.objects.create(name='Canarias', parentZone=zone0)
    zone1_14.save()

    zone1_15 = Zone.objects.create(name='Ceuta', parentZone=zone0)
    zone1_15.save()

    zone1_16 = Zone.objects.create(name='Melilla', parentZone=zone0)
    zone1_16.save()

    zone1_17 = Zone.objects.create(name='Extremadura', parentZone=zone0)
    zone1_17.save()

    # Andalucía
    zone2 = Zone.objects.create(name='Sevilla', parentZone=zone1_0)
    zone2.save()

    zone3 = Zone.objects.create(name='Huelva', parentZone=zone1_0)
    zone3.save()

    zone4 = Zone.objects.create(name='Almería', parentZone=zone1_0)
    zone4.save()

    zone5 = Zone.objects.create(name='Cádiz', parentZone=zone1_0)
    zone5.save()

    zone6 = Zone.objects.create(name='Málaga', parentZone=zone1_0)
    zone6.save()

    zone7 = Zone.objects.create(name='Córdoba', parentZone=zone1_0)
    zone7.save()

    zone8 = Zone.objects.create(name='Granada', parentZone=zone1_0)
    zone8.save()

    zone9 = Zone.objects.create(name='Jaén', parentZone=zone1_0)
    zone9.save()

    # Aragón
    zone10 = Zone.objects.create(name='Huesca', parentZone=zone1_5)
    zone10.save()

    zone11 = Zone.objects.create(name='Teruel', parentZone=zone1_5)
    zone11.save()

    zone12 = Zone.objects.create(name='Zaragoza', parentZone=zone1_5)
    zone12.save()

    # Canarias

    zone13 = Zone.objects.create(name='Las Palmas', parentZone=zone1_14)
    zone13.save()

    zone14 = Zone.objects.create(name='Santa Cruz de Tenerife', parentZone=zone1_14)
    zone14.save()

    # Castilla y León
    zone15 = Zone.objects.create(name='Ávila', parentZone=zone1_12)
    zone15.save()

    zone16 = Zone.objects.create(name='Burgos', parentZone=zone1_12)
    zone16.save()

    zone17 = Zone.objects.create(name='León', parentZone=zone1_12)
    zone17.save()

    zone18 = Zone.objects.create(name='Palencia', parentZone=zone1_12)
    zone18.save()

    zone19 = Zone.objects.create(name='Salamanca', parentZone=zone1_12)
    zone19.save()

    zone20 = Zone.objects.create(name='Segovia', parentZone=zone1_12)
    zone20.save()

    zone21 = Zone.objects.create(name='Soria', parentZone=zone1_12)
    zone21.save()

    zone22 = Zone.objects.create(name='Valladolid', parentZone=zone1_12)
    zone22.save()

    zone23 = Zone.objects.create(name='Zamora', parentZone=zone1_12)
    zone23.save()

    # Castilla-La Mancha
    zone24 = Zone.objects.create(name='Albacete', parentZone=zone1_1)
    zone24.save()

    zone25 = Zone.objects.create(name='Ciudad Real', parentZone=zone1_1)
    zone25.save()

    zone26 = Zone.objects.create(name='Cuenca', parentZone=zone1_1)
    zone26.save()

    zone27 = Zone.objects.create(name='Guadalajara', parentZone=zone1_1)
    zone27.save()

    zone28 = Zone.objects.create(name='Toledo', parentZone=zone1_1)
    zone28.save()

    # Cataluña
    zone29 = Zone.objects.create(name='Barcelona', parentZone=zone1_4)
    zone29.save()

    zone30 = Zone.objects.create(name='Girona', parentZone=zone1_4)
    zone30.save()

    zone31 = Zone.objects.create(name='Lleida', parentZone=zone1_4)
    zone31.save()

    zone32 = Zone.objects.create(name='Tarragona', parentZone=zone1_4)
    zone32.save()

    # Valencia
    zone33 = Zone.objects.create(name='Alicante', parentZone=zone1_3)
    zone33.save()

    zone34 = Zone.objects.create(name='Castellón', parentZone=zone1_3)
    zone34.save()

    zone35 = Zone.objects.create(name='Valencia', parentZone=zone1_3)
    zone35.save()

    # Extremadura
    zone36 = Zone.objects.create(name='Badajoz', parentZone=zone1_17)
    zone36.save()

    zone37 = Zone.objects.create(name='Cáceres', parentZone=zone1_17)
    zone37.save()

    # Galicia
    zone38 = Zone.objects.create(name='A Coruña', parentZone=zone1_11)
    zone38.save()

    zone39 = Zone.objects.create(name='Lugo', parentZone=zone1_11)
    zone39.save()

    zone40 = Zone.objects.create(name='Ourense', parentZone=zone1_11)
    zone40.save()

    zone41 = Zone.objects.create(name='Pontevedra', parentZone=zone1_11)
    zone41.save()

    # País vasco
    zone42 = Zone.objects.create(name='Álava', parentZone=zone1_8)
    zone42.save()

    zone43 = Zone.objects.create(name='Guipuzkoa', parentZone=zone1_8)
    zone43.save()

    zone44 = Zone.objects.create(name='Bizkaia', parentZone=zone1_8)
    zone44.save()

    # Users...

    # ...musician

    # username = carlosdj        password = make_password('0b10a1e2c186b89a0e15f4b1a84bac20')
    user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                        first_name='Carlos', last_name='Campos Cuesta',
                                        email=users_artists_email)  # 'infoaudiowar@gmail.com'
    user1_artist1.save()

    # username = fromthenoise    password = make_password('b0190558c7add4f8f8067907d372cbc0')
    user2_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                        first_name='José Antonio', last_name='Granero Guzmán',
                                        email=users_artists_email)  # josegraneroguzman@gmail.com
    user2_artist2.save()

    # username = lossaraos       password = make_password('e8b86eae8ad14c1520bfdc0a4781fb79')
    user3_artist3 = User.objects.create(username='artist3', password=make_password('artist3artist3'),
                                        first_name='Francisco', last_name='Martín',
                                        email=users_artists_email)  # saralcum@gmail.com
    user3_artist3.save()

    # username = anadj           password = make_password('fe6a8fd16a97020ca074b1fa00eda0d3')
    user4_artist4 = User.objects.create(username='artist4', password=make_password('artist4artist4'), first_name='Ana',
                                        last_name='Mellado González',
                                        email=users_artists_email)  # mellizalez@hotmail.com
    user4_artist4.save()

    # username = pasando         password = make_password('33fab3ca79958b5d59c3ac5781fac357')
    user5_artist5 = User.objects.create(username='artist5', password=make_password('artist5artist5'),
                                        first_name='Alejandro', last_name='Arteaga Ramírez',
                                        email=users_artists_email)  # alejandroarteagaramirez@gmail.com
    user5_artist5.save()

    # username = sinclase        password = make_password('dc58c65d968ce4aec9e5f20a41a349ed')
    user6_artist6 = User.objects.create(username='artist6', password=make_password('artist6artist6'),
                                        first_name='Pablo', last_name='Delgado Flores',
                                        email=users_artists_email)  # pabloj.df@gmail.com
    user6_artist6.save()

    # username = batracio        password = make_password('0bb2adacaa1cbdab1878f9dfafd509df')
    user7_artist7 = User.objects.create(username='artist7', password=make_password('artist7artist7'),
                                        first_name='Domingo', last_name='Muñoz Daza',
                                        email=users_artists_email)  # dmunnoz96@gmail.com
    user7_artist7.save()

    # username = medictum        password = make_password('a2ff5e4313effd9f4326ff851835cc1c')
    user8_artist8 = User.objects.create(username='artist8', password=make_password('artist8artist8'),
                                        first_name='Rafael', last_name='Córdoba',
                                        email=users_artists_email)  # contacto@medictum.es
    user8_artist8.save()

    # username = waterdogs       password = make_password('ef3e7a1268790f2adb70a89d4918310f')
    user9_artist9 = User.objects.create(username='artist9', password=make_password('artist9artist9'),
                                        first_name='José Luis', last_name='Salvador Lauret',
                                        email=users_artists_email)  # joseluis.salvador@gmail.com
    user9_artist9.save()

    # Famous artist
    # TAMTA

    # username = tamta           password = make_password('1daf86d4c5b00ce4374e2c745371a842')
    user1_artist10 = User.objects.create(username='tamta', password=make_password('tamta'), first_name='Tamta',
                                         last_name='Goduadze', email=users_artists_email)
    user1_artist10.save()

    artist10 = Artist.objects.create(user=user1_artist10, rating=5.0, phone='600304999',
                                     language='en',
                                     photo='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_photo.jpg',
                                     iban='ES6621000418401234567891', paypalAccount='tamta.info@gmail.com')
    artist10.save()

    portfolio10 = Portfolio.objects.create(artisticName='Tamta',
                                           artist=artist10,
                                           banner='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_banner.jpeg',
                                           biography='Tamta, is a Georgian-Greek singer. She first achieved popularity in Greece and Cyprus in 2004 for her participation in Super Idol Greece, in which she placed second. She went on to release several charting albums and singles in Greece and Cyprus. Goduadze became a mentor on X Factor Georgia in 2014, and The X Factor Greece in 2016.')

    portfolio10.artisticGender.add(artistic_gender1)
    portfolio10.zone.add(zone0)
    portfolio10.save()

    portfolio10.artisticGender.add(artistic_gender3)
    portfolio10.zone.add(zone0)
    portfolio10.save()

    portfolio10_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Tv show',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_porfoliomodule1.jpg')
    portfolio10_module1.save()

    portfolio10_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Spot show',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_porfoliomodule2.png')
    portfolio10_module2.save()

    portfolio10_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Show',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_porfoliomodule3.jpg')
    portfolio10_module3.save()

    portfolio10_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Videoclip',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_porfoliomodule4.gif')
    portfolio10_module4.save()

    portfolio10_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='New clip',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist10/artist10_porfoliomodule5.jpg')
    portfolio10_module5.save()

    portfolio10_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Replay',
                                                         link='https://www.youtube.com/watch?v=ESkhPXfl4A0')
    portfolio10_module6.save()

    portfolio10_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Πες Μου Αν Τολμάς',
                                                         link='https://www.youtube.com/watch?v=LiD1kiUF9CQ')
    portfolio10_module7.save()

    portfolio10_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Tag You In My Sky',
                                                         link='https://www.youtube.com/watch?v=9G7FMG1ar1w')
    portfolio10_module8.save()

    portfolio10_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Don’t Kiss Goodbye',
                                                         link='https://www.youtube.com/watch?v=S3BagUEA-LU')
    portfolio10_module9.save()

    availableDays10 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar10 = Calendar.objects.create(days=availableDays10, portfolio=portfolio10)
    calendar10.save()

    performance1_paymentPackageFamous1 = Performance.objects.create(info='This is only mi pay for mi top 8 songs',
                                                                    hours=1.5, price=200)
    performance1_paymentPackageFamous1.save()

    paymentPackage1_performanceFamous1 = PaymentPackage.objects.create(
        description='I can do this for this price, but not include equipment',
        portfolio=portfolio10,
        performance=performance1_paymentPackageFamous1)
    paymentPackage1_performanceFamous1.save()

    fare1_paymentPackageFamous1 = Fare.objects.create(priceHour=250)

    fare1_paymentPackageFamous1.save()

    paymentPackage2_fareFamous1 = PaymentPackage.objects.create(description='I can do this for this price, but not include equipment',
                                                                portfolio=portfolio10,
                                                                fare=fare1_paymentPackageFamous1)
    paymentPackage2_fareFamous1.save()

    custom1_paymentPackageFamous1 = Custom.objects.create(minimumPrice=150)
    custom1_paymentPackageFamous1.save()

    paymentPackage3_customFamous1 = PaymentPackage.objects.create(description='This price include my own performancers',
                                                                  portfolio=portfolio10,
                                                                  custom=custom1_paymentPackageFamous1)
    paymentPackage3_customFamous1.save()

    # Rosalia
    # username = rosalia           password = make_password('05a1e379e057d61c93884b389d23563b')
    user1_artist11 = User.objects.create(username='rosalia', password=make_password('rosalia'), first_name='Rosalía',
                                         last_name='Vila Tobella', email=users_artists_email)
    user1_artist11.save()

    artist11 = Artist.objects.create(user=user1_artist11, rating=5.0, phone='600304999',
                                     language='en',
                                     photo='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_photo.gif',
                                     iban='ES6621000418401234567891', paypalAccount='rosalia.info@gmail.com')
    artist11.save()

    portfolio11 = Portfolio.objects.create(artisticName='Rosalía',
                                           artist=artist11,
                                           banner='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_banner.jpg',
                                           biography='She is a Spanish singer and actress. In 2018 she became the most Latin Grammy Award winning Spaniard for a single work. Her song "Malamente" won two awards out of five nominations.')

    portfolio11.artisticGender.add(artistic_gender1)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11.artisticGender.add(artistic_gender3)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11.artisticGender.add(artistic_gender5)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Interview',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_porfoliomodule1.jpg')
    portfolio11_module1.save()

    portfolio11_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Billboard',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_porfoliomodule2.jpg')
    portfolio11_module2.save()

    portfolio11_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Interview',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_porfoliomodule3.jpeg')
    portfolio11_module3.save()

    portfolio11_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Videoclip malamente',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_porfoliomodule4.gif')
    portfolio11_module4.save()

    portfolio11_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Concert',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist11/artist11_porfoliomodule5.jpg')
    portfolio11_module5.save()

    portfolio11_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='Con Altura',
                                                         link='https://www.youtube.com/watch?v=ESkhPXfl4A0')
    portfolio11_module6.save()

    portfolio11_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='MALAMENTE ',
                                                         link='https://www.youtube.com/watch?v=Rht7rBHuXW8')
    portfolio11_module7.save()

    portfolio11_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='DI MI NOMBRE',
                                                         link='https://www.youtube.com/watch?v=mUBMPaj0L3o')
    portfolio11_module8.save()

    portfolio11_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='BAGDAD ',
                                                         link='https://www.youtube.com/watch?v=Q2WOIGyGzUQ')
    portfolio11_module9.save()

    portfolio11_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                          description='De Plata',
                                                          link='https://www.youtube.com/watch?v=NfDEEyg3AdA')
    portfolio11_module10.save()

    availableDays11 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar11 = Calendar.objects.create(days=availableDays11, portfolio=portfolio11)
    calendar11.save()

    performance1_paymentPackageFamous2 = Performance.objects.create(
        info='I can sign my new 7 songs',
        hours=2, price=500)

    performance1_paymentPackageFamous2.save()

    paymentPackage1_performanceFamous2 = PaymentPackage.objects.create(
        description='This price include my own performancers',
        portfolio=portfolio11,
        performance=performance1_paymentPackageFamous2)
    paymentPackage1_performanceFamous2.save()

    fare1_paymentPackageFamous2 = Fare.objects.create(priceHour=250)
    fare1_paymentPackageFamous2.save()

    paymentPackage2_fareFamous2 = PaymentPackage.objects.create(description='This price is without equipment',
                                                                portfolio=portfolio11,
                                                                fare=fare1_paymentPackageFamous2)
    paymentPackage2_fareFamous2.save()

    custom1_paymentPackageFamous2 = Custom.objects.create(minimumPrice=350)
    custom1_paymentPackageFamous2.save()

    paymentPackage3_customFamous2 = PaymentPackage.objects.create(
        description='This price is without equipment',
        portfolio=portfolio11,
        custom=custom1_paymentPackageFamous2)
    paymentPackage3_customFamous2.save()

    # Taylor Swift
    # username = username='taylor'              password = make_password('c8c7afe225a5f142f33f38da472081c5')
    user1_artist12 = User.objects.create(username='taylor', password=make_password('taylor'),
                                         first_name='Taylor Alison',
                                         last_name='Swift', email=users_artists_email)
    user1_artist12.save()

    artist12 = Artist.objects.create(user=user1_artist12, rating=5.0, phone='600304999',
                                     language='en',
                                     photo='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist11_photo.jpg',
                                     iban='ES6621000418401234567891', paypalAccount='taylor.info@gmail.com')
    artist12.save()

    portfolio12 = Portfolio.objects.create(artisticName='Taylor Swift',
                                           artist=artist12,
                                           banner='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist11_banner.jpg',
                                           biography='Is an American singer-songwriter. As one of the world`s leading contemporary recording artists, she is known for narrative songs about her personal life, which has received widespread media coverage.')

    portfolio12.artisticGender.add(artistic_gender1)
    portfolio12.zone.add(zone0)
    portfolio12.save()

    portfolio12.artisticGender.add(artistic_gender3)
    portfolio12.zone.add(zone0)
    portfolio12.save()

    portfolio12_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Paper',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist12_porfoliomodule1.jpg')
    portfolio12_module1.save()

    portfolio12_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Interview',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist12_porfoliomodule2.jpg')
    portfolio12_module2.save()

    '''
    portfolio12_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Smile',
                                                         link='https://em.wattpad.com/67028e42a9ebd5c53342cae98d2082deb0d12424/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f51387a68664f58415a73575937773d3d2d32372e313536343431653536393831363236393135363633353535333030392e676966?s=fit&w=720&h=720')
    portfolio12_module3.save()


    portfolio12_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Videoclip rainbow',
                                                         link='https://www.nacionrex.com/__export/1548185009356/sites/debate/img/2019/01/22/taylor_swift_cats_bombalurina_personaje_quien_es_foto_instagram_2019_crop1548184963929.jpg_1834093470.jpg')
    portfolio12_module4.save()
    '''

    portfolio12_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Concert',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist12_porfoliomodule5.jpg')
    portfolio12_module5.save()

    portfolio12_module6 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Interview',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist12/artist12_porfoliomodule6.jpg')
    portfolio12_module6.save()

    portfolio12_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Delicate ',
                                                         link='https://www.youtube.com/watch?v=tCXGJQYZ9JA')
    portfolio12_module7.save()

    portfolio12_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Ready For It',
                                                         link='https://www.youtube.com/watch?v=wIft-t-MQuE')
    portfolio12_module8.save()

    portfolio12_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Look What You Made Me Do',
                                                         link='https://www.youtube.com/watch?v=3tmd-ClpJxA')
    portfolio12_module9.save()

    portfolio12_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                          description='Wildest Dreams',
                                                          link='https://www.youtube.com/watch?v=IdneKLhsWOQ')
    portfolio12_module10.save()

    portfolio12_module11 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                          description='Style',
                                                          link='https://www.youtube.com/watch?v=-CmadmM5cOk')
    portfolio12_module11.save()

    availableDays12 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar12 = Calendar.objects.create(days=availableDays12, portfolio=portfolio12)
    calendar12.save()

    performance1_paymentPackageFamous3 = Performance.objects.create(
        info='I only play my songs of Reputation disc',
        hours=2, price=325)

    performance1_paymentPackageFamous3.save()

    paymentPackage1_performanceFamous3 = PaymentPackage.objects.create(
        description='This price is with equipment',
        portfolio=portfolio12,
        performance=performance1_paymentPackageFamous3)
    paymentPackage1_performanceFamous3.save()

    fare1_paymentPackageFamous3 = Fare.objects.create(priceHour=231)
    fare1_paymentPackageFamous3.save()

    paymentPackage2_fareFamous3 = PaymentPackage.objects.create(
        description='This price is without equipment, if you need equipment, use my performance package',
        portfolio=portfolio12,
        fare=fare1_paymentPackageFamous3)
    paymentPackage2_fareFamous3.save()

    custom1_paymentPackageFamous3 = Custom.objects.create(minimumPrice=763)
    custom1_paymentPackageFamous3.save()

    paymentPackage3_customFamous3 = PaymentPackage.objects.create(
        description='This price is without equipment',
        portfolio=portfolio12,
        custom=custom1_paymentPackageFamous3)
    paymentPackage3_customFamous3.save()

    # Charli XCX
    # username = charli             password = make_password('76734a16cd99ce80128ab37468d353d2')
    user1_artist13 = User.objects.create(username='charli', password=make_password('charli'),
                                         first_name='Charlotte Emma',
                                         last_name='Aitchison', email=users_artists_email)
    user1_artist13.save()

    artist13 = Artist.objects.create(user=user1_artist13, rating=5.0, phone='600304999',
                                     language='en',
                                     photo='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_photo.gif',
                                     iban='ES6621000418401234567891', paypalAccount='charli.info@gmail.com')
    artist13.save()

    portfolio13 = Portfolio.objects.create(artisticName='Charli XCX',
                                           artist=artist13,
                                           banner='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_banner.jpg',
                                           biography='Is an American singer-songwriter. As one of the world`s leading contemporary recording artists, she is known for narrative songs about her personal life, which has received widespread media coverage.')

    portfolio13.artisticGender.add(artistic_gender1)
    portfolio13.zone.add(zone0)
    portfolio13.save()

    portfolio13.artisticGender.add(artistic_gender3)
    portfolio13.zone.add(zone0)
    portfolio13.save()

    '''
    portfolio13_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Road',
                                                         link='https://www.musicmundial.com/wp-content/uploads/2018/02/charli-xcx.jpg')
    portfolio13_module1.save()
    '''

    portfolio13_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Paper',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_porfoliomodule2.jpg')
    portfolio13_module2.save()

    portfolio13_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Old Profile',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_porfoliomodule3.jpg')
    portfolio13_module3.save()

    portfolio13_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Old style',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_porfoliomodule4.jpg')
    portfolio13_module4.save()

    portfolio13_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Concert',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist13/artist13_porfoliomodule5.jpg')
    portfolio13_module5.save()

    portfolio13_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Troye Sivan',
                                                         link='https://www.youtube.com/watch?v=6-v1b9waHWY')
    portfolio13_module7.save()

    portfolio13_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Girls Night Out',
                                                         link='https://www.youtube.com/watch?v=IFr3GnboNRU')
    portfolio13_module8.save()

    portfolio13_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Backseat',
                                                         link='https://www.youtube.com/watch?v=hiGqKwy4yM0')
    portfolio13_module9.save()

    portfolio13_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                          description=' I Love It',
                                                          link='https://www.youtube.com/watch?v=UxxajLWwzqY')
    portfolio13_module10.save()

    availableDays13 = []

    calendar13 = Calendar.objects.create(days=availableDays13, portfolio=portfolio13)
    calendar13.save()

    # ...admins

    user14_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True,
                                       is_superuser=True, first_name='Chema', last_name='Alonso',
                                       email="grupogrooving@gmail.com")
    user14_admin.save()
    Admin.objects.create(user=user14_admin, language='es')

    # Artists

    artist1 = Artist.objects.create(user=user1_artist1, rating=0, phone='600304999',
                                    language='en',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist1/artist1_photo.jpg',
                                    iban='ES6621000418401234567891', paypalAccount='carlosdj.espectaculos@gmail.com')
    artist1.save()
    artist2 = Artist.objects.create(user=user2_artist2, rating=0, phone='695099812',
                                    language='es',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_photo.jpg',
                                    iban='ES1720852066623456789011', paypalAccount='fromthenois3@gmail.com')
    artist2.save()
    artist3 = Artist.objects.create(user=user3_artist3, rating=0, phone='695990241',
                                    language='en',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist3/artist3_photo.jpg',
                                    iban='ES6000491500051234567892', paypalAccount='saraos.flamenco@gmail.com')
    artist3.save()
    artist4 = Artist.objects.create(user=user4_artist4, rating=0, phone='610750391',
                                    language='es',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist4/artist4_photo.jpg',
                                    iban='ES9420805801101234567891', paypalAccount='anadj.session@outlook.com')
    artist4.save()
    artist5 = Artist.objects.create(user=user5_artist5, rating=0, phone='675181175',
                                    language='en',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist5/artist5_photo.jpg',
                                    iban='ES9000246912501234567891', paypalAccount='chirigota_pasando@hotmail.com')
    artist5.save()
    artist6 = Artist.objects.create(user=user6_artist6, rating=0, phone='673049277',
                                    language='es',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist6/artist6_photo.jpg',
                                    iban='ES7100302053091234567895', paypalAccount='chirigotasinclase@yahoo.com')
    artist6.save()
    artist7 = Artist.objects.create(user=user7_artist7, rating=0, phone='664196105',
                                    language='es',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist7/artist7_photo.jpg',
                                    iban='ES1000492352082414205416', paypalAccount='batracio-info@hotmail.com')
    artist7.save()
    artist8 = Artist.objects.create(user=user8_artist8, rating=0, phone='664596466',
                                    language='en',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_photo.jpg',
                                    iban='ES1720852066623456789011', paypalAccount='medictum.bussiness@gmail.com')
    artist8.save()
    artist9 = Artist.objects.create(user=user9_artist9, rating=0, phone='679739257',
                                    language='es',
                                    photo='https://raw.githubusercontent.com/grooving/static-content/master/artist9/artist9_photo.jpg',
                                    iban='ES9420805801101234567891', paypalAccount='infowaterdogs@outlook.com')
    artist9.save()

    # Portfolios with his modules

    portfolio1 = Portfolio.objects.create(artisticName='Carlos DJ',
                                          artist=artist1,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist1/artist1_banner.jpg',
                                          biography='Musician, producer, DJ, pianist, promoter, and electronic music enthusiast alike, David Michael hails out of Dayton, Ohio.  When not performing, he spends his time in the studio creating his own music… aided by over a decade of piano lessons and an upbringing in a very musically-influenced home.  Having spent many years playing at all of the major local night clubs (alongside local hard-hitters and national acts alike), holding multiple residencies, DJing special events and promoting his own shows, David has had a lot of time to develop his sound.  For him, it’s all about mood and a deep, hypnotic groove… playing those tracks that get you tapping your feet and nodding your head without you realizing it, regardless of genre, tempo, style, or release date. Don’t be surprised when you suddenly find yourself dancing')
    portfolio1.artisticGender.add(artistic_gender2)
    portfolio1.zone.add(zone23)
    portfolio1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio1,
                                                        description='It was a great festival',
                                                        link='https://www.youtube.com/watch?v=xAzWJCwZY6w')
    portfolio1_module1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio1,
                                                        description='Video with Kill Clown',
                                                        link='https://www.youtube.com/watch?v=BDhUtaS4GT8')
    portfolio1_module1.save()

    # ----

    portfolio2 = Portfolio.objects.create(artisticName='From the noise',
                                          artist=artist2,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_banner.jpg',
                                          biography='Somos un grupo de Sevilla, formado el 2010, somos 6 componentes y tocamos un estilo muy alternativo que mezcla hip hop con rock, electrónica y metal. Tenemos melodías y letras contudentes. Estamos bastante bien aceptados en nuestro entorno y nos gustaría expandirnos más. Queremos tocar allí donde sea posible y que nos ayude a darnos a conocer.')
    portfolio2.artisticGender.add(artistic_gender4)
    portfolio2.zone.add(zone2)
    portfolio2.save()

    portfolio2_module1 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio2,
                                                        link='https://www.facebook.com/fromthenoise/')
    portfolio2_module1.save()

    portfolio2_module2 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2,
                                                        link='https://www.youtube.com/watch?v=CEaJ-COP9Rs')
    portfolio2_module2.save()

    portfolio2_module3 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2,
                                                        link='https://www.youtube.com/watch?v=hWAO0tHxqLo')
    portfolio2_module3.save()

    portfolio2_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2,
                                                        link='https://www.youtube.com/watch?v=OnuzoSXS4_c')
    portfolio2_module4.save()

    portfolio2_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio2,
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_porfoliomodule5.jpg')
    portfolio2_module5.save()

    portfolio2_module6 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio2,
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_porfoliomodule6.jpg')
    portfolio2_module6.save()

    portfolio2_module7 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio2,
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_porfoliomodule7.jpg')
    portfolio2_module7.save()

    portfolio2_module8 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio2,
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist2/artist2_porfoliomodule8.jpg')
    portfolio2_module8.save()

    # ----

    portfolio3 = Portfolio.objects.create(artisticName='Los saraos',
                                          artist=artist3,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist3/artist3_banner.jpg',
                                          biography='Considerados una de las principales figuras del flamenco actual, se le atribuye la responsabilidad de la reforma que llevó este arte a la escena musical internacional gracias a la inclusión de nuevos ritmos desde el jazz, la bossa nova y la música clásica. De este modo destacan sus colaboraciones con artistas internacionales como Carlos Santana, Al Di Meola o John McLaughlin, pero también con otras figuras del flamenco como Camarón de la Isla o Tomatito, con quienes modernizó el concepto de flamenco clásico.')
    portfolio3.artisticGender.add(artistic_gender5)
    portfolio3.zone.add(zone2)
    portfolio3.save()

    portfolio3_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio3,
                                                        description='Grupo Flamenco Saraos - 1',
                                                        link='https://www.youtube.com/watch?v=V599AxrB7P4')
    portfolio3_module4.save()

    portfolio3_module5 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio3,
                                                        description='Grupo Flamenco Saraos - 2',
                                                        link='https://www.youtube.com/watch?v=PZA5WVWzJd0')
    portfolio3_module5.save()

    # ----

    portfolio4 = Portfolio.objects.create(artisticName='Ana DJ',
                                          artist=artist4,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist4/artist4_banner.jpg',
                                          biography='She may have been ‘born to be a DJ’, but sheer hard work and dedication are what’s brought ANNA success. In São Paulo, the traffic jams can stretch over a hundred miles on a bad day. Trapped under scorching sun or torrential rain, the air chewy and warm regardless, cars trudge along its roads and raised highways. Trees and shrubbery bring colour to the worn-out streets, sand-coloured and mirrored tower blocks looming large over the city. Beneath a concrete underpass in the north of the city, ANNA, aka DJ Ana Miranda, is making an emphatic return to the city that shaped her.')
    portfolio4.zone.add(zone4)
    portfolio4.artisticGender.add(artistic_gender2)
    portfolio4.save()

    portfolio4_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio4,
                                                        description='ANNA techno set at CRSSD Fest | Spring 2018',
                                                        link='https://www.youtube.com/watch?v=Up67slBkyRs')
    portfolio4_module1.save()

    portfolio4_module2 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio4,
                                                        description='ANNA Live from DJ Mag HQ',
                                                        link='https://www.youtube.com/watch?v=SCAHe6T-gK4')
    portfolio4_module2.save()

    # ----

    portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente',
                                          artist=artist5,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist5/artist5_banner.jpg',
                                          biography='En 1989 monta la chirigota Los sanmolontropos con una música y una letra muy extraña que llama la atención hasta el punto que entran en la Final, de manera inesperada, sorprendiendo a propios y extraños. Siguiendo con esa línea de locura y surrealismo, al año siguiente saca la chirigota Carnaval 2036 Piconeros Galácticos. Se pregunta si pueden salir los 18 amigos en el Falla y decide hacer dos chirigotas. Le supuso un grandísimo esfuerzo y crea Ballet zum zum malacatum y El que la lleva la entiende (Los borrachos), en las que lleva la misma línea de surrealismo, pero pide por favor que fuera una chirigota interpretada porque le gusta mucho hacerse el borracho.')
    portfolio5.artisticGender.add(artistic_gender8)
    portfolio5.zone.add(zone4)
    portfolio5.save()
    portfolio5.zone.add(zone1_10)
    portfolio5.save()

    portfolio5_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio5,
                                                        description='ANNA Live from DJ Mag HQ',
                                                        link='https://www.youtube.com/watch?v=W-8oEgRg5e8')
    portfolio5_module1.save()

    # ----

    portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase',
                                          artist=artist6,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist6/artist6_banner.jpg',
                                          biography='En 1989 monta la chirigota Los sanmolontropos con una música y una letra muy extraña que llama la atención hasta el punto que entran en la Final, de manera inesperada, sorprendiendo a propios y extraños. Siguiendo con esa línea de locura y surrealismo, al año siguiente saca la chirigota Carnaval 2036 Piconeros Galácticos. Se pregunta si pueden salir los 18 amigos en el Falla y decide hacer dos chirigotas. Le supuso un grandísimo esfuerzo y crea Ballet zum zum malacatum y El que la lleva la entiende (Los borrachos), en las que lleva la misma línea de surrealismo, pero pide por favor que fuera una chirigota interpretada porque le gusta mucho hacerse el borracho.')
    portfolio6.artisticGender.add(artistic_gender8)
    portfolio6.zone.add(zone2)
    portfolio6.save()
    portfolio6.zone.add(zone29)
    portfolio6.save()
    portfolio6_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio6,
                                                        description='Una chirigota sin clase - Preliminares',
                                                        link='https://www.youtube.com/watch?v=zm6JyvxOcd8')
    portfolio6_module1.save()

    portfolio6_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio6,
                                                        description='Actuación en el Falla 2019 - 1',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist6/artist6_porfoliomodule2.jpg')
    portfolio6_module2.save()

    portfolio6_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio6,
                                                        description='Actuación en el Falla 2019 - 2',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist6/artist6_porfoliomodule3.jpg')
    portfolio6_module3.save()

    # ----

    portfolio7 = Portfolio.objects.create(artisticName='Batracio',
                                          artist=artist7,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist7/artist7_banner.jpg',
                                          biography='Batracio nace en 2015, fruto de una reunión entre viejos amigos, Febes (voz) y José Alberto (guitarra) cansados de hacer en anteriores formaciones ḿúsica más genérica. De ahí no sólo nació una banda, sino que surgieron dos de sus temas más emblemáticos. La Charca y Pulgadas. Esto motivó a seguir adelante y continuar con un proyecto al que luego se sumarían Juan Bidegain (bajo), José Manuel Rodríguez “Negro” (teclado) y Javier Galliza (batería). Tras añadirse Domingo Muñoz (trombón) a la formación, sucedió el increíble debut en una mítica sala FunClub totalmente abarrotada. A partir de ese momento, las composiciones giraron hacia el Ska-funk característico de la banda. En 2016 la banda volvía al estudio para darle vida a Famelia y Souciedad.')
    portfolio7.artisticGender.add(artistic_gender3)
    portfolio7.artisticGender.add(artistic_gender4)
    portfolio7.zone.add(zone2)
    portfolio7.save()
    portfolio7.zone.add(zone1_13)
    portfolio7.save()

    portfolio7_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio7, description='Group photo',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist7/artist7_porfoliomodule1.jpg')
    portfolio7_module1.save()

    portfolio7_module2 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio7,
                                                        description='Canal de Facebook',
                                                        link='https://www.facebook.com/batraciosvq/')
    portfolio7_module2.save()

    portfolio7_module3 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio7,
                                                        description='Canal de Twitter',
                                                        link='https://twitter.com/batraciosvq')
    portfolio7_module3.save()

    portfolio7_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='No vuelvas ft Chusta (La Selva Sur)',
                                                        link='https://www.youtube.com/watch?v=g43nbmB1cD8')
    portfolio7_module4.save()

    portfolio7_module5 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='Bona Fortuna',
                                                        link='https://www.youtube.com/watch?v=GB9AG5hDx4E')
    portfolio7_module5.save()

    portfolio7_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='Souciedad',
                                                        link='https://www.youtube.com/watch?v=g7zqDQhxzzc')
    portfolio7_module6.save()

    portfolio7_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='La Charca',
                                                        link='https://www.youtube.com/watch?v=WuLcH_W6iPg')
    portfolio7_module7.save()

    portfolio7_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='Yo No Tonto Tanto',
                                                        link='https://www.youtube.com/watch?v=MC0nvRgKR30')
    portfolio7_module8.save()

    portfolio7_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='Directo en Espartinas (La Raíz + Batracio + Sonido Vegetal)',
                                                        link='https://www.youtube.com/watch?v=GdQQUYCfSGw')
    portfolio7_module9.save()

    portfolio7_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                         description='Moskojonera',
                                                         link='https://www.youtube.com/watch?v=9i2rM6dd5yA')
    portfolio7_module10.save()

    portfolio7_module11 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio7, description='Group 1',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist7/artist7_porfoliomodule11.jpg')
    portfolio7_module11.save()

    portfolio7_module12 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio7, description='Group 2',
                                                         link='https://raw.githubusercontent.com/grooving/static-content/master/artist7/artist7_porfoliomodule12.jpg')
    portfolio7_module12.save()

    # ----

    portfolio8 = Portfolio.objects.create(artisticName='Medictum',
                                          artist=artist8,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_banner.jpg',
                                          biography='MedictuM es una banda que surge en 2012 de la mano de los hermanos Antonio y Manuel Medina en su pueblo natal, Morón de la Frontera. Tras el paso de ambos por grupos locales, deciden crear su propio proyecto con toques de thrash metal, heavy metal clásico, pinceladas de hard rock y otros estilos.')
    portfolio8.artisticGender.add(artistic_gender3)
    portfolio8.artisticGender.add(artistic_gender4)
    portfolio8.zone.add(zone2)
    portfolio8.save()

    portfolio8_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8, description='New disc!!!',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_porfoliomodule1.jpg')
    portfolio8_module1.save()

    portfolio8_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8,
                                                        description='Antonio Medina',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_porfoliomodule2.jpg')
    portfolio8_module2.save()

    portfolio8_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8,
                                                        description='Manuel Medina',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_porfoliomodule3.jpg')
    portfolio8_module3.save()

    portfolio8_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8,
                                                        description='Rafael Córdoba',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_porfoliomodule4.jpg')
    portfolio8_module4.save()

    portfolio8_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8, description='Pablo Pérez',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist8/artist8_porfoliomodule5.jpg')
    portfolio8_module5.save()

    portfolio8_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - El país de las pesadillas',
                                                        link='https://www.youtube.com/watch?v=EdUFDOM4lrU')
    portfolio8_module6.save()

    portfolio8_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Sala Palo Palo',
                                                        link='https://www.youtube.com/watch?v=bgqfkpxH5h0')
    portfolio8_module7.save()

    portfolio8_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=fYzhR6g9J-4')
    portfolio8_module8.save()

    portfolio8_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=9wSTyCbDicE')
    portfolio8_module9.save()

    # ----

    portfolio9 = Portfolio.objects.create(artisticName='Waterdogs',
                                          artist=artist9,
                                          banner='https://raw.githubusercontent.com/grooving/static-content/master/artist9/artist9_banner.jpg',
                                          biography='Un potente trío de Rock-Blues nacido a orillas del delta del Piedras')
    portfolio9.artisticGender.add(artistic_gender3)
    portfolio9.artisticGender.add(artistic_gender4)
    portfolio9.zone.add(zone4)
    portfolio9.save()
    portfolio9.zone.add(zone22)
    portfolio9.save()

    portfolio9_module1 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio9,
                                                        description='Canal de Facebook',
                                                        link='https://www.facebook.com/WATERDOGS.BLUES/')
    portfolio9_module1.save()

    portfolio9_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio9,
                                                        description='Foto 1',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist9/artist9_porfoliomodule2.jpg')
    portfolio9_module2.save()

    portfolio9_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio9,
                                                        description='Foto 2',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist9/artist9_porfoliomodule3.jpg')
    portfolio9_module3.save()

    portfolio9_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio9,
                                                        description='Foto 3',
                                                        link='https://raw.githubusercontent.com/grooving/static-content/master/artist9/artist9_porfoliomodule4.jpg')
    portfolio9_module4.save()
    availableDays9 = []

    calendar9 = Calendar.objects.create(days=availableDays9, portfolio=portfolio9)
    calendar9.save()

    # Calendar

    availableDays1 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                      '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar1 = Calendar.objects.create(days=availableDays1, portfolio=portfolio1)
    calendar1.save()

    availableDays2 = ['2019-07-05', '2019-07-06', '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-10',
                      '2019-07-11', '2019-08-15', '2019-08-16', '2019-10-13']

    calendar2 = Calendar.objects.create(days=availableDays2, portfolio=portfolio2)
    calendar2.save()

    availableDays3 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                      '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19',
                      '2019-09-01', '2019-09-02', '2019-09-03', '2019-09-04', '2019-09-05', '2019-09-06',
                      '2019-09-07', '2019-09-08', '2019-09-09', '2019-09-10', '2019-09-11', '2019-09-12',
                      '2019-11-13', '2019-09-14', '2019-09-15', '2019-09-16', '2019-09-17', '2019-09-18',
                      '2019-12-21', '2019-12-23', '2019-12-24', '2019-12-25', '2019-12-26', '2019-12-27']

    calendar3 = Calendar.objects.create(days=availableDays3, portfolio=portfolio3)
    calendar3.save()

    availableDays4 = ['2019-05-21', '2019-05-22', '2019-05-23', '2019-05-24', '2019-05-25', '2019-05-26',
                      '2019-05-27', '2019-05-28', '2019-05-29', '2019-05-30', '2019-05-31',
                      '2019-06-01', '2019-06-02', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06',
                      '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-10', '2019-07-11', '2019-07-12',
                      '2019-08-01', '2019-08-02', '2019-08-03', '2019-08-04', '2019-08-05', '2019-08-06',
                      '2019-11-21', '2019-11-22', '2019-11-23', '2019-11-24', '2019-11-25', '2019-11-26']

    calendar4 = Calendar.objects.create(days=availableDays4, portfolio=portfolio4)
    calendar4.save()

    availableDays5 = ['2019-06-01', '2019-06-02', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06',
                      '2019-07-04', '2019-07-05', '2019-07-06', '2019-07-07', '2019-07-08',
                      '2019-08-11', '2019-08-12', '2019-08-13', '2019-08-14', '2019-08-15', '2019-08-16',
                      '2019-08-17', '2019-08-18', '2019-08-19', '2019-08-20', '2019-08-21', '2019-08-22',
                      '2019-09-23', '2019-09-24', '2019-09-25', '2019-09-26', '2019-09-27', '2019-09-28',
                      '2019-11-01', '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-06']

    calendar5 = Calendar.objects.create(days=availableDays5, portfolio=portfolio5)
    calendar5.save()

    availableDays6 = ['2019-04-06', '2019-04-07', '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11',
                      '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16', '2019-04-17',
                      '2019-05-03', '2019-05-04', '2019-05-05', '2019-05-06', '2019-05-07', '2019-05-08',
                      '2019-05-09', '2019-05-10', '2019-05-11', '2019-05-12', '2019-05-13', '2019-05-14',
                      '2019-06-17', '2019-06-18', '2019-06-19', '2019-06-20', '2019-06-21', '2019-06-22',
                      '2019-08-04', '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08']

    calendar6 = Calendar.objects.create(days=availableDays6, portfolio=portfolio6)
    calendar6.save()

    availableDays7 = ['2019-07-24', '2019-07-25', '2019-07-26', '2019-07-27', '2019-07-28', '2019-07-29',
                      '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08', '2019-08-09', '2019-08-10',
                      '2019-09-14', '2019-09-15', '2019-09-06', '2019-09-07', '2019-09-08', '2019-09-09',
                      '2019-11-15', '2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20',
                      '2019-12-17', '2019-12-18', '2019-12-19', '2019-12-20', '2019-12-21', '2019-12-22',
                      '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09']

    calendar7 = Calendar.objects.create(days=availableDays7, portfolio=portfolio7)
    calendar7.save()

    availableDays8 = ['2019-04-06', '2019-04-07', '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11',
                      '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16', '2019-04-17',
                      '2019-05-03', '2019-05-04', '2019-05-05', '2019-05-06', '2019-05-07', '2019-05-08',
                      '2019-05-09', '2019-05-10', '2019-05-11', '2019-05-12', '2019-05-13', '2019-05-14',
                      '2019-06-17', '2019-06-18', '2019-06-19', '2019-06-20', '2019-06-21', '2019-06-22',
                      '2019-08-04', '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08',
                      '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09']

    calendar8 = Calendar.objects.create(days=availableDays8, portfolio=portfolio8)
    calendar8.save()

    # ...customers

    # username = rafesqram         password = make_password('ef3e7a1268790f2adb70a89d4918310f')
    user10_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                           first_name='Rafael', last_name='Esquivias Ramírez',
                                           email=users_customers_email)  # resquiviasramirez@gmail.com
    user10_customer1.save()

    # username = jorjimcor         password = make_password('d54d4c790733f33dba91a68b099f401e')
    user11_customer2 = User.objects.create(username='customer2', password=make_password('customer2customer2'),
                                           first_name='Jorge', last_name='Jimenez',
                                           email=users_customers_email)  # jorjicorral@gmail.com
    user11_customer2.save()

    # username = juamanfer         password = make_password('108832878f600d74fcc5053dc8ff8ffc')
    user12_customer3 = User.objects.create(username='customer3', password=make_password('customer3customer3'),
                                           first_name='Juan Manuel', last_name='Fernández',
                                           email=users_customers_email)  # surlive@imgempresas.com
    user12_customer3.save()

    # username = migromgut         password = make_password('933c6c464ab272bf6241be38f6801826')
    user13_customer4 = User.objects.create(username='customer4', password=make_password('customer4customer4'),
                                           first_name='Miguel', last_name='Romero Gutierrez',
                                           email=users_customers_email)  # La posada Sevilla
    user13_customer4.save()

    # Customers with credit card

    customer1 = Customer.objects.create(user=user10_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                        expirationDate='2020-10-01', number='4651001401188232',
                                        language='en',
                                        paypalAccount='rafesqram@gmail.com')
    customer1.save()

    customer2 = Customer.objects.create(user=user11_customer2, phone='664656659', holder='Jorge Jiménez del Corral',
                                        language='es',
                                        expirationDate='2027-03-01', number='4934521448108546',
                                        paypalAccount='jorjimcor@gmail.com')
    customer2.save()

    customer3 = Customer.objects.create(user=user12_customer3, phone='678415820', holder='Juan Manuel Fernández',
                                        language='en',
                                        expirationDate='2025-10-01', number='4656508395720981',
                                        paypalAccount='juamarfer@gmail.com')
    customer3.save()

    customer4 = Customer.objects.create(user=user13_customer4, phone='627322721', holder='Miguel Romero Gutierrez',
                                        language='es',
                                        expirationDate='2027-03-01', number='4826704855401486',
                                        paypalAccount='migromgut@gmail.com')
    customer4.save()

    # Event location

    event_location1 = EventLocation.objects.create(name="Festival Rockupo",
                                                   address="Universidad Pablo de Olavide",
                                                   description="We only provide the stage with microphones, speakers and a sound technician.",
                                                   zone=zone2,
                                                   customer=customer1)
    event_location1.save()
    event_location2 = EventLocation.objects.create(name="La Posada Sevilla",
                                                   address="C/Astronomía, 42, 41015",
                                                   description="Yes, we have al equipment necessary, we have concerts every week, we have all you need for this job.",
                                                   zone=zone2,
                                                   customer=customer2)
    event_location2.save()
    event_location3 = EventLocation.objects.create(name="Rosalia en vivo", address="C/Sol, 45, 41652",
                                                   equipment="We provided a full sound & video equipment for the event",
                                                   zone=zone2, customer=customer3)
    event_location3.save()
    event_location4 = EventLocation.objects.create(name="Charlie XCX", address='C/Amalgama, 2, 41609',
                                                   description="Yes, we have a stage of 30 square meters, a system of loudspeakers distributed by the local, with a total of 16 loudspeakers and a complete system of LED lights that can be adjusted to the intensity and color desired.",
                                                   zone=zone4, customer=customer4)
    event_location4.save()

    # Payment packages with Payment types

    performance1_paymentPackage1 = Performance.objects.create(info='This price is with equipment',
                                                              hours=1.5, price=50)
    performance1_paymentPackage1.save()

    paymentPackage1_performance1 = PaymentPackage.objects.create(
        description='This price is with equipment',
        portfolio=portfolio1,
        performance=performance1_paymentPackage1)
    paymentPackage1_performance1.save()

    fare1_paymentPackage2 = Fare.objects.create(priceHour=45)
    fare1_paymentPackage2.save()

    paymentPackage2_fare1 = PaymentPackage.objects.create(description='This price is without equipment',
                                                          portfolio=portfolio1,
                                                          fare=fare1_paymentPackage2)
    paymentPackage2_fare1.save()

    custom1_paymentPackage3 = Custom.objects.create(minimumPrice=60)
    custom1_paymentPackage3.save()

    paymentPackage3_custom1 = PaymentPackage.objects.create(description='This price include the equipment',
                                                            portfolio=portfolio1,
                                                            custom=custom1_paymentPackage3)
    paymentPackage3_custom1.save()

    # ----

    performance2_paymentPackage4 = Performance.objects.create(info='This price is without equipment',
                                                              hours=1.5, price=50)
    performance2_paymentPackage4.save()

    paymentPackage4_performance2 = PaymentPackage.objects.create(
        description='This price include an especial begining',
        portfolio=portfolio2,
        performance=performance2_paymentPackage4)
    paymentPackage4_performance2.save()

    fare2_paymentPackage5 = Fare.objects.create(priceHour=45)
    fare2_paymentPackage5.save()

    paymentPackage5_fare2 = PaymentPackage.objects.create(description='This price is without equipment',
                                                          portfolio=portfolio2,
                                                          fare=fare2_paymentPackage5)
    paymentPackage5_fare2.save()

    custom2_paymentPackage6 = Custom.objects.create(minimumPrice=60)
    custom2_paymentPackage6.save()

    paymentPackage6_custom2 = PaymentPackage.objects.create(
        description='This price include the equipment',
        portfolio=portfolio2,
        custom=custom2_paymentPackage6)
    paymentPackage6_custom2.save()

    # ----

    performance3_paymentPackage7 = Performance.objects.create(info='This is performance package from Los saraos.',
                                                              hours=1.5, price=50)
    performance3_paymentPackage7.save()

    paymentPackage7_performance3 = PaymentPackage.objects.create(
        description='This price include the equipment',
        portfolio=portfolio3,
        performance=performance3_paymentPackage7)
    paymentPackage7_performance3.save()

    fare3_paymentPackage8 = Fare.objects.create(priceHour=45)
    fare3_paymentPackage8.save()

    paymentPackage8_fare3 = PaymentPackage.objects.create(description='I only need a chair that is not include in the price',
                                                          portfolio=portfolio3,
                                                          fare=fare3_paymentPackage8)
    paymentPackage8_fare3.save()

    custom3_paymentPackage9 = Custom.objects.create(minimumPrice=60)
    custom3_paymentPackage9.save()

    paymentPackage9_custom3 = PaymentPackage.objects.create(description='This price include the equipment',
                                                            portfolio=portfolio3,
                                                            custom=custom3_paymentPackage9)
    paymentPackage9_custom3.save()

    # ----

    performance4_paymentPackage10 = Performance.objects.create(info='This price include the equipment',
                                                               hours=1.5, price=50)
    performance4_paymentPackage10.save()

    paymentPackage10_performance4 = PaymentPackage.objects.create(
        description='Performance Package',
        portfolio=portfolio4,
        performance=performance4_paymentPackage10)
    paymentPackage10_performance4.save()

    fare4_paymentPackage11 = Fare.objects.create(priceHour=45)
    fare4_paymentPackage11.save()

    paymentPackage11_fare3 = PaymentPackage.objects.create(description='I need equipment',
                                                           portfolio=portfolio4,
                                                           fare=fare4_paymentPackage11)
    paymentPackage11_fare3.save()

    custom4_paymentPackage12 = Custom.objects.create(minimumPrice=60)
    custom4_paymentPackage12.save()

    paymentPackage12_custom4 = PaymentPackage.objects.create(description='This price include the equipment and my own performances',
                                                             portfolio=portfolio4,
                                                             custom=custom4_paymentPackage12)
    paymentPackage12_custom4.save()

    # ----

    performance5_paymentPackage13 = Performance.objects.create(
        info='This price include the equipment',
        hours=1.5, price=50)
    performance5_paymentPackage13.save()

    paymentPackage13_performance5 = PaymentPackage.objects.create(
        description='This price include the equipment',
        portfolio=portfolio5,
        performance=performance5_paymentPackage13)
    paymentPackage13_performance5.save()

    fare5_paymentPackage14 = Fare.objects.create(priceHour=45)
    fare5_paymentPackage14.save()

    paymentPackage14_fare5 = PaymentPackage.objects.create(
        description='This is whithout equipment',
        portfolio=portfolio5,
        fare=fare5_paymentPackage14)
    paymentPackage14_fare5.save()

    custom5_paymentPackage15 = Custom.objects.create(minimumPrice=60)
    custom5_paymentPackage15.save()

    paymentPackage15_custom5 = PaymentPackage.objects.create(
        description='This price include the equipment',
        portfolio=portfolio5,
        custom=custom5_paymentPackage15)
    paymentPackage15_custom5.save()

    # ----

    performance6_paymentPackage16 = Performance.objects.create(
        info='Una chirigota con clase dont need anything',
        hours=1.5, price=50)
    performance6_paymentPackage16.save()

    paymentPackage16_performance6 = PaymentPackage.objects.create(
        description='We have all you need for the performance',
        portfolio=portfolio6,
        performance=performance6_paymentPackage16)
    paymentPackage16_performance6.save()

    fare6_paymentPackage17 = Fare.objects.create(priceHour=45)
    fare6_paymentPackage17.save()

    paymentPackage17_fare6 = PaymentPackage.objects.create(
        description='We have all you need for the performance',
        portfolio=portfolio6,
        fare=fare6_paymentPackage17)
    paymentPackage17_fare6.save()

    custom6_paymentPackage18 = Custom.objects.create(minimumPrice=60)
    custom6_paymentPackage18.save()

    paymentPackage18_custom6 = PaymentPackage.objects.create(
        description='We have all you need for the performance but if you want us in outside, we cant do it',
        portfolio=portfolio6,
        custom=custom6_paymentPackage18)
    paymentPackage18_custom6.save()

    # ----

    performance7_paymentPackage19 = Performance.objects.create(info='This price is whith the equipment',
                                                               hours=1.5, price=50)
    performance7_paymentPackage19.save()

    paymentPackage19_performance7 = PaymentPackage.objects.create(
        description='This price is whithout the equipment',
        portfolio=portfolio7,
        performance=performance7_paymentPackage19)
    paymentPackage19_performance7.save()

    fare7_paymentPackage20 = Fare.objects.create(priceHour=45)
    fare7_paymentPackage20.save()

    paymentPackage20_fare7 = PaymentPackage.objects.create(description='This price include my own performancer',
                                                           portfolio=portfolio7,
                                                           fare=fare7_paymentPackage20)
    paymentPackage20_fare7.save()

    custom7_paymentPackage21 = Custom.objects.create(minimumPrice=60)
    custom7_paymentPackage21.save()

    paymentPackage21_custom7 = PaymentPackage.objects.create(description='This price is whith the equipment',
                                                             portfolio=portfolio7,
                                                             custom=custom7_paymentPackage21)
    paymentPackage21_custom7.save()

    # ----

    performance8_paymentPackage22 = Performance.objects.create(info='I do all in my portolio video carrousel',
                                                               hours=1.5, price=50)
    performance8_paymentPackage22.save()

    paymentPackage22_performance8 = PaymentPackage.objects.create(
        description='This price is with equipment',
        portfolio=portfolio8,
        performance=performance8_paymentPackage22)
    paymentPackage22_performance8.save()

    fare8_paymentPackage23 = Fare.objects.create(priceHour=45)
    fare8_paymentPackage23.save()

    paymentPackage23_fare8 = PaymentPackage.objects.create(description='This price is whithout equipment',
                                                           portfolio=portfolio8,
                                                           fare=fare8_paymentPackage23)
    paymentPackage23_fare8.save()

    custom8_paymentPackage24 = Custom.objects.create(minimumPrice=60)
    custom8_paymentPackage24.save()

    paymentPackage24_custom8 = PaymentPackage.objects.create(description='This price is whithout equipment',
                                                             portfolio=portfolio8,
                                                             custom=custom8_paymentPackage24)
    paymentPackage24_custom8.save()

    # ----

    performance9_paymentPackage25 = Performance.objects.create(info='This performance dont need nothing',
                                                               hours=1.5, price=50)
    performance9_paymentPackage25.save()

    paymentPackage25_performance9 = PaymentPackage.objects.create(
        description='We have all we need for this performance',
        portfolio=portfolio9,
        performance=performance9_paymentPackage25)
    paymentPackage25_performance9.save()

    fare9_paymentPackage26 = Fare.objects.create(priceHour=45)
    fare9_paymentPackage26.save()

    paymentPackage26_fare9 = PaymentPackage.objects.create(description='This price is whithout equipment',
                                                           portfolio=portfolio9,
                                                           fare=fare9_paymentPackage26)
    paymentPackage26_fare9.save()

    custom9_paymentPackage27 = Custom.objects.create(minimumPrice=60)
    custom9_paymentPackage27.save()

    paymentPackage27_custom9 = PaymentPackage.objects.create(description='This price is whithout equipment',
                                                             portfolio=portfolio9,
                                                             custom=custom9_paymentPackage27)
    paymentPackage27_custom9.save()

    # Transactions
    transaction_offer1 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='4578eph3', amount="120")
    transaction_offer1.save()  # CONTRACT_MADE - OK

    transaction_offer2 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='ew0ayqav', amount='120')
    transaction_offer2.save()  # PAYMENT_MADE - OK

    transaction_offer3 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='8tyxeyhk', amount='120')
    transaction_offer3.save()  # PAYMENT_MADE - OK

    transaction_offer4 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='crt7p01k', amount='120')
    transaction_offer4.save()  # CANCELLED_ARTIST - OK

    transaction_offer5 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='50vckfr9', amount='120')
    transaction_offer5.save()  # PENDING - OK

    transaction_offer6 = Transaction.objects.create(paypalArtist='carlosdj.espectaculos@gmail.com',
                                                    braintree_id='fwzysehd', amount='115')
    transaction_offer6.save()  # CONTRACT_MADE - OK

    transaction_offer7 = Transaction.objects.create(braintree_id='28msg07g', amount='100')
    transaction_offer7.save()  # REJECTED - OK

    transaction_offer8 = Transaction.objects.create(braintree_id='fj58887s', amount='140')
    transaction_offer8.save()  # REJECTED - OK

    transaction_offer9 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='pkjqy7p1',
                                                    amount='140')
    transaction_offer9.save()  # CONTRACT_MADE - OK

    transaction_offer10 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='amwhkx1j',
                                                     amount='140')
    transaction_offer10.save()  # CANCELLED_ARTIST - OK

    transaction_offer11 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='r3ca6wjr',
                                                     amount='140')
    transaction_offer11.save()  # CONTRACT_MADE - OK

    transaction_offer12 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='gtfcqq8k',
                                                     amount='140')
    transaction_offer12.save()  # CANCELLED_ARTIST - OK

    transaction_offer13 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='ewzr056h',
                                                     amount='140')
    transaction_offer13.save()  # CANCELLED_CUSTOMER - OK

    transaction_offer14 = Transaction.objects.create(braintree_id='23dnh3xq', amount='115')
    transaction_offer14.save()  # PENDING - OK

    transaction_offer15 = Transaction.objects.create(braintree_id='8xqp595r', amount='80')
    transaction_offer15.save()  # PENDING - OK

    transaction_offer16 = Transaction.objects.create(braintree_id='9r2rt4pz', amount='160')
    transaction_offer16.save()  # PENDING - OK

    transaction_offer17 = Transaction.objects.create(braintree_id='670zzdqz', amount='800')
    transaction_offer17.save()  # PENDING - OK

    transaction_offer18 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='4nzgyn9a',
                                                     amount='1000')
    transaction_offer18.save()  # PAYMENT_MADE - OK

    transaction_offer19 = Transaction.objects.create(paypalArtist='fromthenois3@gmail.com', braintree_id='800rh4t1',
                                                     amount='1200')
    transaction_offer19.save()  # PAYMENT_MADE - OK

    # Rating
    rating_offer2 = Rating.objects.create(score=5, comment="Excellent")
    rating_offer3 = Rating.objects.create(score=4, comment="Very good, I will hire him another time")

    # Offers

    offer1_performance1 = Offer.objects.create(description='This offer interests you',
                                               status='CONTRACT_MADE',
                                               date='2019-04-29 12:00:00', hours=2.5, price='120', currency='EUR',
                                               appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer1,
                                               paymentCode=_service_generate_unique_payment_code())
    offer1_performance1.save()

    jsonfield = {"init": True,
                 "messages": [
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:47",
                             "mode": "MESSAGE",
                             "name": "Rafael",
                             "message": "hola",
                             "username": "customer1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:55",
                             "mode": "MESSAGE",
                             "name": "José Antonio",
                             "message": "hola, ha surgido algo?",
                             "username": "artist1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:56",
                             "mode": "MESSAGE",
                             "name": "Rafael",
                             "message": "Para comentarte que el aforo sera de 100 personas",
                             "username": "customer1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:56",
                             "mode": "MESSAGE",
                             "name": "José Antonio",
                             "message": "Ah, ok perfe",
                             "username": "artist1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:56",
                             "mode": "MESSAGE",
                             "name": "Rafael",
                             "message": "Algo adicional que quieras saber?",
                             "username": "customer1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:57",
                             "mode": "MESSAGE",
                             "name": "José Antonio",
                             "message": "No nada,gracias",
                             "username": "artist1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:57",
                             "mode": "MESSAGE",
                             "name": "Rafael",
                             "message": "Ok, adios",
                             "username": "customer1"
                         }
                     },
                     {
                         "json": {
                             "date": "2019-05-02",
                             "hour": "01:57",
                             "mode": "MESSAGE",
                             "name": "José Antonio",
                             "message": "Ok, adios",
                             "username": "artist1"
                         }
                     }
                 ]
                 }

    Chat.objects.create(offer=offer1_performance1, json=jsonfield)

    offer2_performance1 = Offer.objects.create(description='Can you make a performance for me?',
                                               status='PAYMENT_MADE',
                                               date='2019-07-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer2,
                                               rating=rating_offer2)
    offer2_performance1.save()

    offer3_performance1 = Offer.objects.create(description='A need a DJ in my bar',
                                               status='PAYMENT_MADE',
                                               date='2019-02-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer3,
                                               rating=rating_offer3)
    offer3_performance1.save()

    jsonfield2 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Muy buenas",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "hola, acabo de recibir la oferta",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Si, el aforo será de 100 personas aprox. ¿Sigues interesado?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Pues perfecto",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "¿Algo más que quieras saber?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "No nada, nos vemos en allí.",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Ok, adios",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "¡Bye!",
                              "username": "artist1"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer3_performance1, json=jsonfield2)

    offer4_performance1 = Offer.objects.create(description='Can you come this day?',
                                               status='CANCELLED_ARTIST',
                                               date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location2, transaction=transaction_offer4,
                                               reason='Due to personal problems, we must cancel the performance.')
    offer4_performance1.save()

    jsonfield3 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Jorge",
                              "message": "Hola, ¿por lo que veo estas interesado?",
                              "username": "customer2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "Sí, pero aún no conocemos la disponibilidad para ese día debido a unos " +
                                         "problemas de ultima hora",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Jorge",
                              "message": "Vale, el evento sería para 70 personas entre 20 y 30 años.",
                              "username": "customer2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "Pues perfecto",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Jorge",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "No nada, te lo confirmaré en los próximos días.",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Jorge",
                              "message": "Ok, adios",
                              "username": "customer2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "¡Hasta luego!",
                              "username": "artist1"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer4_performance1, json=jsonfield3)

    offer5_fare1 = Offer.objects.create(description='Rave party at my place', status='PENDING',
                                        date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                        appliedVAT=10, paymentPackage=paymentPackage2_fare1,
                                        eventLocation=event_location2, transaction=transaction_offer5)
    offer5_fare1.save()

    offer6_custom1 = Offer.objects.create(description='You cannot miss this opportunity', status='CONTRACT_MADE',
                                          date='2019-8-25 12:00:00', hours=1.5, price='115', currency='EUR',
                                          appliedVAT=10, paymentCode=_service_generate_unique_payment_code(),
                                          paymentPackage=paymentPackage3_custom1,
                                          eventLocation=event_location1, transaction=transaction_offer6)
    offer6_custom1.save()

    offer7_custom1 = Offer.objects.create(description='I need a DJ for my sisters weeding', status='REJECTED',
                                          date='2019-10-25 19:00:00', hours=1.5, price='100', currency='EUR',
                                          appliedVAT=10, paymentPackage=paymentPackage3_custom1,
                                          eventLocation=event_location1, transaction=transaction_offer7,
                                          reason='Your local has a bad reputation.')
    offer7_custom1.save()

    offer8_performance2 = Offer.objects.create(description='I want you to my event!',
                                               status='REJECTED',
                                               date='2019-10-25 15:00:00', hours=1.5, price='140', currency='EUR',
                                               appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                               eventLocation=event_location1, transaction=transaction_offer8,
                                               reason='I will be in another country.')
    offer8_performance2.save()

    jsonfield4 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Hola",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Buenas, te adelanto que no sabré si podremos ir ese dia.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Vale, el evento sería para 90 personas con todo el equipo preparado.",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Pues perfecto",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "No nada, te lo confirmaré en los próximos días.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Ok, adios",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "¡Hasta luego!",
                              "username": "artist2"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer8_performance2, json=jsonfield4)

    offer9_performance2 = Offer.objects.create(description='Come on!',
                                               status='CONTRACT_MADE',
                                               date='2019-10-25 15:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                               eventLocation=event_location1, transaction=transaction_offer9)
    offer9_performance2.save()

    jsonfield5 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Miguel",
                              "message": "Hola, gracias por aceptar la oferta.",
                              "username": "customer4"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Buenas, cuentame un poco las condiciones del evento.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Miguel",
                              "message": "Vale, el evento sería para bastantes personas y con varios artistas.",
                              "username": "customer4"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Pues perfecto",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Miguel",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer4"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "No nada, vamos hablando.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Miguel",
                              "message": "Ok, hasta luego",
                              "username": "customer4"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "¡Hasta luego!",
                              "username": "artist2"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer9_performance2, json=jsonfield5)

    offer10_fare2 = Offer.objects.create(description='Can you make me very happy?', status='CANCELLED_ARTIST',
                                         date='2019-03-27 00:00:00', hours=1.5, price='140', currency='EUR',
                                         paymentCode=_service_generate_unique_payment_code(),
                                         appliedVAT=10, paymentPackage=paymentPackage5_fare2,
                                         eventLocation=event_location4, transaction=transaction_offer10,
                                         reason='I will be in another country.')
    offer10_fare2.save()

    jsonfield6 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Hola, ¿cómo va todo?.",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Buenas, cuentame un poco las condiciones del evento.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Vale, el evento sería para 50 personas, ¿sigues interesado.",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Sí, gracias por la oportunidad.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "No nada, estamos en contacto.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Ok, hasta luego",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "¡Hasta luego!",
                              "username": "artist2"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer10_fare2, json=jsonfield6)

    offer11_fare2 = Offer.objects.create(description='Please, I need you for my birthday', status='CONTRACT_MADE',
                                         date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                         paymentCode=_service_generate_unique_payment_code(),
                                         appliedVAT=10, paymentPackage=paymentPackage5_fare2,
                                         eventLocation=event_location4, transaction=transaction_offer11)
    offer11_fare2.save()

    offer12_custom2 = Offer.objects.create(description='Wow, I want to see you again in my place',
                                           status='CANCELLED_ARTIST',
                                           date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                           paymentCode=_service_generate_unique_payment_code(),
                                           appliedVAT=10, paymentPackage=paymentPackage5_fare2,
                                           eventLocation=event_location3, transaction=transaction_offer12,
                                           reason='The singer is aphonic')
    offer12_custom2.save()

    jsonfield7 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Juan Manuel",
                              "message": "Hola, ¿qué tal?",
                              "username": "customer3"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "Buenas, te cuento un poco sobre el evento.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Juan Manuel",
                              "message": "Perfecto.",
                              "username": "customer3"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "El evento será dentro de la sala y para 50 personas. ¿Sigues intresado?",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Juan Manuel",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer3"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "No nada, estamos en contacto.",
                              "username": "artist2"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Juan Manuel",
                              "message": "Ok, hasta luego",
                              "username": "customer3"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "José Antonio",
                              "message": "¡Hasta luego!",
                              "username": "artist2"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer12_custom2, json=jsonfield7)

    offer13_custom2 = Offer.objects.create(description='Formal contract',
                                           status='CANCELLED_CUSTOMER',
                                           date='2017-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                           paymentCode=_service_generate_unique_payment_code(),
                                           appliedVAT=10, paymentPackage=paymentPackage5_fare2,
                                           eventLocation=event_location3, transaction=transaction_offer13,
                                           reason='The establishment will be refurbished.')
    offer13_custom2.save()

    offer14_performance2 = Offer.objects.create(description='Can you miss this opportunity?',
                                                status='PENDING',
                                                date='2019-07-07 15:00:00', hours=2.5, price='115', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer14)

    offer14_performance2.save()

    offer15_performance2 = Offer.objects.create(description='I want to hear us again!',
                                                status='PENDING',
                                                date='2019-07-11 15:00:00', hours=1.5, price='80', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location2, transaction=transaction_offer19)

    offer15_performance2.save()

    offer16_performance1 = Offer.objects.create(description='Come on!', status='PENDING',
                                                date='2019-07-11 15:00:00', hours=2.5, price='160', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                                eventLocation=event_location1, transaction=transaction_offer15)

    offer16_performance1.save()

    offer17_performance1 = Offer.objects.create(description='I want a great party to my friend', status='PENDING',
                                                date='2019-07-14 08:00:00', hours=1.5, price='800', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage1_performance1,
                                                eventLocation=event_location2, transaction=transaction_offer16)

    offer17_performance1.save()

    offer18_performance1 = Offer.objects.create(description='Can you interested to my offer?',
                                                status='PAYMENT_MADE',
                                                date='2019-03-14 08:00:00', hours=3, price='1000', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer17,
                                                paymentCode=_service_generate_unique_payment_code())

    offer18_performance1.save()

    jsonfield8 = {"init": True,
                  "messages": [
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:47",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Hola, ¿qué tal?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:55",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "Buenas, te cuento un poco sobre el evento.",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Perfecto.",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "El evento será dentro de la sala y para 50 personas. ¿Sigues intresado?",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:56",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "¿Algo más que necesites saber?",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "No nada, estamos en contacto.",
                              "username": "artist1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Rafael",
                              "message": "Ok, hasta luego",
                              "username": "customer1"
                          }
                      },
                      {
                          "json": {
                              "date": "2019-05-02",
                              "hour": "01:57",
                              "mode": "MESSAGE",
                              "name": "Carlos",
                              "message": "¡Hasta luego!",
                              "username": "artist1"
                          }
                      }
                  ]
                  }

    Chat.objects.create(offer=offer18_performance1, json=jsonfield8)

    offer19_performance1 = Offer.objects.create(description='The best opportunity for your group',
                                                status='PAYMENT_MADE',
                                                date='2019-03-14 12:00:00', hours=3.1, price='1200', currency='EUR',
                                                appliedVAT=10, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer18,
                                                paymentCode=_service_generate_unique_payment_code())

    offer19_performance1.save()

    # Data for teachers

    # Portfolio from teachers

    portfolio14_prof = Portfolio.objects.create(artisticName='The great magician')
    portfolio14_prof.save()

    calendar14 = Calendar.objects.create(days=[], portfolio=portfolio14_prof)
    calendar14.save()

    portfolio15_prof = Portfolio.objects.create(artisticName='The pianist')
    portfolio15_prof.save()

    calendar15 = Calendar.objects.create(days=[], portfolio=portfolio15_prof)
    calendar15.save()

    # ...user artist from teachers

    email_to_send_mail_teachers = 'ispp.profesores@gmail.com'

    user15_artist10_prof = User.objects.create(username='PabloArtist',
                                               password=make_password('PabloArtistPabloArtist'),
                                               first_name='Pablo', last_name='Trinidad Fernandez',
                                               email=email_to_send_mail_teachers)
    user15_artist10_prof.save()

    user16_artist11_prof = User.objects.create(username='CarlosArtist',
                                               password=make_password('CarlosArtistCarlosArtist'),
                                               first_name='Carlos', last_name='Müller',
                                               email=email_to_send_mail_teachers)
    user16_artist11_prof.save()

    # ...user customer from teachers

    user17_customer5_prof = User.objects.create(username='PabloCustomer',
                                                password=make_password('PabloCustomer'),
                                                first_name='Pablo', last_name='Trinidad Fernandez',
                                                email=email_to_send_mail_teachers)
    user17_customer5_prof.save()

    user18_customer6_prof = User.objects.create(username='CarlosCustomer',
                                                password=make_password('CarlosCustomer'),
                                                first_name='Carlos', last_name='Müller',
                                                email=email_to_send_mail_teachers)
    user18_customer6_prof.save()

    # ...artists from teachers

    artist10_prof = Artist.objects.create(user=user15_artist10_prof, rating=0, portfolio=portfolio14_prof,
                                          photo='https://raw.githubusercontent.com/Iriabow/pepe/master/magician-circus-ladies-b75b24-1024.jpg')
    artist10_prof.save()

    artist11_prof = Artist.objects.create(user=user16_artist11_prof, rating=0, portfolio=portfolio15_prof,
                                          photo='https://raw.githubusercontent.com/Iriabow/pepe/master/pianista.jpg')
    artist11_prof.save()

    # ...customer from teachers

    artist15_prof = Customer.objects.create(user=user17_customer5_prof)
    artist15_prof.save()

    artist16_prof = Customer.objects.create(user=user18_customer6_prof)
    artist16_prof.save()


os.system('python3 manage.py sqlflush | python3 manage.py dbshell')
save_data()
# index_all()
