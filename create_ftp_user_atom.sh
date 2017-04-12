#!/bin/bash
docker exec -ti elsecloudservice_ftp_1 pure-pw useradd atom -u ftpuser -d /home/ftpusers/atom
docker exec -ti elsecloudservice_ftp_1 pure-pw mkdb
