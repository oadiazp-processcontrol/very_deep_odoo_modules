# Copyright 2020 Raul Carbonell - raul.carbonell@processcontrol.es
# License AGPL-3.0 or later
{
    "name": "PC EDI",
    "summary": "Implementación configurable de EDI",
    "version": "16.0.1.0.0",
    "category": "EDI",
    "website": "",
    "author": "Omar Díaz, Process Control",
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "pc_edi",
        "account",
    ],
    "data": [
        "views/account_move.xml",
    ]
}
