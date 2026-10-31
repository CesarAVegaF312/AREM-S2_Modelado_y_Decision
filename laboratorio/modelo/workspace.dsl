/*
 * Red Salud Andina: la costura AGENDA-WEB -> HIS-CORE, en C4.
 *
 * Fuente: dossier del caso, secciones 7 (integraciones) y 8 (infraestructura).
 * Se abre con: docker compose --profile modelo up -d structurizr
 *              y luego http://localhost:8200
 *
 * Las dos vistas de contenedores muestran las dos alternativas que se miden en
 * el laboratorio. Cambiar el modelo aqui cambia los diagramas: no se dibujan a
 * mano.
 */
workspace "Red Salud Andina · Costura de agendamiento" "Laboratorio de la Unidad 2 de AREM" {

    !identifiers hierarchical

    model {
        paciente = person "Paciente" "Agenda citas por el portal web o por el call center."
        agente = person "Agente del call center" "Agenda en nombre del paciente."

        group "Red Salud Andina" {
            agenda = softwareSystem "AGENDA-WEB" "Portal de agendamiento. Servicio en la nube de un proveedor." {
                portal = container "Portal de agendamiento" "Recibe la solicitud de cita del paciente." "Servicio web"
                cola = container "Cola de citas" "Guarda las citas hasta que HIS-CORE las registra." "RabbitMQ" "Cola"
                adaptador = container "Adaptador de HIS-CORE" "Consume la cola, registra en HIS-CORE y reintenta si no está disponible." "Servicio"
            }
            hisCore = softwareSystem "HIS-CORE" "Historia clínica y admisión en 18 sedes y la clínica. Ventana de mantenimiento dominical de 2 h." "Existente"
            hisNorte = softwareSystem "HIS-NORTE" "HIS de las 6 sedes adquiridas a Centro Médico del Norte." "Existente"
            lis = softwareSystem "LIS-LAB" "Órdenes y resultados de laboratorio." "Existente"
            fact = softwareSystem "FACT-SALUD" "Facturación y radicación ante aseguradores." "Existente"
        }

        paciente -> agenda.portal "Solicita cita" "HTTPS"
        agente -> agenda.portal "Agenda en nombre del paciente" "HTTPS"

        // Alternativa sincrona: la costura que existe hoy.
        agenda.portal -> hisCore "Registra la cita y espera la confirmación" "HTTP síncrono" "Sincrona"

        // Alternativa asincrona: cola y adaptador.
        agenda.portal -> agenda.cola "Publica la cita" "AMQP" "Asincrona"
        agenda.adaptador -> agenda.cola "Consume citas" "AMQP" "Asincrona"
        agenda.adaptador -> hisCore "Registra la cita; reintenta si no responde" "HTTP" "Asincrona"

        // Contexto: otras integraciones del inventario (seccion 7 del dossier).
        hisCore -> fact "Lectura directa de tablas, sin contrato de interfaz"
        hisCore -> lis "Archivos planos por carpeta compartida, cada 15 min"
        hisNorte -> fact "Carga manual asistida, diaria"
    }

    views {
        systemContext agenda "Contexto" "AGENDA-WEB y los sistemas asistenciales con los que se integra." {
            include *
            include hisNorte lis fact
            autolayout lr
        }

        container agenda "AlternativaSincrona" "Hoy: el portal espera a HIS-CORE. Si HIS-CORE está lento o caído, el paciente lo siente." {
            include paciente agente agenda.portal hisCore
            exclude "relationship.tag==Asincrona"
            autolayout lr
        }

        container agenda "AlternativaAsincrona" "Cola y adaptador: el portal responde de inmediato y HIS-CORE se pone al día después." {
            include paciente agente agenda.portal agenda.cola agenda.adaptador hisCore
            exclude "relationship.tag==Sincrona"
            autolayout lr
        }

        styles {
            element "Element" {
                background #1565C0
                color #ffffff
                shape RoundedBox
            }
            element "Person" {
                background #002060
                shape Person
            }
            element "Existente" {
                background #64748B
            }
            element "Cola" {
                shape Pipe
            }
            relationship "Sincrona" {
                color #B0392B
            }
            relationship "Asincrona" {
                color #1D4ED8
                style dashed
            }
        }
    }
}
