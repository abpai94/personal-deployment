Vagrant.configure('2') do | config |
  config.vm.provider "virtualbox" do | franklinvm |
    franklinvm.cpus = 4
    franklinvm.memory = 1024
  end
  config.vm.define 'franklin' do | franklin |
    franklin.vm.box = 'generic/debian12'
    franklin.vm.network 'forwarded_port', guest: 51820, host: 51820, protocol: 'udp'  # wireguard_vpn
    franklin.vm.network 'forwarded_port', guest: 51821, host: 51821, protocol: 'tcp'  # wireguard_ui
    franklin.vm.network 'forwarded_port', guest: 9091, host: 9091                     # authelia
    franklin.vm.network 'forwarded_port', guest: 80, host: 80                         # traefik_http
    franklin.vm.network 'forwarded_port', guest: 443, host: 443                       # traefik_https
    franklin.vm.network 'forwarded_port', guest: 8080, host: 8080                     # traefik_dashboard
    franklin.vm.network 'forwarded_port', guest: 3000, host: 3000                     # dashboard
    franklin.vm.network 'forwarded_port', guest: 9000, host: 9000                     # portainer
    franklin.vm.network 'forwarded_port', guest: 81, host: 80                         # pihole_ui
    franklin.vm.network 'forwarded_port', guest: 53, host: 53, protocol: 'udp'        # pihole_dns_udp
    franklin.vm.network 'forwarded_port', guest: 53, host: 53, protocol: 'tcp'        # pihole_dns_tcp
    franklin.vm.network 'forwarded_port', guest: 67, host: 67                         # pihole_dhcp
    franklin.vm.network 'forwarded_port', guest: 82, host: 80                         # vaultwarden
    franklin.vm.network 'forwarded_port', guest: 84, host: 80                         # personal-website
  end
  config.vm.provider "virtualbox" do | eleanorvm |
    eleanorvm.cpus = 8
    eleanorvm.memory = 8192
  end
  config.vm.define 'eleanor' do | eleanor |
    eleanor.vm.box = 'generic/debian12'
    eleanor.vm.network 'forwarded_port', guest: 8112, host: 8112                     # deluge_ui
    eleanor.vm.network 'forwarded_port', guest: 6881, host: 6881, protocol: 'tcp'    # deluge_torrect_tcp
    eleanor.vm.network 'forwarded_port', guest: 6881, host: 6881, protocol: 'udp'    # deluge_torrent_udp
    eleanor.vm.network 'forwarded_port', guest: 7878, host: 7878                     # radarr
    eleanor.vm.network 'forwarded_port', guest: 8989, host: 8989                     # sonarr
    eleanor.vm.network 'forwarded_port', guest: 8096, host: 8096                     # jellyfin
    eleanor.vm.network 'forwarded_port', guest: 9696, host: 9696                     # prowlarr
    eleanor.vm.network 'forwarded_port', guest: 443, host: 1443                      # nextcloud
    eleanor.vm.network 'forwarded_port', guest: 83, host: 1080                       # onlyoffice
  end
end