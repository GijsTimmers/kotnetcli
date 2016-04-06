#!/bin/sh

rm kotnetcli_server.pem
openssl req -new -x509 -keyout kotnetcli_server.pem -out kotnetcli_server.pem -days 365 -nodes
