====================
matejc.myportal
====================

My personal Plone web portal.

* `Source code @ GitHub <https://github.com/matejc/matejc.myportal>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/matejc/matejc.myportal>`_


Development
===========

.. sourcecode:: bash

    git clone git://github.com/matejc/matejc.myportal.git
    virtualenv --no-site-packages matejc.myportal/
    cd matejc.myportal
    make

    # run instance in foreground
    bin/instance fg


Production
==========

This was tested on Ubuntu server 12.04.

.. sourcecode:: bash

    sudo su -
        useradd -s /bin/bash -m myportal
        groupadd myportal
        usermod -G myportal myportal
        passwd myportal

        cd /etc/nginx/certs/
        openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -keyout <hostname>.key -out <hostname>.crt
        cp /home/myportal/matejc.myportal/etc/nginx.conf /etc/nginx/sites-available/myportal
        ln -s /etc/nginx/sites-available/myportal /etc/nginx/sites-enabled/
        exit

    su - myportal

    git clone git://github.com/matejc/matejc.myportal.git
    virtualenv --no-site-packages matejc.myportal/
    cd matejc.myportal
    vim buildout.d/production.cfg
        # at least change password
        # in section [zope1] change user = admin:<change>
    bin/python bootstrap.py -d --version 1.7.1
    bin/buildout -c production.cfg

    bin/supervisord

    sudo /etc/init.d/nginx reload

