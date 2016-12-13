#!/bin/bash
## kotnetcli is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## kotnetcli is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with kotnetcli.  If not, see <http://www.gnu.org/licenses/>.
##
## see http://stackoverflow.com/a/10176685

COUNTRY="BE"
STATE="Belgium"
CITY="Leuven"
COMPANY="kotnetcli"
UNIT="dev"
CN="localhost"

SUBJ="/C=$COUNTRY/ST=$STATE/L=$CITY/O=$COMPANY/OU=$UNIT/CN=$CN"
CERT="kotnetcli-localhost.pem"
OPENSSL_CMD="openssl req -x509 -newkey rsa:2048 -keyout $CERT -out $CERT -days 365 -nodes -subj $SUBJ"

rm $CERT
echo -e "===== generating self-signed openSSL certificate: $OPENSSL_CMD =====\n"
$OPENSSL_CMD

OPENSSL_VERIFY_CMD="openssl verify $CERT"
echo -e "\n===== verifying generated certificate: $OPENSSL_VERIFY_CMD =====\n"
$OPENSSL_VERIFY_CMD
