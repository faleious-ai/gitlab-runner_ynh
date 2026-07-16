#!/usr/bin/env bash

# Shared registration implementation for install, restore and the YunoHost
# action. It validates every item before invoking the Runner, so a malformed
# list cannot partially register a set of runners.

set -Eeuo pipefail

_register_redact() {
    local output=${1-}
    local secret=${2-}
    if [[ -n "$secret" ]]; then
        output=${output//"$secret"/[REDACTED]}
    fi
    printf '%s' "$output" | sed -E 's/((token|password|authorization|private[-_ ]token)[=: ]+)[^[:space:]]+/\1[REDACTED]/Ig'
}

_register_validate_value() {
    local value=$1
    local label=$2
    if [[ -z "$value" || "$value" == *$'\n'* || "$value" == *$'\r'* || "$value" == *$'\t'* ]]; then
        printf 'registration %s is empty or contains control characters\n' "$label" >&2
        return 1
    fi
}

_register_split_csv() {
    local input=$1
    local label=$2
    local -n destination=$3
    if [[ -z "$input" || "$input" == *, ]]; then
        printf 'registration %s list is empty or has a trailing comma\n' "$label" >&2
        return 1
    fi
    IFS=',' read -r -a destination <<< "$input"
    if ((${#destination[@]} == 0)); then
        printf 'registration %s list is empty\n' "$label" >&2
        return 1
    fi
    local item
    for item in "${destination[@]}"; do
        _register_validate_value "$item" "$label" || return 1
    done
}

register_runner_set() {
    local url_list=${1-}
    local token_list=${2-}
    local image_list=${3-}
    local runner_bin=${4:-gitlab-runner}
    local -a urls tokens images

    _register_split_csv "$url_list" "URL" urls
    _register_split_csv "$token_list" "token" tokens
    _register_split_csv "$image_list" "Docker image" images

    if [[ ! "$runner_bin" =~ ^[A-Za-z0-9_./-]+$ ]]; then
        printf 'registration runner binary path is invalid\n' >&2
        return 1
    fi
    if ((${#urls[@]} != ${#tokens[@]} || ${#urls[@]} != ${#images[@]})); then
        printf 'registration lists must have equal cardinality\n' >&2
        return 1
    fi

    local index url token image output
    for index in "${!urls[@]}"; do
        url=${urls[$index]}
        image=${images[$index]}
        if [[ ! "$url" =~ ^https?://[^[:space:]]+$ ]]; then
            printf 'registration URL is invalid\n' >&2
            return 1
        fi
        if [[ "$image" == *,* ]]; then
            printf 'registration Docker image is invalid\n' >&2
            return 1
        fi
    done

    for index in "${!urls[@]}"; do
        url=${urls[$index]}
        token=${tokens[$index]}
        image=${images[$index]}

        # The current gitlab-runner CLI accepts the token only as the --token
        # value. Keep tracing disabled, capture output, and redact before any
        # diagnostic is emitted. No token is written by this helper.
        if output=$("$runner_bin" register \
            --non-interactive \
            --url "$url" \
            --token "$token" \
            --executor docker \
            --docker-image "$image" 2>&1); then
            printf 'runner registration succeeded for %s\n' "$url"
        else
            printf 'runner registration failed for %s: %s\n' "$url" "$(_register_redact "$output" "$token")" >&2
            return 1
        fi
    done
}
