#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import time

import pythoncom
import win32com.client


class OmniRigEvents:
    """
    Manejador de eventos de OmniRig.

    OJO:
    Los nombres de estos métodos tienen que coincidir EXACTAMENTE con los nombres
    de los eventos que expone el wrapper de pywin32 (makepy).
    Si en tu wrapper aparecen sin el sufijo 'Event' (VisibleChange, StatusChange, etc.)
    simplemente renombra los métodos a esos nombres.
    """

    # Se llamará cuando cambie la visibilidad de la ventana de OmniRig
    def VisibleChangeEvent(self, RigNumber):
        print(f"[EVENT] VisibleChangeEvent: rig={RigNumber}", flush=True)

    # Se llamará cuando cambie el tipo de rig
    def RigTypeChangeEvent(self, RigNumber):
        print(f"[EVENT] RigTypeChangeEvent: rig={RigNumber}", flush=True)

    # Se llamará cuando cambie el estado del rig (online, offline, error, etc.)
    def StatusChangeEvent(self, RigNumber):
        try:
            rig = self.Rig1 if RigNumber == 1 else self.Rig2
            # Get_StatusStr es una propiedad del RigX
            status = rig.Get_StatusStr
            print(f"[EVENT] StatusChangeEvent: rig={RigNumber}, status='{status}'",
                  flush=True)
        except Exception as e:
            print(f"[EVENT] StatusChangeEvent: rig={RigNumber}, error leyendo estado: {e}",
                  flush=True)

    # Se llamará cuando cambien parámetros (frecuencia, modo, etc.)
    def ParamsChangeEvent(self, RigNumber):
        try:
            rig = self.Rig1 if RigNumber == 1 else self.Rig2
            freq = rig.Freq
            mode = rig.Mode
            print(f"[EVENT] ParamsChangeEvent: rig={RigNumber}, freq={freq}, mode={mode}",
                  flush=True)
        except Exception as e:
            print(f"[EVENT] ParamsChangeEvent: rig={RigNumber}, error leyendo params: {e}",
                  flush=True)


def send_command_and_read(rig, command: str, length: int) -> None:
    """
    Envía un comando CAT al rig y, opcionalmente, intenta leer una respuesta
    de 'length' caracteres (si length > 0).

    Ajusta esto según cómo estés usando OmniRig (SendCustomCommand, etc.).
    """
    print(f"[INFO] Enviando comando al rig: {command!r}", flush=True)
    try:
        # Ejemplo con SendCustomCommand; cámbialo si usabas otro método.
        # Devuelve una cadena con la respuesta del rig.
        response = rig.SendCustomCommand(command) if command else ""
        if length > 0:
            response = response[:length]
        print(f"[INFO] Respuesta (truncada a {length}): {response!r}", flush=True)
    except Exception as e:
        print(f"[ERROR] Falló el envío/lectura de comando: {e}", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Cliente de OmniRig vía COM (pywin32) con manejo de eventos."
    )
    parser.add_argument(
        "-c", "--command",
        help="Comando CAT a enviar al rig (string literal).",
        default=""
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=0,
        help="Longitud de respuesta a considerar (0 = no truncar / ignorar)."
    )
    parser.add_argument(
        "-r", "--rig",
        type=int,
        choices=[1, 2],
        default=1,
        help="Número de rig a usar (1 o 2)."
    )
    parser.add_argument(
        "-t", "--time",
        type=int,
        default=0,
        help="Tiempo en segundos para escuchar eventos (0 = infinito hasta Ctrl+C)."
    )

    args = parser.parse_args()

    # Inicialización de COM
    pythoncom.CoInitialize()

    try:
        # Creamos el objeto con soporte de eventos
        omni = win32com.client.DispatchWithEvents("OmniRig.OmniRig", OmniRigEvents)
        print("[INFO] OmniRig COM conectado.", flush=True)

        # Seleccionar rig
        rig = omni.Rig1 if args.rig == 1 else omni.Rig2

        # Mostrar estado inicial
        try:
            status = rig.Get_StatusStr
            freq = rig.Freq
            mode = rig.Mode
            print(f"[INFO] Estado inicial rig {args.rig}: status='{status}', "
                  f"freq={freq}, mode={mode}", flush=True)
        except Exception as e:
            print(f"[WARN] No se pudo leer estado inicial del rig {args.rig}: {e}",
                  flush=True)

        # Si se pasó un comando, lo enviamos
        if args.command:
            send_command_and_read(rig, args.command, args.length)

        # Bucle para procesar eventos
        if args.time == 0:
            print("[INFO] Escuchando eventos de OmniRig (Ctrl+C para salir)...",
                  flush=True)
            while True:
                # Procesa eventos COM pendientes
                pythoncom.PumpWaitingMessages()
                time.sleep(0.05)
        else:
            print(f"[INFO] Escuchando eventos de OmniRig durante {args.time} s...",
                  flush=True)
            end_time = time.time() + args.time
            while time.time() < end_time:
                pythoncom.PumpWaitingMessages()
                time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[INFO] Interrumpido por el usuario (Ctrl+C).", flush=True)
    except Exception as e:
        print(f"[ERROR] Error general en pycat.py: {e}", flush=True)
    finally:
        pythoncom.CoUninitialize()


if __name__ == "__main__":

