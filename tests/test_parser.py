import os

from ftl_installer.config.Config import Config
from ftl_installer.parser.Parser import Parser
from unittest import TestCase


test_config = """
    version: v1
    deployment:
      variant: openshift-enterprise
      variant_version: 3.1
      ansible_ssh_user: root
      ansible_become: no
      use_openshift_sdn: yes
      sdn_network_plugin_name: redhat/openshift-ovs-subnet
      masters:
        default_subdomain: apps.test.example.com
        master_identity_providers:
        - name: htpasswd_auth
          login: true
          challenge: true
          kind: HTPasswdPasswordIdentityProvider
          filename: /etc/openshift/htpasswd
        hosts:
        - ip: 10.0.0.1
          hostname: master-private.example.com
          public_ip: 24.222.0.1
          public_hostname: master.example.com
          containerized: true
      nodes:
        kubelet_args:
          max_pods:
          - "100"
        storage_plugin_deps:
        - ceph
        - glusterfs
        hosts:
        - ip: 10.0.0.1
          hostname: master-private.example.com
          public_ip: 24.222.0.1
          public_hostname: master.example.com
          schedulable: no
          containerized: true
        - ip: 10.0.0.2
          hostname: node1-private.example.com
          public_ip: 24.222.0.2
          public_hostname: node1.example.com
          node_labels:
            region: primary
            zone: default
        - ip: 10.0.0.3
          hostname: node2-private.example.com
          public_ip: 24.222.0.3
          public_hostname: node2.example.com
          node_labels:
            region: secondary
            zone: default
      etcd:
        initial_cluster_token: etcd-cluster-1
        hosts:
        - ip: 10.0.0.4
          hostname: etcd1-private.example.com
          etcd_interface: eth0
    """


class TestParser(TestCase):
    '''
    Test the command line parser.
    It defines three methods for testing:
        empty args
        config from file method from Config class.
        write_config method from Config class.
    '''

    def test_with_empty_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        parser = Parser()
        args = parser.parser.parse_args([])
        self.assertFalse(args.config)
        self.assertFalse(args.verbose)
        self.assertFalse(args.quiet)

    def test_config_from_file(self):
        """
        Test if config was found.
        """
        parser = Parser()
        args = parser.parser.parse_args(['-c'])
        if args.config:
            config = Config()
            config.config_file = "./config"
            config.config = test_config
            config.config_from_file()
            self.assertTrue(config.config)
            os.remove(config.config_file)

    def test_write_config(self):
        """
        Test if config file was written.
        """
        config = Config()
        config.config = test_config
        config.config_file = "./config"
        config.write_config()
        with open(config.config_file) as config_file:
            data = config_file.read()
            self.assertTrue(data)
        os.remove(config.config_file)
