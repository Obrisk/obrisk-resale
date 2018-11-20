#!/bin/sh

set -o errexit
set -o pipefail
set -o nounset


celery -A obrisk.taskapp beat -l INFO
