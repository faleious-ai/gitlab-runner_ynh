#!/usr/bin/env bash

printf '%s\n' "$*" > "${ARGV_LOG:?}"
printf 'CI_SERVER_URL=%s\nCI_SERVER_TOKEN=%s\nREGISTER_NON_INTERACTIVE=%s\n' "${CI_SERVER_URL:-}" "${CI_SERVER_TOKEN:-}" "${REGISTER_NON_INTERACTIVE:-}" > "${ENV_LOG:?}"
printf 'runner failed token=%s\n' "${CI_SERVER_TOKEN:-}" >&2
exit 1
