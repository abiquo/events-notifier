#!/usr/bin/env python

#       The Abiquo Platform
#       Cloud management application for hybrid clouds
#       Copyright (C) 2008-2013 - Abiquo Holding S.L.
#
#       This application is free software; you can redistribute it and/or
#       modify it under the terms of the GNU LESSER GENERAL PUBLIC
#       LICENSE as published by the Free Software Foundation under
#       version 3 of the License
#
#       This software is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#       LESSER GENERAL PUBLIC LICENSE v.3 for more details.
#
#       You should have received a copy of the GNU Lesser General Public
#       License along with this library; if not, write to the
#       Free Software Foundation, Inc., 59 Temple Place - Suite 330,
#       Boston, MA 02111-1307, USA.

def load_email_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    f = config.get('email', 'from')
    s = config.get('email', 'subject')
    ip = config.get('email', 'smtp_ip')
    port = config.get('email', 'smtp_port')
    tls = config.get('email','smtp_tls')
    user = config.get('email','smtp_user')
    password = config.get('email','smtp_password')

    return (f, s, ip, port, tls, user, password)

def load_api_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    api_url = config.get('abiquo', 'api_url')
    api_user = config.get('abiquo', 'api_user')
    api_pwd = config.get('abiquo', 'api_pwd')
    api_port = config.get('abiquo', 'api_port')
    ssl_verify_disabled = config.get('abiquo', 'skip_ssl_peer_verify')
    stream_path = str(config.get('abiquo', 'stream_path'))


    return (api_url, api_user, api_pwd, api_port, stream_path, ssl_verify_disabled)

def load_ruleeditor_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    rule_editor_enabled = int(config.get('ruleeditor', 'enabled'))
    rule_editor_port = int(config.get('ruleeditor', 'rule_editor_port'))

    return (rule_editor_enabled, rule_editor_port)

def load_main_config():
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read('notifier.cfg')

    retry_interval = int(config.get('main', 'retry_interval'))

    return (retry_interval)
