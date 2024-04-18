# Prepare your web servers

package {'nginx':
ensure => installed
}

service {'nginx':
ensure => 'running',
enable => true
}

file { ['/data', '/data/web_static',
'/data/web_static/releases', '/data/web_static/shared/',
'/data/web_static/releases/test']:
ensure => directory,
owner  => 'ubuntu',
group  => 'ubuntu'
}

file { '/data/web_static/releases/test/index.html':
ensure  => present,
owner   => 'ubuntu',
group   => 'ubuntu',
content => 'Hello from web_static\n'
}

file { '/data/web_static/current':
ensure => link,
target => '/data/web_static/releases/test/',
owner  => 'ubuntu',
group  => 'ubuntu'
}

exec {'serve_static':
notify  => Service['nginx'],
command => "/bin/sed -i '/^\tserver_name.*/a \\\tlocation /hbnb_static {\\n\t\talias /data/web_static/current/;\\n\t}\\n' /etc/nginx/sites-available/default"
}
