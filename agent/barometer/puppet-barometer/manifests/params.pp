# Parameters for puppet-barometer
#
class barometer::params {
  include ::openstacklib::defaults

  case $::osfamily {
    'RedHat': {
    }
    'Debian': {
    }
    default: {
      fail("Unsupported osfamily: ${::osfamily} operatingsystem")
    }

  } # Case $::osfamily
}
