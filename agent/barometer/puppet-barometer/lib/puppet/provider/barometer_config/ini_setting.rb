Puppet::Type.type(:barometer_config).provide(
  :ini_setting,
  :parent => Puppet::Type.type(:openstack_config).provider(:ini_setting)
) do

  def self.file_path
    '/etc/barometer/barometer.conf'
  end

end
