#!/bin/bash

if [[ ! "${SAUCE_USERNAME}" || ! "${SAUCE_ACCESS_KEY}" ]]; then
  echo "This script runs only when Sauce credentials are present"
  echo "Please set SAUCE_USERNAME and SAUCE_ACCESS_KEY env variables"
  echo "export SAUCE_USERNAME=ur-username"
  echo "export SAUCE_ACCESS_KEY=ur-access-key"
  return 0
fi

local sc_tmp sc_platform sc_archive sc_distro_fmt \
  sc_readyfile sc_logfile sc_tunnel_id_arg sc_bin

sc_tmp="$(mktemp -d -t sc.XXXX)"
echo "Using temp dir ${sc_tmp}"
pushd "${sc_tmp}" || true


sc_archive=sc-linux.tar.gz

sc_readyfile="sauce-connect-ready-${RANDOM}"
sc_logfile="${TRAVIS_HOME}/sauce-connect.log"
if [ ! -z "${TRAVIS_JOB_NUMBER}" ]; then
  sc_tunnel_id_arg="-i ${TRAVIS_JOB_NUMBER}"
fi

sc_download_url="https://saucelabs.com/downloads/sc-4.5.4-linux.tar.gz"
wget "${sc_download_url}" -O "${sc_archive}"
echo 'Extracting Sauce Connect'
tar zxf sc-linux.tar.gz


sc_bin="$(find sc-* -type f -perm -0500 -name sc)"

# shellcheck disable=SC2086
"${sc_bin}" \
  ${sc_tunnel_id_arg} \
  -f ${sc_readyfile} \
  -l ${sc_logfile} \
  -x "https://eu-central-1.saucelabs.com/rest/v1" \
  ${SAUCE_NO_SSL_BUMP_DOMAINS} \
  ${SAUCE_DIRECT_DOMAINS} \
  ${SAUCE_TUNNEL_DOMAINS} &
export TRAVIS_SAUCE_CONNECT_PID="${!}" &

echo "Waiting for Sauce Connect readyfile"
while test ! -f "${sc_readyfile}" && ps -f "${TRAVIS_SAUCE_CONNECT_PID}" &>/dev/null; do
  sleep .5
done

if test ! -f "${sc_readyfile}"; then
  echo "readyfile not created"
fi

test -f "${sc_readyfile}"
_result="${?}"

popd || true
