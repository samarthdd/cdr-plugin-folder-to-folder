#!/usr/bin/env sh
set -e

SUBNET_PREFIX="192.168.1"
NETMASK="255.255.255.0"
DOMAIN_NAME="dhcp.glasswall"
DHCP_CONFIG="${1:-dhcpd.conf}"
TERRAFORM_CONFIG="${2:-dhcp.tf}"

generate_config() {
  cat <<EOF >"$DHCP_CONFIG"
subnet ${SUBNET_PREFIX}.0 netmask ${NETMASK} {
  option domain-name "${DOMAIN_NAME}";
  option domain-name-servers ${SUBNET_PREFIX}.1;
  option routers ${SUBNET_PREFIX}.1;
}
EOF
  cat <<EOF >"$TERRAFORM_CONFIG"
locals {
  dhcp_address_mac = {
EOF
  USED_MACS="$(mktemp)"
  for i in {2..254}; do
    while true; do
      MAC="$(openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/:$//')"
      if grep -qF "$MAC" "$USED_MACS"; then
        continue
      fi
      printf "info: %s.%s\n" "$SUBNET_PREFIX" "$i"
      cat <<EOF >>"$DHCP_CONFIG"
host dhcp-client {
  hardware ethernet ${MAC};
  fixed-address ${SUBNET_PREFIX}.$i;
}
EOF
      cat <<EOF >>"$TERRAFORM_CONFIG"
    "${SUBNET_PREFIX}.$i" = "${MAC}"
EOF
      break
    done
  done
  printf "  }\n}\n" >>"$TERRAFORM_CONFIG"
  rm -f "$USED_MACS"
}

dirname "$CONFIG" | xargs mkdir -p
generate_config