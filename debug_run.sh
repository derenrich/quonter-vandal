#!/bin/bash

poetry run gunicorn quonter_vandal.proxy_server:app