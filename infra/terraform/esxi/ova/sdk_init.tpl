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
        ip=$(echo $fullip | cut -d"/" -f1 )
        prefix=$(echo $fullip | cut -d"/" -f2 )

        ifname=`ip l | awk '/^[1-9]/ {sub(":","",$2);if ($2=="lo") next; print $2;nextfile}'`
        mac_add=$(ifconfig $ifname | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
        sudo tee /etc/sysconfig/network-scripts/ifcfg-eth0 <<EOF >/dev/null
        # Created by cloud-init on instance boot automatically, do not edit.
        #
        NM_CONTROLLED=no
        BOOTPROTO=none
        DEVICE=$ifname
        HWADDR=$mac_add
        ONBOOT=yes
        STARTMODE=auto
        TYPE=Ethernet
        USERCTL=no
        NETMASK=255.255.255.0
        IPADDR=$ip
        PREFIX=$prefix
        GATEWAY=$gw
        DNS1=$dns
        IPV6INIT=no
        DEFROUTE=yes
        IPV4_FAILURE_FATAL=no
        UUID=a5855473-efea-4ef4-a414-f350e677276
        NAME=$ifname
        EOF
        sudo tee -a /etc/resolv.conf <<EOF
        NAMESERVER 8.8.8.8
        EOF
        sudo systemctl restart network  2>/dev/null || errorbox "Configuration error"
        sudo /home/centos/flush_iptables.sh

runcmd:
    - date > /root/cloudinit.log
    - echo "Updating the instance IP to ${ip_address}"
    - chmod +x /root/configure_ip.sh
    - /root/configure_ip.sh ${ip_address} ${gateway_ip} 8.8.8.8
    