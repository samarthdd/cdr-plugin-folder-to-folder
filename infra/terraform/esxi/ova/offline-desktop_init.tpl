#cloud-config

write_files:
    - path: /root/configure_ip.sh
      content: |
        #!/bin/bash
        fullip=$${1}
        gw=$${2}
        dns=$${3}
        [ -z $fullip  ] && return
        [ -z $gw  ] && return
        [ -z $dns ] && return
        if [ "$(ls /etc/netplan/*.yaml /etc/netplan/*.yml 2>/dev/null |  tail -n1 | wc -l)" != 0 ] ; then
        [ -d /etc/netplan.backup ] || sudo mkdir -p /etc/netplan.backup
        sudo mv /etc/netplan/*.yaml /etc/netplan.backup 2>/dev/null || true
        sudo mv /etc/netplan/*.yml /etc/netplan.backup 2>/dev/null || true
        fi
        ifname=`ip l | awk '/^[1-9]/ {sub(":","",$2);if ($2=="lo") next; print $2;nextfile}'`
        sudo tee /etc/netplan/$(date +%F-%H_%M).yaml <<EOF >/dev/null
        network:
          version: 2
          ethernets:
            $ifname:
              addresses:
              - $fullip
              nameservers:
                addresses:
                - $dns
              gateway4: $gw
              dhcp4: false
        EOF
        sudo netplan generate 2>/dev/null && sudo netplan apply  2>/dev/null

runcmd:
    - date > /root/cloudinit.log
    - echo "Updating the instance IP to ${ip_address}"
    - chmod +x /root/configure_ip.sh
    - /root/configure_ip.sh ${ip_address} ${gateway_ip} 8.8.8.8
    