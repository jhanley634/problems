#! /usr/bin/env bash
# Copyright 2024 John Hanley. MIT licensed.

# make audit | xargs -n1 infra/prepend_notice.sh

FILE=${1:-unknown}
set -e
test -r "${FILE}"
grep Copyright "${FILE}" > /dev/null && exit
set -x
grep 'env python' "${FILE}" > /dev/null && sed -i~ -e '2 i\
# Copyright 2024 John Hanley. MIT licensed.'  "${FILE}" && pwd && exit
sed -i~ -e '1 i\
# Copyright 2024 John Hanley. MIT licensed.'  "${FILE}"
