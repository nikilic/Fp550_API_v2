===========================================
Connexion / SQLAlchemy Fp550 REST Service
===========================================

This is a variant of the `Connexion Example "pet shop" REST Service`_ that stores data using the `SQLAlchemy`_ ORM.

.. _Connexion Example "pet shop" REST Service: https://github.com/hjacobs/connexion-example
.. _SQLAlchemy: http://www.sqlalchemy.org/

DV: Izmenjen simulator:
    1. U commands.recv() dodat
     `port_buff= b"\x01abcdata1\x31\xc1\xc0\x80dddata2\x04STATUS\x05bcc\x03"`
     kao konstanta umesto serial.port.read()
    2. Izmenjene if i elif da rade sa integer jer je port_buff type bytes, tj svaki byte je integer.  
    3. Dodat ispravan print u ascii i hex celog line[].  
    4. Return output vraca LEN,SEQ,CMD, STATUS, recv_pack_data   
    5. Uradjen i testiran "operationId: app.g11_cmd" koji prenosi recv - return output na REST API  
    6. Testiranje sa http://0.0.0.0:8090/ui/#!/G1_Commands/app_g11_cmd  
        {
  "Cmd": 99,
  "LEN": 97,
  "SEQ": 98,
  "Status": [    83,   84,    65,    84,    85,    83  ],
  "recv_pck_Data": [    100,    97,    116,    97,    49,    49,    193,    192,    128,    100,    100,    100,
    97,
    116,
    97,
    50,
    4  ]
}
