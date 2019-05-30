import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nginx_conf(host):
    cmd = host.run('nginx -t -c /etc/nginx/nginx.conf')
    assert cmd.rc == 0


def test_http(host):
    cmd = host.run('curl http://localhost')
    assert cmd.rc == 0
    assert "301 Moved Permanently" in cmd.stdout


def test_https(host):
    cmd = host.run('curl -k https://localhost')
    assert cmd.rc == 0
    assert "Hello Molecule!!" in cmd.stdout
