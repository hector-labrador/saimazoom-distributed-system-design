#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
launch_delivery.py
------------------
Lanza un Repartidor que escucha la cola saimazoom_repartidor_queue.
"""


from saimazoom_lib.repartidor import Repartidor


def main():
    rep = Repartidor(repartidor_id=2, max_intentos=3, prob_exito=0.7, config_file="config/server.conf")
    rep.start()
    rep.start_consuming()
    rep.stop()

if __name__ == "__main__":
    main()