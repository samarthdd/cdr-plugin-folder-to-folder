#cloud-config

runcmd:
    - echo "Updating the instance IP to ${ip_address}"
    - nmcli connection add ifname ens160 con-name offline type ethernet ipv4.addresses ${ip_address}/27 ipv4.gateway ${gateway_ip} ipv4.dns 8.8.8.8 ipv4.method manual
    - nmcli connection up offline
    - nmcli connection show
    