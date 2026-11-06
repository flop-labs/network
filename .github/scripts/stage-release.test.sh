#!/usr/bin/env bash
# Tests stage-release.sh against a fake gh. Run: .github/scripts/stage-release.test.sh
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/.github/scripts" "$tmp/bin"
cp "$here/stage-release.sh" "$tmp/.github/scripts/"
echo 'rest-gateway flop-labs/source' >"$tmp/.github/release-sources.txt"

cat >"$tmp/bin/gh" <<'EOF'
#!/usr/bin/env bash
echo "$*" >>"$CALLS"
case "$*" in
  *--paginate*) printf '%s' "$FAKE_RELEASE" ;;
  *"-X PUT"*) cat >>"$CALLS"; echo commit123 ;;
  *"-X POST"* | *"-X PATCH"*) cat >>"$CALLS" ;;
  *contents*) [[ -n ${FAKE_FILE_SHA:-} ]] && echo "$FAKE_FILE_SHA" || exit 1 ;;
esac
EOF
chmod +x "$tmp/bin/gh"

failures=0
run() {
  : >"$tmp/calls"
  PATH="$tmp/bin:$PATH" CALLS="$tmp/calls" SOURCE_REPO="${SOURCE_REPO:-flop-labs/source}" \
    TARGET_REPO=flop-labs/network SERVICE="${SERVICE:-rest-gateway}" VERSION="${VERSION:-v1.4.0}" \
    NOTES="${NOTES:-Fixed model listing.}" FAKE_RELEASE="${FAKE_RELEASE:-}" \
    FAKE_FILE_SHA="${FAKE_FILE_SHA:-}" "$tmp/.github/scripts/stage-release.sh" >/dev/null 2>&1
}
pass() { # name, then a command that must succeed
  local name=$1
  shift
  if "$@"; then echo "ok   $name"; else echo "FAIL $name"; failures=$((failures + 1)); fi
}
refused() { ! run && ! grep -qE -- '-X (PUT|POST|PATCH)' "$tmp/calls"; }
wrote() { grep -qE -- "$1" "$tmp/calls"; }

first_run() { run && wrote '-X POST' && wrote '"draft": ?true' && wrote 'commit123' && ! wrote '"sha"'; }
pass 'first run creates a draft on its own commit' first_run

rerun() { FAKE_RELEASE=$'77\ttrue' FAKE_FILE_SHA=abc run && wrote 'releases/77' && wrote '"sha": ?"abc"' && ! wrote '-X POST'; }
pass 'rerun updates the existing draft' rerun

FAKE_RELEASE=$'77\tfalse' pass 'published release is refused' refused
SOURCE_REPO=flop-labs/other pass 'unlisted source is refused' refused
SERVICE=other-service pass 'unlisted service is refused' refused
VERSION=1.4.0 pass 'version without v is refused' refused
NOTES='   ' pass 'blank notes are refused' refused
NOTES='see flop-labs/flop-core#12' pass 'private repo link is refused' refused
NOTES='edge at rpc.ts.flop.network' pass 'internal host is refused' refused
NOTES='node at 10.1.2.3 restarted' pass 'IP address is refused' refused

exit "$failures"
