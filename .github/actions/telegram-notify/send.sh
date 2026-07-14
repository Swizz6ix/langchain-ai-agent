#!/usr/bin/env bash

set -Eeuo pipefail


# Status Icon
case "${INPUT_STATUS}" in

success)
ICON="✅"
;;

failure)
ICON="❌"
;;

cancelled)
ICON="⚪"
;;

*)
ICON="ℹ️"
;;

esac


# Timestamp
TIME=$(date -u +"%Y-%m-%d %H:%M:%S UTC")


# Short SHA
SHORT_SHA="${INPUT_SHA:0:7}"


# Workflow URL
RUN_URL="https://github.com/${INPUT_REPOSITORY}/actions/runs/${INPUT_RUN_ID}"


# Message
TEXT=$(cat <<EOF
$ICON *${INPUT_TITLE}*

*Environment:* ${INPUT_ENVIRONMENT}
*Status:* ${INPUT_STATUS}

*Repository:* ${INPUT_REPOSITORY}
*Workflow:* ${INPUT_WORKFLOW}

*Branch:* ${INPUT_BRANCH}

*Commit:* ${SHORT_SHA}

*Actor:* ${INPUT_ACTOR}

*Run:* #${INPUT_RUN_NUMBER}

*Time:* ${TIME}

${INPUT_MESSAGE}

${RUN_URL}
EOF
)


# Send
curl \
    --silent \
    --show-error \
    --fail \
    --retry 3 \
    --retry-delay 5 \
    --retry-all-errors \
    -X POST \
    "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${TEXT}" \
    --data-urlencode "parse_mode=Markdown"
