;<----FUNCIONES---->
(deffunction Horas (?distancia ?velocidad_cruc)
    (return (div ?distancia ?velocidad_cruc))
);;Horas

(deffunction Min (?horas)
    (return (mod ?horas 60))
);;Min

;<----PLANTILLAS---->
(deftemplate aeronave
    (slot id_aero)
    (slot compania)
    (slot aeorigen)
    (slot aedestino)
    (slot velocidad)
    (slot accion (allowed-values Ninguna Despegue Aterrizaje Emergencia Rumbo))
    (slot estado(allowed-values enTierra Ascenso Crucero Descenso) (default enTierra))
);;aeronave

(deftemplate aerodromo
    (slot id_aerodromo)
    (slot ciudad)
    (slot radar (allowed-values ON OFF))
    (slot visibilidad)
    (slot viento)
);;aerodromo

(deftemplate piloto
    (slot id_aeronave)
    (slot confirmacion (allowed-values OK SOS Ejecutando Stand_by) (default Stand_by))
);;piloto

(deftemplate vuelo
    (slot id_origen)
    (slot id_destino)
    (slot distancia)
    (slot velocidad_desp (default 240))
    (slot velocidad_cruc (default 700))
);;vuelo

;<----HECHOS---->
(deffacts H1
    (aeronave (id_aero FX001) (compania Iberia) (aeorigen XRY) (aedestino ZXY) (accion Despegue))
    (aerodromo (id_aerodromo XRY) (ciudad Jerez) (radar ON) (visibilidad 20) (viento 2))
    (aerodromo (id_aerodromo ZXY)(ciudad Madrid) (radar ON) (visibilidad 15) (viento 15))
    (piloto (id_aeronave FX001) (confirmacion OK))
    (vuelo (id_origen XRY) (id_destino ZXY) (distancia 800))
);;H1

;<----REGLAS---->
(defrule Despegar
    ?nave <- (aeronave (id_aero ?aeronave) (aeorigen ?origen) (aedestino ?destino) (velocidad ?vel) (accion Despegue) (estado enTierra))
    ?p <- (piloto (id_aeronave ?aeronave) (confirmacion OK))
    (aerodromo (id_aerodromo ?origen) (radar ON) (visibilidad ?vis) (viento ?viento))
    (vuelo (id_origen ?origen) (id_destino ?destino) (velocidad_desp ?desp))
    (test (!= ?origen ?destino))
    (test (> ?vis 5))
    (test (< ?viento 75))
    =>
    (modify ?p (confirmacion Ejecutando))
    (modify ?nave (velocidad ?desp) (accion Ninguna)  (estado Ascenso))
);;Despegar

(defrule Excepcion
    (piloto (id_aeronave ?aeronave) (confirmacion ~OK))
    ?nave <- (aeronave (id_aero ?aeronave) (compania ?compania) (aeorigen ?origen) (aedestino ?destino) (accion Despegue))
    (aerodromo (id_aerodromo ?origen))
    (aerodromo (id_aerodromo ?destino))
    (vuelo (id_origen ?origen) (id_destino ?destino))
    (test (!= ?origen ?destino))
    =>
    (modify ?nave (accion Emergencia))
    (println "ATENCION El piloto de la aeronvae " ?aeronave " de la compania " ?compania " no se ecuentra disponible para iniciar el despegue desde el aerodromo " ?origen " con destino" ?destino)
);;Excepcion

(defrule Crucero
    ?nave <- (aeronave (estado Ascenso) (aeorigen ?origen) (aedestino ?destino) (velocidad ?velocidad))
    (vuelo (id_origen ?origen) (id_destino ?destino) (distancia ?distancia) (velocidad_cruc ?crucero))
    ?p <- (piloto (confirmacion Ejecutando))
    (test (!= ?velocidad ?crucero))
    (test (!= ?origen ?destino))
    =>
    (modify ?nave (estado Crucero) (velocidad ?crucero))
    (modify ?p (confirmacion Stand_by))
    (bind ?horas (Horas ?distancia ?crucero))
    (bind ?min (Min ?horas))
    (println "El despegue ha sido correcto.  El vuelo tardará " ?horas " horas y " ?min " minutos.")
);;Crucero